---
title: Tracer 源码阅读（5）
category: [Research, Software Security]
tags: [program analysis, code reading]
math: true
---

> 为了记录自己读代码的过程，开设 Tracer 源码阅读系列博客。该系列博客以 ACM CCS 22' Tracer 的源代码为分析对象，旨在理解论文思路和复现论文结果，为后续在未初始化变量上的改进工作提供思路。

上文提到为了实现新的 checker，首先需要设计好抽象域。从 Tracer 的开发流程看来，大多数漏洞都是对 API 的使用进行建模，但这和（测试集中所展现的）最简单的未初始化场景之间还有一定的 gap。所幸 Infer 本身也实现了关于未初始化的 checker：uninit 和 pulse，本文尝试从上述两个 checker 的代码中总结出符合 Tracer 的抽象域设计。

思路有二：

- 找到 Infer 对于未初始化变量的建模
- 找到常见的未初始化变量涉及的 source-sink 函数

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

到此 uninit checker 介绍完毕，其大部分函数还是涉及到 C/C++ 对应 的 Hil 的处理。从 source-sink 对的角度看来，还是不够移植到 Tracer 提供的抽象域上。

## pulse checker

pulse 一共有 139 个文件，25K LoCs，使用的是 Sil。所由于代码较多，需要把目光聚焦于其对于建模的代码上以及和变量未初始化的相关代码上。

### PulseModelsXXX

这是一系列函数模型，和 Tracer 中定义的 dispatcher 逻辑一样（甚至可以猜测 Tracer 的灵感就是来自于这里），其入口逻辑在 PulseModels.ml 中定义：

```ocaml
module ProcNameDispatcher = struct
  let dispatch : (Tenv.t * Procname.t, model, arg_payload) ProcnameDispatcher.Call.dispatcher =
    ProcnameDispatcher.Call.make_dispatcher
      ( FbPulseModels.matchers @ PulseModelsCSharp.matchers
      @ PulseModelsObjC.transfer_ownership_matchers @ PulseModelsCpp.abort_matchers
      @ PulseModelsAndroid.matchers @ PulseModelsC.matchers @ PulseModelsCpp.matchers
      @ PulseModelsErlang.matchers @ PulseModelsGenericArrayBackedCollection.matchers
      @ PulseModelsHack.matchers @ PulseModelsJava.matchers @ PulseModelsObjC.matchers
      @ PulseModelsOptional.matchers @ PulseModelsSmartPointers.matchers @ PulseModelsLocks.matchers
      @ Basic.matchers )
end
```

可惜的是，在 PulseModelsC.ml 和 PulseModelsCp.ml 中都没有出现和未初始化直接相关的函数建模。

### Where to hold unintialized info?

我们换一个思路来研究，即通过分析 Infer 报告给出的 debug 结果中的字符串来搜寻代码。以最简单的未初始化变量为例：

```c
void self_assign_bad() {
  int x; 
  x = x; // PULSE_UNINITIALIZED_VALUE  `x` is read without initialization
  }
```

pulse checker 给出的错误报告如下：

```ascii
exec_instr n$0=*&x:int [line 17, column 7];
Executing instruction from disjunct #0
Checking validity of v1
  Abducing v1:MustBeValid(, None, t=1)
  Checking if v1 is initialized
  UNINITIALIZED
  Canonicalizing...
  
  Show/hide canonicalized state
  conditions: (empty) phi: (empty)
  { roots={ &x=v1 };
    mem  ={ };
    attrs={ v1 -> { Uninitialized(value) } };}
  PRE=[{ roots={ };
         mem  ={ };
         attrs={ };}]
  need_closure_specialization=false
  need_dynamic_type_specialization={ }
  skipped_calls={ }
  Topl={len=0;content=
         [  ]}

  Simplifying conditions: (empty) phi: (empty) wrt { } (keep), with prunables={ }
  Reachable vars: { }
  Reporting issue: Uninitialized Value:  `x` is read without initialization
  Got 1 disjunct back
```

由字符串查到了 PulseBaseDomain.ml 中相关的 pp 函数：

```ocaml
let pp fmt {heap; stack; attrs} =
  F.fprintf fmt "{@[<v1> roots=@[<hv>%a@];@;mem  =@[<hv>%a@];@;attrs=@[<hv>%a@];@]}" Stack.pp stack
    Memory.pp heap AddressAttributes.pp attrs
```

roots，mem 和 attrs 组成的三元组会负责记录未初始化的变量，这和 uninit checker 的 maybe_uninit_vars 是类似的。在 PulseAttribute.ml 找到了 Attribute.t 的定义，其包含了两个有关未初始化的 type，分别用于从正向/反向的思路来描述变量初始化的状态：

```ocaml
  type t =
    ...
    | Initialized
    ...
    | Uninitialized
  [@@deriving compare, equal, variants]
```

为了利用好这两个 type，该模块也定义了两个 helper functions：

```ocaml
(* 判断是否包含未初始化属性 *)
let is_uninitialized attrs =
  mem_by_rank Attribute.uninitialized_rank attrs
  && not (mem_by_rank Attribute.initialized_rank attrs)

(* 移除未初始化的属性 *)
let remove_uninitialized = remove_by_rank Attribute.uninitialized_rank
```

这两个函数在上层的 PulseBaseAddressAttibutes.ml 中被调用：

```ocaml
(* 检查当前 AbstractValue 是否为未初始化 *)
let check_initialized address attrs: AbstractValue.t -> t -> (unit, unit) result =
  L.d_printfln "Checking if %a is initialized" AbstractValue.pp address ;
  if Graph.find_opt address attrs |> Option.exists ~f:Attributes.is_uninitialized then (
    L.d_printfln ~color:Red "UNINITIALIZED" ;
    Error () )
  else Ok ()

(* 添加 Initialized 属性，移除 Uninitialized 属性，从而初始化该 AbstractValue *)
let initialize address memory =
  add_one address Initialized memory |> remove_attribute Attributes.remove_uninitialized address
```

在找到这些 helper functions 后，我们需要查看 pulse checker 在哪里调用了他们。值得一提的是，OCaml 的插件并不能直接找 reference，还是得通过字符串的形式。我们仍然从 source-sink 的角度出发：

### source: where is the unintialized attribute set?

- PulseModelsImport.ml：在 alloc_not_null_common 中，对分配的堆内存设置未初始化
- PulseAbductiveDomain.ml：在 realloc_pvar 中设置未初始化，其上层函数为 Pulse.ml 中的 exec_instr_aux，当分析到 VariableLifetimeBegins 类型的指令时调用

以上两个函数最后都是调用 AddressAttributes.set_uninitialized，代码如下：

```ocaml
let set_uninitialized tenv {PathContext.timestamp} src typ location astate =
  let src =
    match src with
    | `LocalDecl (pvar, v_opt) ->
        `LocalDecl (pvar, CanonValue.canon_opt' astate v_opt)
    | `Malloc v ->
        `Malloc (CanonValue.canon' astate v)
  in
  { astate with
    post= SafeAttributes.set_uninitialized_post tenv timestamp src typ location astate.post }
```

随后调用 SafeAttributes.set_uninitialized_post 函数来实际地设置未初始化的属性：

```ocaml
let rec set_uninitialized_post tenv timestamp src typ location ?(fields_prefix = RevList.empty)
        (post : PostDomain.t) =
      match typ.Typ.desc with
      | Tint _ | Tfloat _ | Tptr _ ->
          let {stack; attrs} = (post :> base_domain) in
          let stack, addr = add_edge_on_src timestamp src location stack in
          let attrs = BaseAddressAttributes.add_one addr Uninitialized attrs in
          PostDomain.update ~stack ~attrs post
      | Tstruct typ_name when UninitBlocklist.is_blocklisted_struct typ_name ->
          post
      | Tstruct (CUnion _) | Tstruct (CppClass {is_union= true}) ->
          (* Ignore union fields in the uninitialized checker *)
          post
      | Tstruct _ -> (
        match Typ.name typ |> Option.bind ~f:(Tenv.lookup tenv) with
        | None | Some {fields= [_]} ->
            (* Ignore single field structs: see D26146578 *)
            post
        | Some {fields} ->
            let stack, addr = add_edge_on_src timestamp src location (post :> base_domain).stack in
            let init = PostDomain.update ~stack post in
            List.fold fields ~init ~f:(fun (acc : PostDomain.t) (field, field_typ, _) ->
                if Fieldname.is_internal field || Fieldname.is_capture_field_in_cpp_lambda field
                then acc
                else
                  let field_addr = CanonValue.mk_fresh () in
                  let fields = RevList.cons field fields_prefix in
                  let history =
                    ValueHistory.singleton (StructFieldAddressCreated (fields, location, timestamp))
                  in
                  let heap =
                    BaseMemory.add_edge addr (MemoryAccess.FieldAccess field)
                      (downcast field_addr, history)
                      (acc :> base_domain).heap
                  in
                  PostDomain.update ~heap acc
                  |> set_uninitialized_post tenv timestamp (`Malloc field_addr) field_typ location
                       ~fields_prefix:fields ) )
      | Tarray _ | Tvoid | Tfun | TVar _ ->
          (* We ignore tricky types to mark uninitialized addresses. *)
          post
```

从直觉上看来，应该有其他地方也调用了这个函数，反向搜索后可以发现在 mk_initial 中才是完成了对于一般变量的未初始化属性的设置，该函数的核心逻辑如下：

```ocaml
  let post =
    List.fold proc_attrs.locals ~init:post
      ~f:(fun (acc : PostDomain.t) {ProcAttributes.name; typ; modify_in_block; is_constexpr} ->
        if modify_in_block || is_constexpr then acc
        else
          SafeAttributes.set_uninitialized_post tenv Timestamp.t0
            (`LocalDecl (Pvar.mk name proc_name, None))
            typ proc_attrs.loc acc )
```

先定义初始的 stack，heap 和 attrs，然后遍历局部变量，传入的指令类型为 LocalDecl，并设置未初始化属性。从打印的结果上看，测试代码中的未初始化属性都是在 mk_initial 中设置的

### propagate: how is the attribute propagate?

未初始化的属性只涉及单向的传播，即从 uninitialized 到 initialize

- PulseAbductiveDomain.ml：apply_unknown_effect 中会调用 BaseAddressAttributes.initialize，该函数的上层函数如下，用于支持过程间分析：
  - PulseCallOperations.ml
  - PulseInteproc.ml
- PulseOperations.ml：check_addr_access 在写入变量时添加 Initialized 属性
- ...

### sink: when is the attribute check?

在使用变量时，需要检查其是否已经被初始化了

- PulseInterproc.ml: 当遇到 MustBeInitialized 检查的时候
- PulseOperations.ml：当需要读取某个地址的变量时

### report

在 PulseDiagnostic.ml 中设置了 ReadUninitializedValue of read_uninitialized_value 的类型，最后在 get_message_and_suggestion 中给出报告内容。