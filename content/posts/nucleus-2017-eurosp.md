+++
date = '2025-08-08T02:03:57+08:00'
draft = true
title = 'Nucleus 2017 Euro S&P Code Review'
tags = ['rtfsc', 'binary disassembly']
showTableOfContents = true
type = 'post'
+++

> 好久没有进行源码阅读了。但对于总是喜欢抽象思考的我，如果不真实调试源码的话，还是搞不懂很多自以为熟悉的算法。以这个反汇编为例，Necleus原文中的算法可能用几张图就可以概括，但现在要开始开发自己的Disassembler了，还是要学习一下代码实现。

## Overview

- 论文地址：https://ieeexplore.ieee.org/document/7961979
- 原代码仓库：https://bitbucket.org/vusec/nucleus
- 复现代码仓库：https://github.com/x14ngch3n/nucleus-py.git

整个项目包含了4218行C++代码，其中和论文创新点相关的部分大约有1000行代码（`cfg.cc/.h`）。项目整体依赖libbfd进行ELF加载（`loader.cc/.h`），依赖capstone进行反汇编（e.g. `nucleus_disasm_bb_x86.cc/.h`）。

对于反汇编，以及ICFG构建，到最后的函数识别中遇到的每个对象，项目都有单独的文件定义了一个对象。其中最核心的对象是`BB`，它不仅是ICFG的节点，通过`Edge`和其他BB关联起来，它同时也包含了内部的所有指令`Insn`，以及上层所属的`Function`和`Section`。整体的工作流程也是以`BB`的构建为阶段分界线。

## Stage 1: Recursive Disassembly

## Stage 2: ICFG Construction

## Stage 3: Function Identification

## Challenges

### Jump Table Analysis

### Indirect Call

## Conclusion

其实所有反汇编都是在选定一个