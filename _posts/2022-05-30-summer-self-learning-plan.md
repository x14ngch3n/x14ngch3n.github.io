---
title: 2022暑期自学计划
category: [Misc, Learning]
tags: [plan]
---

> 勿在浮沙筑高台，想做出好的研究，提高CTF比赛的水平，还是要打好计算机基础

## 国外CS课程

打算从[CS自学指南](https://csdiy.wiki)上选取一些计算机基础课程和安全相关的课程来进行自学。学习方式主要为看slide，写lab+project，在学习的过程中定期记录到博客。目前打算进行自学的课程列表：

| 名称                         | 学校       | 博客                                                       | 时间                    |
| -------------------------- | -------- | -------------------------------------------------------- | --------------------- |
| [CS61A](https://cs61a.org) | UCB      | `./2022-05-30-summer-self-learning-plan.md`{: .filepath} | 2022.05.21-2022.07.08 |
| [rCore](https://learningos.github.io/rust-based-os-comp2022/) | Tsinghua      | `./2022-07-01-rust-based-os-comp2022.md`{: .filepath} | 2022.07.01-2022.07.30 |
| [CSAPP](https://github.com/cascades-sjtu/CS-APP)                      | CMU      |                                                          | 2022.06.09-2022.06.30 |
| CS106B/X/L                 | Stanford |                                                          | 2022.07.01-2022.08.01 |
| 6.S081                     | MIT      |                                                          | 2022.08.01-2022.09.01 |
| CS143                      | Stanford |                                                          | 2022.08.01-2022.09.01 |

预计还想学习 CS161，MIT 6.858 和 Seed-labs 这样的计算机安全课程

## CTF

从进入石楠花到现在，从简单的校赛到DEFCON Quals各种难度的比赛都算是见过了。目前自己的情况属于各种方向都了解一点，但都只能做简单的题目。嘴上虽然说自己是binary选手，但比赛中几乎没做出过re/pwn的题目。

如果只是把CTF当作兴趣，这样的状态倒也还好。但如果想打出成绩，真正体会到CTF大手子的乐趣，还是要专精于一个方向。结合我的研究方向，还是选择研究二进制方向的题目吧。首先还是复习一下各个架构的指令集（x86，ARM，MIPS，RISC-V），然后可以熟悉熟悉各类自动化漏洞挖掘工具（angr，z3）和逆向分析工具（Ghidra），最后就是看看有没有自己感兴趣的方向可以钻研一下，主要还是二进制的程序分析吧（IoT，WebAssembly，MacOS，LLVM）。目前打算进行自学的内容：

| 资源                     | 博客  | 时间  |
| ---------------------- | --- | --- |
| Reversing for everyone |     |     |
| 逆向工程权威指南               |     |     |
| decomposition          |     |     |
| Angr examples          |     |     |

## 科研

先从二进制分析的经典论文看起来吧，了解一下这个领域发展的来龙去脉。目前打算阅读的论文列表:

| 名称                                                                                           | 会议              | 年份   | 博客 |
| --------------------------------------------------------------------------------------------- | --------------- | ---- | ---- |
| KLEE: Unassisted and Automatic Generation of High-Coverage Tests for Complex Systems Programs | OSDI            | 2008 | |
| Arbiter: Bridging the Static and Dynamic Divide in Vulnerability Discovery on Binary Programs | Usenix Security | 2022 | |
| All You Ever Wanted to Know About Dynamic Taint Analysis and Forward Symbolic Execution       | IEEE S&P        | 2010 | |
| Program Vulnerability Repair via Inductive Inference                                          | ISSTA           | 2022 | |

## 简单总结

因为暑假的安排有变动，以上的自学计划（包括本博客）几乎完全烂尾了 😭

归根结底还是自己不够自律，自学的驱动力不够，详细原因我会在博客主页新增一个栏目 `weekly` 来总结，之后也会将定期的总结写到该栏目中。
