---
title: Tracer 源码阅读（1）
category: [Research, Software Security]
tags: [program analysis, code reading]
---

> 为了记录自己读代码的过程，开设 Tracer 源码阅读系列博客。该系列博客以 ACM CCS 22' Tracer 的源代码为分析对象，旨在理解论文思路和复现论文结果，为后续在未初始化变量上的改进工作提供思路。

Tracer[^paper] 是 ACM CCS 22' 上由韩国 KAIST 的研究者提出的关于利用静态分析检测 recurring vulnerability （即反复出现的漏洞）的文章。

从技术上来说，Tracer 可以归类于代码相似性检测领域，但其采用了传统的静态分析方法，基于 Facebook Infer 的抽象解释框架来开发[^github]抽象化的污点分析检查器。

从方法上来说，Tracer 的思路很清楚，即提取 trace（污点类漏洞的传播路径），并转化为特征向量，再与历史 CVE 进行比对。

从结果上来说，Tracer 发现了通用 C/C++ 软件（debian 软件包）中的真实漏洞，包括整数溢出（上溢，下溢），缓冲区溢出，命令注入，格式化字符串 5 类，有着很高的安全应用价值。

## 参考链接

[^paper]: https://prosys.kaist.ac.kr/publications/ccs22.pdf
[^github]: https://github.com/prosyslab/tracer
[^website]: https://prosys.kaist.ac.kr/tracer/
