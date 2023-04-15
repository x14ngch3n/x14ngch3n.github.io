---
title: Detecting Kernel Memory Leaks in Specialized Modules With Ownership Reasoning
category: [Research, System Security]
tags: [OS kernel, program analysis, paper reading]
---

> NIS-8018《系统安全前沿技术》的论文阅读作业，选取了漏洞检测领域的论文，了解一下Kernel的漏洞检测。作者实现了K-MELD的原型，使用了所有权（Ownership）机制对内核特定模块的内存泄漏进行了检测。作者在Linux内核中发现了218个bug，其中41个为CVE。

## 论文阅读

主要分析了Ownership机制中的逃逸者分析和消费者分析，并对论文的实验结果进行了分析。[报告Slides](https://cascades-sjtu.github.io/assets/slides/ndss21kernelleak.pdf)

## 论文复现

> K-MELD is also extendable to other OS kernels like FreeBSD.

文中提到K-MELD对其他的项目，尤其是OS项目也是有效果的，所以尝试分析一下FreeBSD。FreeBSD是Unix操作系统变种BSD系列之一（还有OpenBSD，NetBSD），可以在中科大的官网上找到镜像并通过虚拟机安装。

K-MELD接受LLVM bitcode形式的输入，所以需要先把大型项目编译成bitcode。官网给出的bitcode都是针对于单个文件的，而FreeBSD也没有现成的bitcode，所以需要使用`wllvm`来生成FreeBSD的bitcode，相关的教程见[tutorial-freeBSD](https://github.com/travitch/whole-program-llvm/blob/master/doc/tutorial-freeBSD.md)。

## 参考链接

* GoSSIP论文阅读笔记：<https://securitygossip.com/blog/2021/01/12/detecting-kernel-memory-leaks-in-specialized-modules-with-ownership-reasoning/>
