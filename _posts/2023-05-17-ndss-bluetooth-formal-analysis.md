---
title: Extrapolating Formal Analysis to Uncover Attacks in Bluetooth Passkey Entry Pairing
category: [Research, Software Security]
tags: [formal method, paper reading]
---

> 按照组会要求，最近阅读几篇来自 NDSS 2023 的文章，寻求程序分析技术在网络通信上的应用点，我按照 analysis 和 binary 两个关键词搜索出了三篇文章。

这是一篇使用形式化方法分析蓝牙协议中存在的安全问题的文章。具体而言，作者选择了在之前的研究中被较少分析到的蓝牙安全配对协议中的 Passkey Entry（PE）方法，对其交互流程和攻击场景进行建模，成功分析并复现出了 5 个协议安全问题，其中 2 个为新发现的安全问题。

![The protocol flow of PE pairing](https://s2.loli.net/2023/05/21/SHOAo2f3rZFhUmy.png)

首先，作者介绍 PE 配对的 4 个流程，如上图所示。包括认证方式协商（共同输入相同的 passkey，还是一方提示另一方输入），密钥交换（需要经过20轮），主密钥生成，密钥验证，最后得到一个用于后续加密的会话密钥。作者还介绍了本文使用的形式化建模工具 Tamarin Prover（TP），它接受一个经过建模（改写成 MSR 规则的集合）的加密协议以及某个安全属性（以一阶逻辑为表示形式）作为输入，（使用不同的启发式算法）判断该模型是否满足安全属性（该问题不可判定，所以 TP 最终不一定会停止）。

具体来说，一个 MSR 规则由 Premise（输入），Conclusion（输出） 和 Action（协议检查点） 组成，一些列的 MSR 规则作用在由变量组成的 Fact 上，形成了 TP 中的一个流程。TP 采用符号化执行，由 Lemma（给定的一个程序属性）来驱动，TP 的任务即是证明是否存在一条 trace 不满足这条属性，或者所有的模型执行都满足属性。此外，先前验证过的 Lemma 还可以用于辅助之后的验证，即 sub-proof。总体来说，其实 TP 的运行逻辑和数据流分析很类似，不过更加关注对于协议流程的抽象，而不是程序语句的抽象。

Tamarin 还是用了统一的威胁建模方法，即 Dolev Yao intruder 模型。该模型允许攻击者：

1. 获取所有公开信道上的信息
2. 有一定的密码学/数学计算能力，可以精心构造数据包
3. 重放/重定向数据包

之后便是对 PE 模型的正式分析了。首先，想要在没有预先准备的安全信道上构建一个理论上完全安全的信道是不可能的，但考虑到实际的蓝牙通信场景，攻击者的窃听能力也非常有限。作者首先对现有的 PE 模型的防护方案进行了分析，给出了 3 个已有的缓解措施，并解释了他们不够可靠的原因。

之后两章，作者详细地介绍了在协议分析中使用的术语，分析范围及威胁模型（增加了攻击者对恶意设备和受害设备的接触能力）。为了能够让形式化方法捕获到 PE 协议尽可能多的流程和细节，作者首先以 Method Confusion 攻击作为初始分析对象。如下图所示，该攻击可以对通信双方使用不同的配对方式（NC 和 PE）达到中间人攻击的效果。

![Illustration of the Method Confusion attack](https://s2.loli.net/2023/05/21/ONgFrT3iVlLYZxD.png)

经过 1700 行 Tamarin 代码的建模，作者对 PE 协议进行了全面的建模，发现了5个未发现的漏洞，分别给出了他们的 trace。其中 Group Guessing 攻击和 Ghost 攻击是两个新发现的漏洞，作者都分别给出了详细的 PoC 和攻击的可行性分析。

随后，作者分析造成这些漏洞的原因（例如不正当的用户操作），对他们进行 fix 后，再次使用之前的建模验证了 patch 的有效性。

![Summary of Uncovered Attacks](https://s2.loli.net/2023/05/21/R1r3Mtb86l2e5WT.png)

![Time cost for Tamarin to produce the attack traces for the discovering individual attacks in the vulnerable model](https://s2.loli.net/2023/05/21/dVgYuNJEjvFHyT8.png)

值得注意的是，在 Usenix Security 23 的录用论文中，也出现了 3 篇类似的形式化方法的文章，且其中有一篇就是针对了另一种蓝牙协议的配对方式。

![placeholder](https://s2.loli.net/2023/05/28/sL1cXdg8BCGHmIi.png)

最后码一个作者张悦老师的招生信息：<https://mp.weixin.qq.com/s/D44OYealPmQ2QG9UEvai0Q>

## 参考链接

* <https://www.ndss-symposium.org/ndss-paper/extrapolating-formal-analysis-to-uncover-attacks-in-bluetooth-passkey-entry-pairing/>
* <https://github.com/OSUSecLab/bluetooth-pairing-formal-verification>
