---
title: Tracer 源码阅读（1）
category: [Research, Software Security]
tags: [program analysis, code reading]
---

> 为了记录自己读代码的过程，开设 Tracer 源码阅读系列博客。该系列博客以 ACM CCS 22' Tracer 的源代码为分析对象，旨在理解论文思路和复现论文结果，为后续在未初始化变量上的改进工作提供思路。

## 论文简介

Tracer[^paper] 是 ACM CCS 22' 上由韩国 KAIST 的研究者[^website]提出的关于利用静态分析检测 recurring vulnerability （反复出现的漏洞）的文章。

从技术上来说，Tracer 可以归类于代码相似性检测领域，但其采用了传统的静态分析方法，基于 Facebook Infer 的抽象解释框架来开发抽象化的污点分析检查器。

从方法上来说，Tracer 的思路很清楚，即提取 trace（污点类漏洞的传播路径），并转化为特征向量，再与历史 CVE 进行比对。

从结果上来说，Tracer 发现了通用 C/C++ 软件（debian 软件包）中的真实漏洞，包括整数溢出（上溢，下溢），缓冲区溢出，命令注入，格式化字符串 5 类，有着很高的安全应用价值。

## 环境搭建

废话少说，直接开始代码阅读，推荐在 Ubuntu-20.04 上进行。首先从仓库[^github]中拉取代码，直接使用 `build.sh` 安装 OCaml 开发环境（顺便学习一下 pushd/popd 的操作）。在了解了 Ocaml 的包管理器/编译工具链管理方法之后，再参考 [^cs3110] 搭建 VS Code 上的开发环境。如下图所示，搭建开发环境也为阅读代码提供了更好的代码提示，更加方便 OCaml 新手服用。且得益于 OCaml 注释即文档的特性，很多时候在 IDE 里面就可以快速了解第三方库的用法和库函数的签名（个人感觉了解 OCaml 代码中涉及的类型非常重要）。

![vscode](https://s2.loli.net/2023/06/01/nWH7PaOpmiDQYMX.png)

## 项目结构

Tracer 的顶层目录结构如下：

- `bin/`: Python 运行脚本，通过 sh 脚本来调用 infer
- `rank/`: 1.5k LoC OCaml 代码，用于对 infer 生成的 json 记录进行特征化处理和后续比较
- `signature-db`: 预先收集的 CVE 库，已经转化为 json 格式
- `test/`: 按照论文 showcase 的漏洞模式（整数溢出 -> 栈溢出）编写的测试代码
- `tracer-infer/`: 通过 `git submodule` 的方式引入经过二次开发（3k LoC OCaml 代码）的 infer[^tracer-infer]（基于 1.0.0 版本）

## Python 运行脚本分析

`bin/tracer` 是一个 Python 脚本，用于驱动整个 Tracer 的运行。该脚本支持两种运行模式：

1. `--debian`: 分析 debian 软件包，在作者提供的镜像 `prosyslab/bug-bench-base` 里进行编译该项目，进行分析
2. `--pacakge`: 分析本地项目，项目支持使用 `make` 编译

接下来重点分析 `run_tracer`。

## 参考链接

[^paper]: <https://prosys.kaist.ac.kr/publications/ccs22.pdf>
[^github]: <https://github.com/prosyslab/tracer>
[^website]: <https://prosys.kaist.ac.kr/tracer/>
[^cs3110]: <https://cs3110.github.io/textbook/chapters/preface/install.html>
[^tracer-infer]: <https://github.com/prosyslab/tracer-infer>
