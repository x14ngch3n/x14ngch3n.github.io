---
title: Goshawk tutorial for AsiaCCS 2023
category: [Research, Conference]
tag: [program analysis, c/c++]
---

> 感谢 GoSSIP，让我有了第一次线下参加国际会议的机会，在此我把投稿过程和参会准备前期的工作都记录下来。

GoSSIP 曾在 2022 年的 IEEE S&P 发表了文章《Goshawk: Hunting Memory Corruptions via Structure-Aware and Object-Centric Memory Operation Synopsis》[^paper]，当时还在实习的我可以说是见证了论文发表的后半过程。不同于大部分的顶会工作，Goshawk 在发表之后，还在不断地进化，体现在以下三个方面：

1. 技术层面：不断更新代码版本，增加用户自定义选项
2. 应用层面：不断用于挖掘新的代码项目，并发现了新的内存问题
3. 宣传层面：不断更新项目网站[^website]和 Github[^github]

借着 AsiaCCS 新增的 tutorial track 的机会，我们得以进一步推广我们的工具，并将这些新的变化展示给大家。我获得了作为讲者的机会，从 3 月 2 日开始，我又重新和 Goshawk 结缘。

## 投稿准备

首先，我再次复习了论文，借着帮助学弟跑项目的机会再次熟悉了代码，并总结出了最近一段时间 Goshawk 的变动。于是在 3 月 14 日，我们开始了第一次的脑洞讨论：如何让大家快速了解 Goshawk？如何在 90 分钟内让观众能够上手操作 Goshawk？在初步的讨论后，我开始拟定了大纲，学弟则继续挖掘 OpenWrt 项目中的漏洞。

## 写稿过程

首先我创建了一个仓库[^tutorial]用于存放 tutorial 相关的材料。中途有段时间由于在准备 CTF，在稿子写好大纲之后我就没动了。终于在 DDL（3 月 31 日）的前一周，我意识到要开始写了。其实写稿的过程很快，我复用了部分论文的说辞（例如 MOS 模型），大概花了 2-3 天的时间写好了初稿。令人高兴的是，老师并没有说要在初稿上有大的改动。只是最后的投稿者从两个学弟变成了 siqi ma 老师，我也第一次名义上成为了 GoSSIP 的成员。

## 办理护照

因为 AsiaCCS 2023 主办方是 USNW，有老师学术圈的熟人，所以我还是比较有信心投中的。所以在写稿的同时，我也办好了护照（反正之后要用的）。办护照总体来说还是很顺利，因为去得时间早，几乎没有排队，我也在一周后拿到了本子。

## 投稿过程

投稿过程有个小插曲：会议方打不开交大邮箱的附件，连续试了两次都是这样，尝试重新转发也不行。随后我就通过上传到 Google Drive 来传递，终于还是可以了。

## 中稿之后

中稿当然是很开心，但接下来就知道又有一堆会议相关的麻烦事了：

- [x] 注册会议：我之前用银联绑定的 Paypal 账号用不了，需要 VISA/Master Card 才能支付。先找我爸借了一个，然后自己也办理了中国银行的 VISA
- [x] 预定酒店：直接预定了会议推荐的希尔顿酒店
- [x] 预定机票：据说是要订中国的航空公司，机票越早订越好
- [x] 获得邀请函：最关键的事情，需要在填写 VISA invitation letter 后，找主办方要邀请函
- [ ] 填写学校的手续：需要和导师沟通，填好几个表，也涉及到后续的报销手续
- [ ] 办理签证：旅游签和学生签很容易被拒，还是走会议的官方渠道，申商务签

预计下来，整趟澳洲行的花销（澳元）为：

| 项目      | 单价 | 数量 | 总价 | 备注                          |
| --------- | ---- | ---- | ---- | ----------------------------- |
| 注册费    | 1400 | 1    | 1400 | Conference only               |
| 酒店      | 260  | 5    | 1300 | 希尔顿，如果太贵可以找 Airbnb |
| 飞机-去程 | 5389 | 1    | 5389 | 要到广州转机                  |
| 飞机-返程 | 4369 | 1    | 4369 |

## 参考链接

[^paper]: https://ieeexplore.ieee.org/document/9833613
[^website]: https://goshawk.code-analysis.org/
[^github]: https://github.com/Yunlongs/Goshawk
[^tutorial]: https://github.com/cascades-sjtu/Goshawk-tutorial
