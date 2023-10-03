---
title: Tracer 源码阅读（5）
category: [Research, Software Security]
tags: [program analysis, code reading]
math: true
---

> 为了记录自己读代码的过程，开设 Tracer 源码阅读系列博客。该系列博客以 ACM CCS 22' Tracer 的源代码为分析对象，旨在理解论文思路和复现论文结果，为后续在未初始化变量上的改进工作提供思路。

上文提到为了实现新的 checker，首先需要设计好抽象域。从 Tracer 的开发流程看来，大多数漏洞都是对 API 的使用进行建模，但这和（测试集中所展现的）最简单的未初始化场景之间还有一定的 gap。所幸 Infer 本身也实现了关于未初始化的 checker：uninit 和 pulse，本文尝试从上述两个 checker 的代码中总结出符合 Tracer 的抽象域设计。

## uninit checker

uninit 的功能更加单一，代码结构也更加简单，不过它是基于的老版本的 Hil。

该 checker 的核心逻辑如下，抽象域维护了一个可能的未初始化变量列表 maybe_uninit_vars，在前向分析中不断迭代：

```ocaml
module D = UninitDomain.Domain = AbstractDomain.InvertedSet (HilExp.AccessExpression)

module MaybeUninitVars = UninitDomain.MaybeUninitVars
module AliasedVars = AbstractDomain.FiniteSet (UninitDomain.VarPair)
module RecordDomain = UninitDomain.Record (MaybeUninitVars) (AliasedVars) (D)

let checker ({InterproceduralAnalysis.proc_desc; tenv} as analysis_data) =
  (* start with empty set of uninit local vars and empty set of init formal params *)
  let maybe_uninit_vars = Initial.get_locals tenv proc_desc in
  let initial =
    { RecordDomain.maybe_uninit_vars= MaybeUninitVars.of_list maybe_uninit_vars
    ; aliased_vars= AliasedVars.empty
    ; prepost= {UninitDomain.pre= D.empty; post= D.empty} }
  in
  let proc_data =
    let formals = FormalMap.make (Procdesc.get_attributes proc_desc) in
    {analysis_data; formals}
  in
  Analyzer.compute_post proc_data ~initial proc_desc
  |> Option.map ~f:(fun {RecordDomain.prepost; _} -> prepost)
```

迭代的逻辑由 exec_instr 函数给出，其逻辑如下：

- Assign (lhs_access_expr, rhs_expr, loc)：递归地（在访问路径上）检查 rhs 中是否有未初始化变量，并报告；将 lhs 从 maybe_uninit_vars 中移除，并更新 prepost
- Call (_, HilInstr.Direct call, [HilExp.AccessExpression (AddressOf (Base base))], _, _)：如果为默认的构造函数，则从 maybe_uninit_vars 中移除所有的成员变量
- Call (_, call, actuals, _, loc)：一般情况下的函数调用，遍历所有的参数情况，例如当开启过程间分析时，对于参数为引用结构体和调用构造函数时，需要移除已经初始化的变量；开启过程内分析时，默认所有通过引用传递的参数都会被初始化；当函数为闭包时，会移除所有的从环境中捕获的变量
- Assume (expr, _, _, loc)：检测条件判断中是否使用了未初始化的变量

到此 uninit checker 介绍完毕，其大部分函数还是涉及到 C/C++ 对应 的 Hil 的处理