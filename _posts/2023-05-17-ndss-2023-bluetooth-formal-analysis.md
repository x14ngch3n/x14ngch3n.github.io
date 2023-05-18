---
title: Extrapolating Formal Analysis to Uncover Attacks in Bluetooth Passkey Entry Pairing
category: [Research, Software Security]
tags: [formal method, paper reading]
---

> 按照组会要求，最近阅读几篇来自 NDSS 2023 的文章，寻求程序分析技术在网络通信上的应用点，我按照 analysis 和 binary 两个关键词搜索出了三篇文章。

这是一篇使用形式化方法分析蓝牙协议中存在的安全问题的文章。具体而言，作者选择了在之前的研究中被较少分析到的蓝牙安全配对协议中的 Passkey Entry（PE）方法，对其交互流程和攻击场景进行建模，成功分析并复现出了 5 个协议安全问题，其中 2 个为新发现的安全问题。

首先，作者介绍 PE 配对的 4 个流程，包括认证方式协商（共同输入相同的 passkey，还是一方提示另一方输入），密钥交换（需要经过20轮），主密钥生成，密钥验证，最后得到一个用于后续加密的会话密钥。作者还介绍了本文使用的形式化建模工具 Tamarin Prover（TP），它接受一个经过建模（改写成 MSR 规则的集合）的加密协议以及某个安全属性（以一阶逻辑为表示形式）作为输入，（使用不同的启发式算法）判断该模型是否满足安全属性（该问题不可判定，所以 TP 最终不一定会停止）。

具体来说，一个 MSR 规则由 Premise（输入），Conclusion（输出） 和 Action（协议检查点） 组成，一些列的 MSR 规则作用在由变量组成的 Fact 上，形成了 TP 中的一个流程。TP 采用符号化执行，由 Lemma（给定的一个程序属性）来驱动，TP 的任务即是证明是否存在一条 trace 不满足这条属性，或者所有的模型执行都满足属性。此外，先前验证过的 Lemma 还可以用于辅助之后的验证，即 sub-proof。总体来说，其实 TP 的运行逻辑和数据流分析很类似，不过更加关注对于协议流程的抽象，而不是程序语句的抽象。

Tamarin 还是用了统一的威胁建模方法，即 Dolev Yao intruder 模型。该模型允许攻击者：

1. 获取所有公开信道上的信息
2. 有一定的密码学/数学计算能力，可以精心构造数据包
3. 重放/重定向数据包

之后便是对 PE 模型的正式分析了

码一个作者张悦老师的招生信息，感觉方向还比较对口：https://mp.weixin.qq.com/s/D44OYealPmQ2QG9UEvai0Q

## 参考链接

* https://www.ndss-symposium.org/ndss-paper/extrapolating-formal-analysis-to-uncover-attacks-in-bluetooth-passkey-entry-pairing/
* https://github.com/OSUSecLab/bluetooth-pairing-formal-verification
* 