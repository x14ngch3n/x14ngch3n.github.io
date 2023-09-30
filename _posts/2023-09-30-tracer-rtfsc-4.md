---
title: Tracer 源码阅读（4）
category: [Research, Software Security]
tags: [program analysis, code reading]
math: true
---

> 为了记录自己读代码的过程，开设 Tracer 源码阅读系列博客。该系列博客以 ACM CCS 22' Tracer 的源代码为分析对象，旨在理解论文思路和复现论文结果，为后续在未初始化变量上的改进工作提供思路。

上文记录了对 IntOverflow 漏洞进行实例化的过程，在陆续查看了 CommandInjection 和 IntUnderflow 上实例化的过程后，本文尝试总结出为 Tracer 实现一个新的 checker 的方法。

## 前置条件

找到当前漏洞所涉及的 source-sink 函数

## APIMisuseChecker.ml

在 report 函数中添加对应的报告内容，该内容会显示在最后的 Trace 文件中：

```ocaml
| Dom.Cond.Exec c when Dom.Cond.is_user_input cond ->
    let ltr_set = TraceSet.make_err_trace c.traces |> Option.some in
    report_src_sink_pair cond ~ltr_set "Exec" ;
    Dom.CondSet.add (Dom.Cond.reported cond) condset
```

## APIMisuseDomain.ml

在 Cond 模块下添加对应的漏洞类型，Cond 模块会被作为 Summary 传播

```ocaml
module Cond = struct
  type t =
  ...
    | Exec of
        { user_input_elem: UserInput.Elem.t
        ; loc: Location.t
        ; traces: (TraceSet.t[@compare.ignore])
        ; reported: bool }
```

随后，分别为该模块的成员函数添加 Exec 的 match arm：

```ocaml
(* 设置 reported 属性，去除重复的 Cond *)
reported: Cond.t -> Cond.t
is_symbolic: Cond.t -> bool
get_location: Cond.t -> Location.t
is_reported: Cond.t -> bool
is_user_input: Cond.t -> bool
extract_user_input: Cond.t -> UserInput.Elem.t option
subst: Subst.subst -> Mem.t -> t -> t list
pp: F.formatter -> t -> unit
```

随后，需要对当前漏洞类型，在 Cond 和 CondSet 中设置构造函数，用于在之后生成报告内容

```ocaml
Module Cond = struct
  ...
  let make_exec {Val.traces} user_input_elem loc: Val.t -> UserInput.Elem.t -> Location.t -> t =
    Exec {user_input_elem; loc; traces; reported= false}
end

module CondSet = struct
  ...
  let make_exec (v : Val.t) loc =
    let user_input_list = UserInput.to_list v.user_input in
    List.fold user_input_list ~init:bottom ~f:(fun cs user_input_elem ->
        let traces =
            TraceSet.filter
            (fun tr ->
                match user_input_elem with
                | UserInput.Elem.Source (_, src_loc) ->
                    Trace.src_may_match src_loc tr
                | UserInput.Elem.Symbol _ ->
                    true)
            v.traces
        in
        add (Cond.make_exec {v with traces} user_input_elem loc) cs)
end
```

## APIMisuseModels.ml

在 dispatch 函数中，添加当前漏洞所涉及到的 source-sink 函数的签名：

```ocaml
let dispatch : Tenv.t -> Procname.t -> unit ProcnameDispatcher.Call.FuncArg.t list -> 'a =
  let open ProcnameDispatcher.Call in
  let char_typ = Typ.mk (Typ.Tint Typ.IChar) in
  let char_ptr = Typ.mk (Typ.Tptr (char_typ, Pk_pointer)) in
  make_dispatcher
    [ -"std" &:: "map" < any_typ &+...>:: "operator[]" $ capt_exp $+ capt_exp $--> StdMap.at
    ; -"std" &:: "map" < any_typ &+...>:: "map" $ capt_exp
      $+ capt_exp_of_typ (-"std" &:: "map")
      $--> StdMap.copy_constructor
    ; -"std" &:: "map" < any_typ &+...>:: "map" $ capt_exp $+? any_arg $+? any_arg $+? any_arg
      $--> StdMap.constructor
    ; -"std" &:: "basic_string" < any_typ &+...>:: "basic_string" $ capt_exp
      $+ capt_exp_of_prim_typ char_ptr $+ any_arg $--> BasicString.constructor
    ; -"std" &:: "basic_string" < any_typ &+...>:: "basic_string" $ capt_exp
      $+ capt_exp_of_typ (-"std" &:: "basic_string")
      $--> BasicString.copy_constructor
    ; -"std" &:: "basic_string" < any_typ &+...>:: "operator=" $ capt_exp $+ capt_exp
      $--> BasicString.assign
    ; -"std" &:: "basic_string" < any_typ &+...>:: "operator+=" $ capt_exp $+? any_arg $+? any_arg
      $--> BasicString.plus_equal
    ; -"std" &:: "basic_string" < any_typ &+ any_typ &+ any_typ >:: "basic_string" &::.*--> empty
    ; -"std" &:: "basic_string" < any_typ &+...>:: "basic_string" &::.*--> empty
    ; -"fread" <>$ capt_exp $+...$--> fread
    ; -"fgets" <>$ capt_exp $+...$--> fread
    ; -"malloc" <>$ capt_exp $--> malloc
    ; -"g_malloc" <>$ capt_exp $--> malloc
    ; -"__new_array" <>$ capt_exp $--> malloc
    ; -"realloc" <>$ capt_exp $+ capt_exp $+...$--> realloc
    ; -"calloc" <>$ capt_exp $+ capt_exp $+...$--> calloc
    ; -"printf" <>$ capt_exp $+...$--> printf
    ; -"sprintf" <>$ capt_exp $+ capt_exp $++$--> sprintf
    ; -"snprintf" <>$ capt_exp $+ capt_exp $+ capt_exp $++$--> snprintf
    ; -"vsprintf" <>$ capt_exp $+ capt_exp $++$--> sprintf
    ; -"vsnprintf" <>$ capt_exp $+ capt_exp $+ capt_exp $++$--> snprintf
    ; -"fprintf" <>$ capt_exp $+ capt_exp $--> fprintf
    ; -"getc" <>$ capt_exp $--> getc
    ; -"_IO_getc" <>$ capt_exp $--> getc
    ; -"getenv" <>$ capt_exp $--> getenv
    ; -"fgetc" <>$ capt_exp $--> getc
    ; -"strtok" <>$ capt_exp $+...$--> strtok
    ; -"strdup" <>$ capt_exp $--> strdup
    ; -"strcpy" <>$ capt_exp $+ capt_exp $+...$--> strcpy
    ; -"memcpy" <>$ capt_exp $+ capt_exp $+...$--> strcpy
    ; -"gnutls_x509_crt_get_subject_alt_name"
      <>$ capt_exp $+ capt_exp $+ capt_exp $+...$--> gnutls_x509_crt_get_subject_alt_name
    ; -"readdir" <>$ capt_exp $--> readdir
    ; -"getopt" <>$ capt_exp $+ capt_exp $+ capt_exp $+...$--> getopt
    ; -"atoi" <>$ capt_exp $--> atoi
    ; -"system" <>$ capt_exp $--> system
    ; -"execl" <>$ capt_exp $+...$--> system
    ; -"execv" <>$ capt_exp $+...$--> system
    ; -"execle" <>$ capt_exp $+...$--> system
    ; -"execve" <>$ capt_exp $+...$--> system
    ; -"execlp" <>$ capt_exp $+...$--> system
    ; -"execvp" <>$ capt_exp $+...$--> system
    ; -"__infer_print__" <>$ capt_exp $--> infer_print ]
```

为该签名实现对应的函数模型，即 exec / check 函数：

```ocaml
let system str =
  let check {location; bo_mem_opt} mem condset =
    let v = Sem.eval str location bo_mem_opt mem in
    let v_powloc = v |> Dom.Val.get_powloc in
    let user_input_val =
      Dom.PowLocWithIdx.fold
        (fun loc v -> Dom.Val.join v (Dom.Mem.find_on_demand loc mem))
        v_powloc Dom.Val.bottom
      |> Dom.Val.append_trace_elem (Trace.make_exec location)
    in
    Dom.CondSet.union (Dom.CondSet.make_exec user_input_val location) condset
  in
  {exec= empty_exec_fun; check}
```

以上述 check 函数为例，其逻辑为找到当前表达式（Exp.t 类型）所包含的污点信息，并添加到 trace 记录中

## APIMisuseTrace.ml

添加 Trace.elem 的类型和对应的构造函数

```ocaml
module Trace = struct
  type elem =
    | SymbolDecl of AbsLoc.Loc.t
    | Input of Procname.t * Location.t
    | Store of Exp.t * Exp.t * Location.t
    | Prune of Exp.t * Location.t
    | Call of Procname.t * Location.t
    | Malloc of Location.t
    | Printf of Location.t
    | Sprintf of Location.t
    | Exec of Location.t
  [@@deriving compare, yojson_of]

let make_exec loc = Exec loc
```

然后分别在 make_err_trace 和 pp 中添加对应的解析代码