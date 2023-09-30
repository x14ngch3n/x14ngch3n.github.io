---
title: Tracer 源码阅读（3）
category: [Research, Software Security]
tags: [program analysis, code reading]
math: true
---

> 为了记录自己读代码的过程，开设 Tracer 源码阅读系列博客。该系列博客以 ACM CCS 22' Tracer 的源代码为分析对象，旨在理解论文思路和复现论文结果，为后续在未初始化变量上的改进工作提供思路。

在完成了基础的污点分析框架的搭建后，作者首先对 Integer Overflow 进行了实例化

## 1654d17: [APIMisuse] add new domains

### IntOverflow Domain

按照文章 4.1 节所引入的抽象域，IntOverflow 域的代码实现如下

```ocaml
module IntOverflow = struct
  type t = Bot | Top [@@deriving compare, equal]

  let to_string = function Bot -> "No Overflow" | Top -> "May Overflow"

  let bottom = Bot

  let top = Top

  let leq ~lhs ~rhs = match (lhs, rhs) with Bot, _ -> true | Top, Bot -> false | Top, Top -> true

  let join x y = match (x, y) with Bot, Bot -> Bot | Top, _ | _, Top -> Top

  let meet x y = match (x, y) with Bot, _ -> Bot | _, Bot -> Bot | _ -> Top

  let is_bot x = equal x Bot

  let widen ~prev ~next ~num_iters:_ = join prev next

  let narrow = meet

  let pp fmt x = F.fprintf fmt "%s" (to_string x)
end
```

作者把溢出与否用一个二元的抽象域 `Bot | Top` 来描述，这一部分也是我认为文章（为了保证 May Analysis）实现得比较草率的部分，在后续的实验中发现了很多的整数溢出的误报问题都是由这里的设计导致的。

### 67c851d: [APIMisuse] initialize overflow checker

扩展了 Model 的类型到两类函数摘要 exec_fun 和 check_fun，分别用于分析阶段和检查阶段

```ocaml
type exec_fun = model_env -> ret:Ident.t * Typ.t -> APIMisuseDomain.Mem.t -> APIMisuseDomain.Mem.t
type check_fun = model_env -> APIDom.Mem.t -> APIDom.CondSet.t -> APIDom.CondSet.t
type model = {exec: exec_fun; check: check_fun}
```

增加了对于 fread（exec_fun）和 malloc（check_fun）函数的建模，具体逻辑如下：

```ocaml
let fread buffer =
let exec {node; bo_mem_opt; location} ~ret:_ mem =
    match (buffer, bo_mem_opt) with
    | Exp.Lvar _, Some bomem | Exp.Var _, Some bomem ->
        BoSemantics.eval_locs buffer bomem.pre
        |> Fun.flip
            (PowLoc.fold (fun l mem ->
                let v = Dom.UserInput.make node location |> Dom.Val.of_user_input in
                let loc = Dom.LocWithIdx.of_loc l in
                Dom.Mem.add loc v mem ))
            mem
    | _, _ ->
        mem
in
{exec; check= empty_check_fun}


let malloc size =
let check {location} mem condset =
    let v = Sem.eval size mem |> APIDom.Val.get_int_overflow in
    APIDom.CondSet.add (APIDom.Cond.make_overflow v location) condset
in
{empty with check}
```

对于 IntOverflow 这个新增的抽象域，也要实现对应的传播语义，即 eval 函数：

```ocaml
and eval exp mem =
  match exp with
  | Exp.Var id ->
      Var.of_id id |> AbsLoc.Loc.of_var |> Dom.LocWithIdx.of_loc |> Fun.flip Mem.find mem
  | Exp.Lvar pvar ->
      pvar |> AbsLoc.Loc.of_pvar |> Dom.LocWithIdx.of_loc |> Fun.flip Mem.find mem
  | Exp.Const _ ->
      Dom.Init.Init |> Val.of_init
  | Exp.BinOp (bop, e1, e2) ->
      eval_binop bop e1 e2 mem
  | Exp.UnOp (uop, e, _) ->
      eval_unop uop e mem
  | Exp.Cast (_, e1) ->
      eval e1 mem
  | _ ->
      (* TODO *)
      Val.bottom

and eval_binop bop e1 e2 mem = ...
```

## cc899de: [APIMisuse] add rules for integer overflow

对于 IntOverflow 域的传播语义进行了完善，体现在对 eval_binop 函数的两个参数都进行了溢出和污点的传播

## 32e7f57: [APIMisuse] interproc analysis

修改了报告的条件为同时满足溢出和污点条件，如下代码所示：

```ocaml
let may_overflow = function
| Overflow cond ->
    IntOverflow.is_top cond.size && UserInput.is_taint cond.user_input
| _ ->
    false
```

为了支持过程间分析，还在 IntOverflow 域加入了 InferBO 提供的符号值

## 56c3e75: [APIMisuse] refactoring

将 APIMisuseModels 单独抽象成一个模块

## 总结

这五个 commit 实现了最基本的整数溢出分析，同时也进一步完善了分析框架。该系列博客暂且告一段落，下一步的目标是为其添加未初始化的抽象域。