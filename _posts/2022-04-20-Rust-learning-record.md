---
title: Learning The Rust Programming Language
category: [course, Github]
tags: [rust]
mermaid: true
---

> 记录我学习Rust的过程

使用mermaid[^mermaid]生成的gantt图：

```mermaid
gantt
  title  Rust学习进度
  dateFormat YY-M-D
  阅读the book: active, p1, 2022-04-18, 4d
  练习rustlings: active, p2, 2022-04-18, 4d
  安装cwe_checker: p3, 2022-04-20, 1d
```

## 为什么选择Rust？

* 想对用Rust写的[cwe_checker](https://github.com/fkie-cad/cwe_checker)进行二次开发
* 学习更多有关内存安全的知识，也可以对应到C/C++中的一些程序分析方法
* 想学习一下现代编程语言的特点，也可以对应到C++的一些高级用法
* 了解函数式编程[^fp]

## 如何学习Rust？

感觉Rust的社区很活跃，学习资料也很多。我简单整理了一些如下：

* 书籍：
  * [The Rust Programming Language(the book)](https://github.com/rust-lang/book)：Rust官方书籍
  * [Rust语言圣经](https://course.rs)：Rust中文学习教程

* 练习：
  * [Rustlings](https://github.com/rust-lang/rustlings)：Small Rust exercises
  * [Rust by Example](https://doc.rust-lang.org/rust-by-example/index.html)：A collection of runnable Rust examples
  * [Rust语言实战](https://practice.rs/)：配套《Rust语言圣经》
  * [Rust培训](https://rustedu.com)：阿图教育，带着你学以上书籍

* 论坛：
  * [Rust语言中文社区](https://rustcc.cn)
  * [Rust语言开源杂志](https://github.com/RustMagazine)：月/季度杂志，包括了一些专栏

* 公众号：
  * 2121实验空间

* 项目：
  * [The Rust community’s crate registry](https://crates.io)：Codebases
  * [Rusty Book](https://rusty.rs/about.html)：Awesome Rust + Rust Cookbook

[^mermaid]: https://mermaid-js.github.io/mermaid/#/
[^fp]: https://zh.wikipedia.org/wiki/函数式编程
