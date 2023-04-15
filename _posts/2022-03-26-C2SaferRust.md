---
title: Translating C to Safer Rust
category: [Research, PL]
tags: [program analysis, paper reading]
---

> GoSSIP推荐的来自程序语言领域subtitle: ACM OOPSLA 21的论文，讲述了C2Rust生成的带有unsafe标签的rust代码存在的安全问题，以及对其中raw pointer这一问题的解决方法。感觉rust是一门在程序分析和软件安全方面有发展前景的语言，趁着这个机会可以好好学一下rust，了解更多关于软件安全的概念。

## 前言

Rust通过ownership等检查机制，可以实现内存安全和线程安全，避免了C/C++中出现的许多问题。目前有很多主流的开源项目（Linux，Firefox，Android）的部分模块开始用rust重写，这个工作可以借助自动化的工具c2rust来完成。

## c2rust仍然存在安全问题

Rust程序员在使用unsafe机制的时候可能引入安全问题，但这一类代码（从crates.io上可以找到很多）不在文章的讨论范围之内。文章分析的是c2rust生成的代码存在的问题，首先需要c2rust生成代码的语料库。考虑到c2rust对c语言编译系统的适配性，作者选取了17个c语言的项目作为分析对象，如下图所示。值得关注的是，

* 生成的rust函数中大部分有unsafe标签
* 只有生成过程中引入的辅助函数才被标记为safe
* 所有从C程序中直接翻译过来的函数都被标记为unsafe，但实际上有些不是必要的

这个结果也很好理解，毕竟c2rust的作者也说到，他们的初步目的仅仅是syntax意义上的正确翻译。
![Screen Shot 2022-03-27 at 21.58.48.png](https://s2.loli.net/2022/03/27/fLvaqWz534nGeTo.png){: width="90%" height="90%" .mx-auto.d-block :}

随后，作者对于rust提出了五类unsafety的来源做了进一步的细化，经过一些增强的假设（比如内存分配函数都是safe的）后，映射到了几类feature：

* RawDeref：解引用一个raw pointer
* Global：读/写/引用一个mutable的全局/外部变量
* Union：读一个C风格的，无标签的Union
* Extern：调用一个程序外部的函数，比如malloc/free
...

针对这些feature，作者基于Rust High-level IR分析，将上述语料库进行了再次分类，发现最常见的问题是RawDeref，Global和Extern。随后，作者在function-level对这些feature又做了一次分析。每个受到影响的函数都可能包括几种问题，不过总结下来，作者选择主要分析RawDeref。

作者分析RawDeref问题主要有以下几个来源，大部分都可以通过rust的一些安全编程特性来缓解

* 程序提供的API中的公共签名
* 自定义的内存分配函数malloc
* 从C风格的`void *`转化过来
* 作为外部函数的参数/返回值
* C风格的数组/指针运算

为了对指针问题进一步分析，作者还根据来源的类型将指针分为了四类：

* Lifetime：可以sink到以下三类
* VoidPtr：`* const void` 或 `* mut void`类型
* ExternPtr：外部调用的返回值
* PtrArith：指针算术运算的结果

## 如何优化c2rust生成的代码

作者基于c2rust的翻译过程，实现了将raw pointer转化为rust中的safe reference的功能。转化的过程中需要ownership和lifetime的信息，所以作者选择了对于自定义Lifetime类型的指针进行优化。

## 感想

* 首先我尝试了自己搭建c2rust的环境，但从crates.io上下载的代码有问题。随后从Github拉取项目后，源码编译才成功。
* 尽管c2rust生成代码存在许多问题，在一篇论文里只需要关注一个主流的问题即可。
* 由于我没有rust基础，所以看不懂作者对于raw pointer问题的优化方案以及实现方法，但对于rust编译器的严格检查有了一些体会。
* PL方面的会议还是很考验语言功底的，如果不了解rust提供的指针类型以及rust的安全机制，是肯定看不懂这篇文章的。

## 参考链接

* 论文地址：<https://dl.acm.org/doi/10.1145/3485498>
* GoSSIP论文阅读笔记：<https://mp.weixin.qq.com/s/W-Qkg7eALuuqFUDSbM2euA>
* c2Rust：<https://c2rust.com>
