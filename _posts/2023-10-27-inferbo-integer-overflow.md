---
title: InferBO 检测整数溢出漏洞分析
category: [Research, Software Security]
tags: [program analysis, code reading]
math: true
---

> 前段时间对 Tracer 的源码进行了分析，虽然这项工作的重点在于漏洞相似性分析，但其对于 IO2BO 这一类漏洞的检测也有贡献。为了更好地理解基于抽象解释（区间分析）来实现整数溢出检测的思路，本文决定从看代码的角度来分析 InferBO 的检测流程。

## 前置知识

从检测的精度出发，InferBO 将整数溢出分为了 4 类报告[^inferbo_issues]，置信度从高到低如下所示:

- **INTEGER_OVERFLOW_L1**: 确定会产生溢出的情况，例如 [2147483647,2147483647] + [1,1]
- **INTEGER_OVERFLOW_L2**: 在区间范围内可能产生溢出的情况，例如 [2147483647,2147483647] + [0,1]
- **INTEGER_OVERFLOW_L5**：考虑所有可能导致溢出的计算（需要通过 `--no-filtering` 开启）
  - 这一类低精度的 Issue 都是默认隐藏的：https://github.com/facebook/infer/pull/1736#discussion_r1119811587
- **INTEGER_OVERFLOW_U5**: 考虑外界输入导致的溢出，例如 [-inf, inf] * 2
  - 仅用于外界函数引入不可知变量的情况，这也是最符合现实漏洞（从外部读入污点数据）的情况

如上所示，可以看出 InferBO 采用了区间域（Interval）作为抽象域。

## 测试代码

我们可以通过阅读 InferBO 的测试代码[^inferbo_test]来更直观地理解这 4 类报告。由于 InferBO 重点还是在于检测 BufferOverrun，所以其测试代码中只有少部分的是针对 IntegerOverflow 的。通过 [issues.exp](https://github.com/facebook/infer/blob/main/infer/tests/codetoanalyze/c/bufferoverrun/issues.exp) 可以看到，大部分和 IntegerOverflow 相关的代码都在 [arith.c](https://github.com/facebook/infer/blob/main/infer/tests/codetoanalyze/c/bufferoverrun/arith.c) 下。

针对 4 类报告，分别举例说明：

```c
// codetoanalyze/c/bufferoverrun/arith.c, integer_overflow_by_addition_Bad, 4, INTEGER_OVERFLOW_L1, no_bucket, ERROR, [<LHS trace>,Assignment,<RHS trace>,Assignment,Binary operation: (2000000000 + 2000000000):signed32]
void integer_overflow_by_addition_Bad() {
  char arr[10];
  int32_t x = 2000000000;
  int32_t y = 2000000000;
  int32_t z = x + y; // z is a negative number.
  if (z < 10) {
    arr[z] = 0;
  }
}

// codetoanalyze/c/bufferoverrun/arith.c, integer_overflow_by_addition_l2_Bad, 7, INTEGER_OVERFLOW_L2, no_bucket, ERROR, [<LHS trace>,Assignment,<RHS trace>,Assignment,Binary operation: ([0, 2000000000] + [0, 2000000000]):signed32]
void integer_overflow_by_addition_l2_Bad(int x) {
  int32_t y;
  if (x) {
    y = 0;
  } else {
    y = 2000000000;
  }
  y = y + y;
}

// codetoanalyze/c/bufferoverrun/arith.c, two_safety_conditions2_Bad, 9, INTEGER_OVERFLOW_L5, no_bucket, ERROR, [<LHS trace>,Call,Assignment,Assignment,<RHS trace>,Assignment,Binary operation: ([0, +oo] + [0, 80]):unsigned32]
void two_safety_conditions2_Bad(uint32_t s) {
  uint32_t x = unknown_nat();
  uint32_t y, z;

  if (unknown_function()) {
    y = 0;
  } else {
    y = 80;
  }
  z = x + y; // integer overflow L5: [0, +oo] + [0, 80]

  if (s >= 10 && s <= 20) {
    z = x + s; // [0, +oo] + [max(10, s.lb), min(20, s.ub)]
  }
}

// codetoanalyze/c/bufferoverrun/arith.c, muliply_two_Bad, 2, INTEGER_OVERFLOW_U5, no_bucket, ERROR, [<LHS trace>,Unknown value from: unknown_uint,Assignment,Binary operation: ([-oo, +oo] × 2):unsigned64]
void muliply_two_Bad() {
  uint64_t x = unknown_uint();
  uint64_t y = x * 2;
}
```

## 如何找到代码

- 正向搜索：在 [bufferOverrunChecker.ml](https://github.com/facebook/infer/blob/89a599ef21cc3e314592e96423df8ce5ede7f961/infer/src/bufferoverrun/bufferOverrunChecker.ml#L309) 中找到了调用 `check_expr_for_integer_overflow` 的检测函数的入口，分别在处理 Load，Store 以及 Prune 指令时发生了调用
- 反向搜索：根据关键词 "integer_overflow_l1" ，在 [bufferOverrunProofObligations.ml](https://github.com/facebook/infer/blob/89a599ef21cc3e314592e96423df8ce5ede7f961/infer/src/bufferoverrun/bufferOverrunProofObligations.ml#L143) 中找到了最终产生报告的函数 `check`

## 检测过程分析

首先分析 `check_expr_for_integer_overflow` 函数，很显然这会是一个递归函数，用于将检测任务分发到 exp 包含的子表达式上。但最后，其都要落到对于二元表达式的检查（因为这是导致溢出的主要原因），该逻辑被派发到了 `check_binop_for_integer_overflow` 函数中。如果子表达式最终不包含二元表达式，则跳过检查。

```ocaml
let rec check_expr_for_integer_overflow integer_type_widths pname exp location mem cond_set =
  match exp with
  | Exp.UnOp (_, e, _)
  | Exp.Exn e
  | Exp.Lfield (e, _, _)
  | Exp.Cast (_, e)
  | Exp.Sizeof {dynamic_length= Some e} ->
      check_expr_for_integer_overflow integer_type_widths pname e location mem cond_set
  | Exp.BinOp (bop, lhs, rhs) ->
      cond_set
      |> check_binop_for_integer_overflow integer_type_widths pname bop ~lhs ~rhs location mem
      |> check_expr_for_integer_overflow integer_type_widths pname lhs location mem
      |> check_expr_for_integer_overflow integer_type_widths pname rhs location mem
  | Exp.Lindex (e1, e2) ->
      cond_set
      |> check_expr_for_integer_overflow integer_type_widths pname e1 location mem
      |> check_expr_for_integer_overflow integer_type_widths pname e2 location mem
  | Exp.Closure {captured_vars} ->
      List.fold captured_vars ~init:cond_set ~f:(fun cond_set (e, _, _, _) ->
          check_expr_for_integer_overflow integer_type_widths pname e location mem cond_set )
  | Exp.Var _ | Exp.Const _ | Exp.Lvar _ | Exp.Sizeof {dynamic_length= None} ->
      cond_set
```

在二元表达式中，首先对于肯定不可能溢出的情况进行了筛选（比如 (unsigned int)0-const 这样的操作）。然后对于一般情况，在提取出 lhs 和 rhs 对应的抽象域的值之后，交给 [bufferOverrunUtils.ml](https://github.com/facebook/infer/blob/89a599ef21cc3e314592e96423df8ce5ede7f961/infer/src/bufferoverrun/bufferOverrunUtils.ml#L333) 模块中的 `binary_operation` 处理。 

```ocaml
let check_binop_for_integer_overflow integer_type_widths pname bop ~lhs ~rhs location mem cond_set =
  match bop with
  | Binop.MinusA (Some typ) when Typ.ikind_is_unsigned typ && Exp.is_zero lhs && Exp.is_const rhs ->
      cond_set
  | Binop.PlusA (Some _) | Binop.MinusA (Some _) | Binop.Mult (Some _) ->
      let lhs_v = Sem.eval integer_type_widths lhs mem in
      let rhs_v = Sem.eval integer_type_widths rhs mem in
      let latest_prune = Dom.Mem.get_latest_prune mem in
      BoUtils.Check.binary_operation integer_type_widths pname bop ~lhs:lhs_v ~rhs:rhs_v
        ~latest_prune location cond_set
  | _ ->
      cond_set
```

该函数似乎也不会做进一步的检测，而是直接把刚刚的表达式以及相应的 trace 加入到 ConditionSet 中。

```ocaml
let binary_operation integer_type_widths pname bop ~lhs ~rhs ~latest_prune location cond_set =
  let lhs_itv = Dom.Val.get_itv lhs in
  let rhs_itv = Dom.Val.get_itv rhs in
  match (lhs_itv, rhs_itv) with
  | NonBottom lhs_itv, NonBottom rhs_itv ->
      L.(debug BufferOverrun Verbose)
        "@[<v 2>Add condition :@,bop:%s@,  lhs: %a@,  rhs: %a@,@]@." (Binop.str Pp.text bop)
        Itv.ItvPure.pp lhs_itv Itv.ItvPure.pp rhs_itv ;
      PO.ConditionSet.add_binary_operation integer_type_widths location pname bop ~lhs:lhs_itv
        ~rhs:rhs_itv ~lhs_traces:(Dom.Val.get_traces lhs) ~rhs_traces:(Dom.Val.get_traces rhs)
        ~latest_prune cond_set
  | _, _ ->
      cond_set
```

难道到这里就结束了？实际上通过运行查看 Infer 的调试信息可以发现，检测的代码是在 CFG 的最后一个基本块（EXIT）才运行的。即 Infer 采用了一种 delay 的方式进行检测，bufferOverrunUtils.ml 里的代码只负责检测任务。具体表现为添加一个 BinaryOperationCondition 对象。该对象定义在 bufferOverrunProofObligations.ml 模块中，整个 InferBO 一共定义了 3 类检查条件：

```ocaml
module Condition = struct
  type t =
    | AllocSize of AllocSizeCondition.t
    | ArrayAccess of ArrayAccessCondition.t
    | BinaryOperation of BinaryOperationCondition.t
  [@@deriving compare, equal]

module BinaryOperationCondition = struct
type binop_t = Plus | Minus | Mult [@@deriving compare, equal]

type t =
  { binop: binop_t
  ; typ: Typ.ikind
  ; integer_widths: IntegerWidths.t
  ; lhs: ItvPure.t
  ; rhs: ItvPure.t
  ; pname: Procname.t }
[@@deriving compare, equal]
```

如此一来便能够对接上最后产生报告的 check 函数了，其实际上是由 BinaryOperationCondition 实现的，由 Condition 类进行分发。当然，Condition 类外还包装了 ConditionSet 和 ConditionWithTrace 两个类，和 InferBO 更上层的处理逻辑有关，本文先不研究。

```ocaml
let check cond trace =
  match cond with
  | AllocSize c ->
      AllocSizeCondition.check c
  | ArrayAccess c ->
      ArrayAccessCondition.check c
  | BinaryOperation c ->
      BinaryOperationCondition.check c trace
```

所有的检测逻辑都在 BinaryOperationCondition.check 函数里面实现。大致逻辑如下：先排除故意的溢出（随机数运算）和不可能的溢出（mult_one），随后获取 lhs 和 rhs 的 Itv 值，并在抽象域上进行计算。将计算结果与该类型的 Itv 进行比较，根据 Issues 里的定义产生报告。在正式检测时，还对 Overflow 和 Underflow 两种情况进行了区分，如果是值域上不可能溢出的（运算包含 0，1 / 加法不会导致下溢 等情况），直接不进行检测。可以见得，为了排除掉许多不可能产生溢出的情况，InferBO 在多个阶段都进行了 sanitization。

```ocaml
let should_check {binop; typ; lhs; rhs} =
  let cannot_underflow, cannot_overflow =
    match (binop, Typ.ikind_is_unsigned typ) with
    | Plus, true ->
        (true, false)
    | Minus, true ->
        (false, true)
    | Mult, true ->
        (true, false)
    | Plus, false ->
        ( ItvPure.is_ge_zero lhs || ItvPure.is_ge_zero rhs
        , ItvPure.is_le_zero lhs || ItvPure.is_le_zero rhs )
    | Minus, false ->
        ( ItvPure.is_ge_zero lhs || ItvPure.is_le_zero rhs
        , ItvPure.is_le_mone lhs || ItvPure.is_ge_zero rhs )
    | Mult, false ->
        ( (ItvPure.is_ge_zero lhs && ItvPure.is_ge_zero rhs)
          || (ItvPure.is_le_zero lhs && ItvPure.is_le_zero rhs)
        , (ItvPure.is_ge_zero lhs && ItvPure.is_le_zero rhs)
          || (ItvPure.is_le_zero lhs && ItvPure.is_ge_zero rhs) )
  in
  (not cannot_underflow, not cannot_overflow)

let check ({binop; typ; integer_widths; lhs; rhs} as c) (trace : ConditionTrace.t) =
  if is_mult_one binop lhs rhs || is_deliberate_integer_overflow c trace then
    {report_issue_type= NotIssue; propagate= false}
  else
    let v =
      match binop with
      | Plus ->
          ItvPure.plus lhs rhs
      | Minus ->
          ItvPure.minus lhs rhs
      | Mult ->
          ItvPure.mult lhs rhs
    in
    let v_lb, v_ub = (ItvPure.lb v, ItvPure.ub v) in
    let typ_lb, typ_ub =
      let lb, ub = IntegerWidths.range_of_ikind integer_widths typ in
      (Bound.of_big_int lb, Bound.of_big_int ub)
    in
    let check_underflow, check_overflow = should_check c in
    if
      (* typ_lb <= v_lb and v_ub <= typ_ub, not an error *)
      ((not check_underflow) || Bound.le typ_lb v_lb)
      && ((not check_overflow) || Bound.le v_ub typ_ub)
    then {report_issue_type= NotIssue; propagate= false}
    else if
      (* v_ub < typ_lb or typ_ub < v_lb, definitely an error *)
      (check_underflow && Bound.lt v_ub typ_lb) || (check_overflow && Bound.lt typ_ub v_lb)
    then {report_issue_type= Issue IssueType.integer_overflow_l1; propagate= false}
    else if
      (* -oo != v_lb < typ_lb or typ_ub < v_ub != +oo, probably an error *)
      (check_underflow && Bound.lt v_lb typ_lb && Bound.is_not_infty v_lb)
      || (check_overflow && Bound.lt typ_ub v_ub && Bound.is_not_infty v_ub)
    then {report_issue_type= Issue IssueType.integer_overflow_l2; propagate= false}
    else
      let is_symbolic = ItvPure.is_symbolic v in
      let report_issue_type =
        if Config.bo_debug <= 3 && is_symbolic then SymbolicIssue
        else Issue IssueType.integer_overflow_l5
      in
      {report_issue_type; propagate= is_symbolic}
```

此外，INTEGER_OVERFLOW_U5 的检测有些不同，在 Condition.check 检测完之后，再对已有的 l5 的报告进行分析，产生 u5 的报告。本质上来说，这和 tracer 的思路很类似：先把所有可能的溢出场景分析出来（l5），如果涉及到外部未知输入则报告（u5）。

```ocaml
let check ~issue_type_u5 : _ t0 -> IssueType.t option =
 fun ct -> if has_unknown ct then Some issue_type_u5 else None

let check_integer_overflow ct = check ~issue_type_u5:IssueType.integer_overflow_u5 ct

let set_u5 {cond; trace} issue_type =
  (* It suppresses issues of array accesses by void pointers.  This is not ideal but Inferbo
     cannot analyze them precisely at the moment. *)
  if Condition.is_array_access_of_void_ptr cond then IssueType.buffer_overrun_l5
  else if
    ( IssueType.equal issue_type IssueType.buffer_overrun_l3
    || IssueType.equal issue_type IssueType.buffer_overrun_l4
    || IssueType.equal issue_type IssueType.buffer_overrun_l5 )
    && Condition.has_infty cond
  then Option.value (ConditionTrace.check_buffer_overrun trace) ~default:issue_type
  else if IssueType.equal issue_type IssueType.integer_overflow_l5 && Condition.has_infty cond
  then Option.value (ConditionTrace.check_integer_overflow trace) ~default:issue_type
  else issue_type

let check cwt =
  let ({report_issue_type; propagate} as checked) = Condition.check cwt.cond cwt.trace in
  match report_issue_type with
  | NotIssue | SymbolicIssue ->
      checked
  | Issue issue_type ->
      let issue_type = set_u5 cwt issue_type in
      (* Only report if the precision has improved.
         This is approximated by: only report if the issue_type has changed. *)
      let report_issue_type =
        match cwt.reported with
        | Some reported when Reported.equal reported issue_type ->
            (* already reported and the precision hasn't improved *) SymbolicIssue
        | _ ->
            (* either never reported or already reported but the precision has improved *)
            Issue issue_type
      in
      {report_issue_type; propagate}
```

## 原理分析

整体思路分析完了，但真正难的点还是在于如何使用 Interval 域，并提供抽象语义。在 InferBO 中，Dom.Val.t 是抽象值的类型，其包含了 Itv.t：

```ocaml
module Val = struct
  type t =
    { itv: Itv.t
    ; itv_thresholds: ItvThresholds.t
    ; itv_updated_by: ItvUpdatedBy.t
    ; modeled_range: ModeledRange.t
    ; powloc: PowLoc.t
    ; arrayblk: ArrayBlk.t
    ; func_ptrs: FuncPtr.Set.t
    ; traces: TraceSet.t }
  [@@deriving abstract_domain]
```

Itv.t 的类型实际为 BottomLifted 过的 ItvPure.t，其包含了两个 Bound：

```ocaml
module ItvPure = struct
  (** (l, u) represents the closed interval [l; u] (of course infinite bounds are open) *)
  type t = Bound.t * Bound.t [@@deriving compare, equal]
```

Bound 的实现较为复杂，包含了一元（二元）函数的模型，Bound 也可以递归地表示为两个 Bound。除此之外，Bound 和 Itv 都提供了大量的辅助函数，用于提供常见的 Interval（比如常数）。

```ocaml
type t =
  | MInf  (** -oo *)
  | Linear of Z.t * SymLinear.t  (** [Linear (c, se)] represents [c+se] where [se] is Σ(c⋅x). *)
  | MinMax of Z.t * Sign.t * MinMax.t * Z.t * Symb.Symbol.t
      (** [MinMax] represents a bound of "int [+|-] [min|max](int, symbol)" format. For example,
          [MinMax (1, Minus, Max, 2, s)] represents [1-max(2,s)]. *)
  | MinMaxB of MinMax.t * t * t  (** [MinMaxB] represents a min/max of two bounds. *)
  | MultB of Z.t * t * t
      (** [MultB] represents a multiplication of two bounds. For example, [MultB (1, x, y)]
          represents [1 + x × y]. *)
  | PInf  (** +oo *)
[@@deriving compare, equal]
```

关于 Bound 的运算，我们主要从 CFG-related instruction 和 Transfer-related instruction 两个角度来看（借鉴 Infer 的思路）。

### CFG-related instruction

这里主要涉及到的是抽象域的 join/widen 等操作：

```ocaml
let join : t -> t -> t =
 fun (l1, u1) (l2, u2) -> (Bound.underapprox_min l1 l2, Bound.overapprox_max u1 u2)


let widen : prev:t -> next:t -> num_iters:int -> t =
 fun ~prev:(l1, u1) ~next:(l2, u2) ~num_iters:_ -> (Bound.widen_l l1 l2, Bound.widen_u u1 u2)


let widen_thresholds : thresholds:Z.t list -> prev:t -> next:t -> num_iters:int -> t =
 fun ~thresholds ~prev:(l1, u1) ~next:(l2, u2) ~num_iters:_ ->
  (Bound.widen_l_thresholds ~thresholds l1 l2, Bound.widen_u_thresholds ~thresholds u1 u2)
```

其中调用的关键函数是 `underapprox_min` 和 `overapprox_max`，对于 max 的计算直接给结果取反（小学数学）即可。

```ocaml
let underapprox_max b1 b2 =
  let res = neg (overapprox_min (neg b1) (neg b2)) in
  if equal res b1 then b1 else if equal res b2 then b2 else res


let overapprox_max b1 b2 =
  let res = neg (underapprox_min (neg b1) (neg b2)) in
  if equal res b1 then b1 else if equal res b2 then b2 else res
```

更复杂的逻辑实现在 `underapprox_min` 中，该函数为 `exact_min` 的封装，额外传入的 `otherwise` 函数用于处理一般情况：

```ocaml
let rec underapprox_min b1 b2 =
  exact_min b1 b2 ~otherwise
```

`exact_min` 首先尝试能否直接给出两者的大小，如果可以则直接取小。如果不行，则需要通过模式匹配来判断。具体的场景先不解释，在遇到实际 case 的时候再分析。

```ocaml
let exact_min : otherwise:(t -> t -> t) -> t -> t -> t =
 fun ~otherwise b1 b2 ->
  if le b1 b2 then b1
  else if le b2 b1 then b2
  else
    match (b1, b2) with
    | Linear (c1, x1), Linear (c2, x2) when SymLinear.is_zero x1 && SymLinear.is_one_symbol x2 ->
        mk_MinMax (c2, Plus, Min, Z.(c1 - c2), SymLinear.get_one_symbol x2)
    | Linear (c1, x1), Linear (c2, x2) when SymLinear.is_one_symbol x1 && SymLinear.is_zero x2 ->
        mk_MinMax (c1, Plus, Min, Z.(c2 - c1), SymLinear.get_one_symbol x1)
    | Linear (c1, x1), Linear (c2, x2) when SymLinear.is_zero x1 && SymLinear.is_mone_symbol x2 ->
        mk_MinMax (c2, Minus, Max, Z.(c2 - c1), SymLinear.get_mone_symbol x2)
    | Linear (c1, x1), Linear (c2, x2) when SymLinear.is_mone_symbol x1 && SymLinear.is_zero x2 ->
        mk_MinMax (c1, Minus, Max, Z.(c1 - c2), SymLinear.get_mone_symbol x1)
    | MinMax (c1, (Plus as sign), (Min as minmax), _, s), Linear (c2, se)
    | Linear (c2, se), MinMax (c1, (Plus as sign), (Min as minmax), _, s)
    | MinMax (c1, (Minus as sign), (Max as minmax), _, s), Linear (c2, se)
    | Linear (c2, se), MinMax (c1, (Minus as sign), (Max as minmax), _, s)
      when SymLinear.is_zero se ->
        let d = Sign.eval_neg_if_minus sign Z.(c2 - c1) in
        mk_MinMax (c1, sign, minmax, d, s)
    | MinMax (c1, Plus, Min, d1, s1), Linear (c2, s2)
    | Linear (c2, s2), MinMax (c1, Plus, Min, d1, s1)
      when SymLinear.is_one_symbol_of s1 s2 ->
        let c = Z.min c1 c2 in
        let d = Z.(c1 + d1) in
        mk_MinMax (c, Plus, Min, Z.(d - c), s1)
    | MinMax (c1, Minus, Max, d1, s1), Linear (c2, s2)
    | Linear (c2, s2), MinMax (c1, Minus, Max, d1, s1)
      when SymLinear.is_mone_symbol_of s1 s2 ->
        let c = Z.min c1 c2 in
        let d = Z.(c1 - d1) in
        mk_MinMax (c, Minus, Max, Z.(c - d), s1)
    | MinMax (c1, (Minus as sign), (Max as minmax), d1, s1), MinMax (c2, Minus, Max, d2, s2)
    | MinMax (c1, (Plus as sign), (Min as minmax), d1, s1), MinMax (c2, Plus, Min, d2, s2)
      when Symb.Symbol.equal s1 s2 ->
        let v1 = Sign.eval_big_int sign c1 d1 in
        let v2 = Sign.eval_big_int sign c2 d2 in
        let c = Z.min c1 c2 in
        let v = MinMax.eval_big_int minmax v1 v2 in
        let d = Sign.eval_neg_if_minus sign Z.(v - c) in
        mk_MinMax (c, sign, minmax, d, s1)
    | b1, b2 ->
        otherwise b1 b2
```

### Transfer-related instruction

Itv.t 定义了一系列的二元运算操作，节选如下：

```ocaml
val div : t -> t -> t

val div_const : t -> Z.t -> t

val minus : t -> t -> t

val mult : t -> t -> t

val mult_const : t -> Z.t -> t

val plus : t -> t -> t

val shiftlt : t -> t -> t

val shiftrt : t -> t -> t
```

以 plus 为例，其底层调用的还是 Bound 相关的 API：

```ocaml
let plus : t -> t -> t =
 fun (l1, u1) (l2, u2) -> (Bound.plus_l ~weak:false l1 l2, Bound.plus_u ~weak:false u1 u2)
```

最后，分享一个有意思的 [patch](https://github.com/facebook/infer/pull/1736)，可以帮助理解即使是在区间域的情况下，考虑到对性能的取舍，还是会在运算中存在丢失精度（对比 Linear 和 MinMax）的情况。

## 参考链接

[^inferbo_issues]: https://fbinfer.com/docs/all-issue-types#integer_overflow_l1
[^inferbo_test]: https://github.com/facebook/infer/tree/main/infer/tests/codetoanalyze/c/bufferoverrun