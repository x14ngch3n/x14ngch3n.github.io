---
title: Tracer 源码阅读（2）
category: [Research, Software Security]
tags: [program analysis, code reading]
math: true
---

> 为了记录自己读代码的过程，开设 Tracer 源码阅读系列博客。该系列博客以 ACM CCS 22' Tracer 的源代码为分析对象，旨在理解论文思路和复现论文结果，为后续在未初始化变量上的改进工作提供思路。

## tracer-infer 整体分析

tracer-infer 一共包括了 132 个 commit（前缀为 "[APIMisuse]"），最终结果实现为一个单独的 checker 目录，加上对于其他配置文件的修改以及注册 checker 的代码，使得作者自定义的 API-Misuse checker 能够在命令行被 Infer 直接调用。

主要分析 [api-misuse](https://github.com/prosyslab/tracer-infer/tree/master/infer/src/api-misuse) 目录的代码，按照开发顺序，重点分析功能性改动，顺便熟悉 Infer 的开发流程。因为开发过程的局限性，不求第一次就看懂每个 commit 的功能，作出精准的解释，但求对于整体代码开发的结构和趋势有个大概的了解，熟悉最终代码的修改位置。

整体的代码量为 3k LoC，分别如下：

```bash
======================================================================================================================================================================================================================================
 Language                                                                                                                                                                   Files        Lines         Code     Comments       Blanks
======================================================================================================================================================================================================================================
 OCaml                                                                                                                                                                          6         3284         2802           17          465
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 infer/src/api-misuse/APIMisuseDomain.ml                                                                                                                                                  1109          876            2          231
 infer/src/api-misuse/APIMisuseModel.ml                                                                                                                                                   1009          889            2          118
 infer/src/api-misuse/APIMisuseChecker.ml                                                                                                                                                  692          631           10           51
 infer/src/api-misuse/APIMisuseTrace.ml                                                                                                                                                    243          202            2           39
 infer/src/api-misuse/APIMisuseSemantics.ml                                                                                                                                                222          196            1           25
 infer/src/api-misuse/util.ml                                                                                                                                                                9            8            0            1
======================================================================================================================================================================================================================================
 Total                                                                                                                                                                          6         3284         2802           17          465
======================================================================================================================================================================================================================================
```

## 40c59af: [APIMisuse] add checker

### 如何创建一个 checker

万事开头难，作者 Kihong Heo 凭借其对 Infer 开发足够的熟悉（作者之前为 Infer 团队开发过 InferBO[^inferbo]），直接在一开始就为 api-misuse checker 搭好了框架。

先分析配置类的代码修改，其中值得关注的是 checker 的注册逻辑：

```ocaml
{ checker= APIMisuse
    ; callbacks=
        [ ( interprocedural2 Payloads.Fields.api_misuse_checker
              Payloads.Fields.buffer_overrun_analysis APIMisuseChecker.checker
          , Clang ) ] }
```

可以看出作者计划实现一个 inter-procedural 的 checker，且该 checker 还依赖于 InferBO 中 buffer_overrun_analysis checker 的分析结果。此外，作者还修改了其他的文件，添加新的 checker 名称，新的 IssueType，以及增加了编译目标。

在 [api-misuse] 目录下，作者提供了三个 ml 模块，但并没有提供对应的 mli 接口文件，部分类型直接写在了代码当中，部分需要通过 IDE 的类型推断

### APIMisuseDomain

按照 checker 开发规范，本模块定义了 checker 的抽象域。该模块的代码主要依照文中第 3.2 章的定义实现：

$$\text{(abstract state) } S = C \rightarrow M$$

$$\text{(abstract memory) } M = X \rightarrow T \times V$$

$$\text{(taint) } T = \mathbb{P} (C)$$

例如抽象内存的代码实现如下，使用 `AbstractDomain.Map` 来描述源代码位置和值的对映关系：

```ocaml
module Mem = struct
  include AbstractDomain.Map (LocWithIdx) (Val)

  let initial = empty

  let find k m = try find k m with _ -> Val.bottom
end
```

由于当前的状态还不是完全体，所以对本模块的其他签名先简单概括如下：

- LocWithIdx：对于抽象内存位置的抽象，使用了 InferBO[^bufferoverrun] 的 `AbsLoc.Loc`，且包含了 Interval 域
- Init：对于 value information 的抽象，目前只实现了简单的 `Bot | Init | Uninit | Top` 域
- PowLocWithIdx：对于 taint information 的抽象，实际上是 `LocWithIdx` 的 PowerSet
- Val：对于 abstract value 的抽象，包括 value information 和 taint information 

### APIMisuseSemantics

该 checker 把定义在抽象域上的操作（Semantics）分离开来，形成了一个单独的模块。

当前该模块实现了 `eval_locs` 函数：

```ocaml
let rec eval_locs : Exp.t -> Mem.t -> Dom.PowLocWithIdx.t
```

其对于给定的 `Exp.t` 类型的表达式[^exp]，从抽象内存中获取污点信息，实现了文中第一条抽象语义。

### APIMisuseChecker

该模块为 checker 的主要模块，和其他的 checker 类似，主要的执行逻辑在 `TransferFunctions.exec_instr` 和 `report` 函数中。

- exec_instr：负责描述执行每一条语句时，对于 abstract state 的修改，结果为对抽象内存的更新
  - Load / Prune：不处理
  - Store：获取 rhs 的污点信息，并把污点信息添加到内存当中
  - Call：借助 Models 对函数的建模信息，以及 ProcnameDispatcher 机制，将当前匹配到的函数交由对应的代码进行处理。每个建模的函数（model 类型）都要实现一个 exec 方法，并将建模逻辑（例如污点信息的传播）写在里面。这个机制的实现对于后续的 source 和 sink 点的添加很有帮助
- report：报告可能产生的问题，并对应到源代码中的位置（即 Location）
  - 值得注意的是，该 checker 采用了 `NormalOneInstrPerNode` 的 CFG，使得其分析时每个节点只有一条指令
  - report 中先遍历 Nodes，最后调用到 check_instr 来检查每次遇到 Load 指令时，抽象内存中是否包含污点值且所有污点值的来源中是否存在未被初始化的情况，则报告源代码位置
  - For taint checking, we collect all possible source points that lead to the value.


此外，该 checker 还实现了一个 util.ml 模块，提供了打印 successor nodes 的函数，暂时用不着。

## 5f24107: [APIMisuse] handle function call

在 Summary 中加入了 `CondSet`，作为最后报告的类型，其定义为：

```ocaml
module Cond = struct
  type t = {absloc: LocWithIdx.t; init: Init.t; loc: Location.t} [@@deriving compare]
```

在 exec_instr 中加入了对于 Load 指令的处理，在 check_instr 中加入了 Call 指令的处理，负责在过程间传递 Summary

## 参考链接

[^inferbo]: https://research.facebook.com/blog/2017/2/inferbo-infer-based-buffer-overrun-analyzer/
[^bufferoverrun]: https://sjxer723.github.io/2023/02/04/Infer-Buffer-Overrun-II/
[^exp]: https://fbinfer.com/odoc/1.1.0/infer/IR/Exp/index.html#type-t