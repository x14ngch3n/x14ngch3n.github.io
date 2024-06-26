---
title: 2023 暑期实习投递/面试记录
category: [Misc, Internship]
tags: [program analysis, c/c++]
---

> 虽然之后准备读博士，但还是想体验一下程序分析的工业界情况（尤其是大厂）。实则能够提高码力，拓宽人脉，虚则能够美化简历，为自己的未来托个底。

从 3 月 10 日到 3 月 31 日，凭借之前通过各种活动/机会/微信群认识的 HR/业内大佬，我有选择性地先后投递了 x 家公司，~~没有错过金三银四的时机~~。为了从这些面试中吸取一些教训，也方便我之后跟进面试流程，选择 offer，我打算把它们记录下来。

以下的职位按照时间顺序记录：

## 上海安势信息科技有限公司

- 消息来源：静态程序分析技术交流群
- 时间跨度：3.10 - 3.22
- 目前进度：没发 offer

虽说是技术交流群，但里面竟然埋伏了不少 HR。不得不吐槽的是，这个公司发 JD 的时候都不说自己是什么公司，还是我靠邮箱后缀名找到的；还总是弄错我的姓氏，让我不得不在英文简历中加上中文名。

笔试是做 4 道 C++ 题目，2 小时完成。一开始我还以为会出一些程序分析场景相关的题目，结果看到题目发现就是非常简单的那种。不过最后电脑没电了，所以只做出来 3 道，也过了。

面试是公司技术负责人，C++开发部门负责人和一个高管一起面试，一共 2 小时。一上来，部门负责人（估计可能是未来的 mentor）先问了一些 C/C++ 和系统的知识，后面才知道这些都在面经上面有答案：

1. static 关键字的应用场景和作用？
2. 拷贝构造函数常见发生的场景？
3. 宏和内联函数的异同？
4. CPU 缓存中使用的是物理内存还是虚拟内存？

虽然没有背过面经，但我基本也都回答上来了，只是每个问题都需要反复地和面试官确认一些细节，不能像背答案一样回答得详细，完整又流畅。**然后才是最难的部分**，公司技术负责人张博士开始问我项目经历，并结合公司业务场景给出了一些静态分析的技术问题。项目经历方面：

1. 在蜚语实习的进度安排，一共写了几个 checker，它们的作用都是什么？代码量多少？能不能介绍其中一个 checker 的实现？
2. 在期智实习的工作结果？~~似乎没有什么，只敢说自己学习了 clang-tidy，所以很尴尬~~

技术方面：

1. 介绍一下编译器的工作流程？越详细越好
2. 介绍一下符号执行出现路径爆炸问题时的几种方案？
3. Clang 的 解析树（Parse Tree）知道吗？~~这玩意儿和 AST 不一样，我都没听说过~~
4. 介绍一下一个 LLVM IR Module 的组成部分？面试官说这是最基础的 LLVM 问题

业务方面：

1. 如何将在一个环境下能够成功编译的源代码和其包含的头文件，自动地移植到另一个环境中？除了使用 Docker 这样的方案
2. 静态分析时会引入大量头文件的代码，如何做到只分析源文件的代码？
3. 做上下文敏感分析和过程间分析时，需要将函数调用图和控制流图结合（笛卡尔积）起来，如何减少这一过程的内存占用？可以使用按需结合的方式

期间，还扯到了一些闲话。毕竟国内静态分析的圈子还比较小，做产品的公司目前都还处于融资 1-2 轮的阶段，这些公司的创始人之间几乎都认识。然后，另一位高管问了我之后的发展方向，说我如果要选择读博就得早做准备。张博士也送了我一句话：想要什么的人不是厉害的，不想要什么的人才厉害。其实这时候已经预感到面试会挂了。

最后，我问公司了公司两个问题：

1. 为什么从 SCA 转到 SAST？SCA 是主要产品，SAST 也在做
2. 为什么不考虑给 CSA 提 PR？公司不稀罕开源贡献，CSA 官方的代码不是工业级别的

总的来说，这次面试还是很有收获的，~~尤其是四个人同时面一个人，算是把压力测试和 HR 面也经历了~~。但毕竟小公司有自己的考量，而且这个社招岗位本来就是只招 1-2 个即战力，需要长时间（大于 3 个月）在岗的。过两天后，公司还是很友好地说明了不给 offer 的原因，我也加到了技术大佬张博士的微信，感觉不算亏。

## 上海那一科技有限公司（NaiveSystems）

- 消息来源：公众号 / 公司创始人微信 / 朋友圈推荐
- 时间跨度：3.31 - 4.21
- 目前进度：一面挂了
- <https://mp.weixin.qq.com/s/dUWnLraHJqALuJqRLJa4xw>

考虑那一主要是因为~~它离学校近~~从之前它们的实习生总结看来，在这里可以学到不少技术，而且带有一些学术性质，所以应该也可以和贾老板聊很多出国读博的事情。它们之前的产品也是基于 CSA 开发的静态分析工具，我还是比较有信心。

首先是做了一个离线的笔试，还比较考验综合水平，我也挺喜欢这样的笔试形式的。笔试给定了一个小项目，要求完成 4 个 commit，最终完成的结果打包为 [git bundle](https://x14ngch3n.github.io/assets/attachments/submission.bundle)：

1. 编写构建文件，使项目以及第三方库能够顺利编译
2. 根据文档，完成功能函数，通过给定的测试用例
3. 自己添加测试用例，注意 corner case
4. 发现初始代码中一个内存相关的 bug

花了 2 小时完成，不过也要吐槽一下它的自动判断脚本。它说可以支持 Mac 下开发，但自动脚本出现了头文件的报错，后续移植到 Linux 下才通过。

过了一个星期收到了一面通知，由于就在零号湾，我是直接前往线下面试的。刚进办公室就感受到贾老板强大的气场和简单高效的沟通方式。不同于之前介绍简历时大说特说，这次我几乎只花了 3 分钟就过了一遍简历，然后就开始了三道现场代码题。在手写白板代码（听说是 Google 企业文化）的过程中，贾老板会跟进提问，引导你回答，并设想代码可能出现的问题。

1. 写一个间隔删除链表节点的函数，直接使用双指针的思路即可。随后问如何测试，即需要测试链表长度为 0，1，2 时的情况，还有超长链表的性能情况
2. 写一个会导致死锁的程序。这个我回答得不太好：首先自己定义锁变量和 P/V 操作，随后我使用了书上的两个程序死锁的场景，但如何同时运行这两个程序，造成死锁也是个问题
3. 写一个有栈溢出的程序。我随手写了 scanf 和 strcpy 的两个版本，但似乎都不太满足他的要求。随后老板又把题目改成如何判断栈的增长顺序，我首先是使用局部变量的位置判断。结果老板说可能在编译器优化后局部变量会调换顺序。随后我又考虑使用栈帧的增长来判断，但也有可能 callee 被内联后再次发生局部变量优化的情况。总之最好的方法还是直接使用内联汇编。

整个面试花了将近 1 个小时，还是比较有收获的。其实白板写代码，也在考验我解决问题的思路，模拟了之后和同事讨论问题的场景。很多时候我还是有点草率了，在自己还没有把问题想清楚之前就想直接和对方交流，导致沟通效率不高。其次是我写代码的熟练度还是不够，贾老板问了和安势一样的问题：一周能写多少个 checker？我都只能支支吾吾地说 3-4 个，但从对方的反映看来，还是太少了，根本不符合公司快速迭代的要求。

最后我还问了一些关于公司的问题。比如为什么使用 MISRA C/C++ 规则，结果回答是客户（金主爸爸）要求。还有之前的科研 idea，是涉及到[编译器的 annotation 辅助静态分析的](https://b23.tv/G5tnm3l)，感觉这一块儿我可以再好好了解了解，看看现代编译器到底有多么智能。

吐槽一下，面试了一周还没有什么反馈。果然还是挂了，总体而言，虽然面试有所收获，但还是给人一种不太友好/尊重的感觉，可能崇尚技术的公司就是这样吧。

## 腾讯安全云鼎实验室

- 消息来源：SIG-程序分析
- 时间跨度：3.31 - 3.31
- 目前进度：简单沟通，估计没戏

也是群里发的广告，我就加微信了。值得吐槽的是我催了两次才有了电话面试的机会。其实也说不上面试，就是简单聊了 30 分钟。他问了我项目上的一些问题，尤其问了我对于 ChatGPT 挖漏洞的看法，是否能够取代传统的逻辑推理的方法。一个有意思的想法是，虽然 LLM 本质上是概率统计的模型，但有没有可能在 LLM 的涌现能力的驱动下，它也具备了逻辑能力。也就是说 ChatGPT 并不是像编译器一样去认识代码，而是像人脑神经元开发编译器的过程一样认识代码。我觉得这个想法很恐怖，也很符合我对 AI 的认识。

了解到他们目前用的比较多的工具是 CodeQL，之后想做一些用 LLM 做代码分析的尝试，然后可能更倾向于有深度学习背景的同学。然后说如果日常实习，名额还是比较多的。

## 阿里云安全 Web 组

- 消息来源：xdd
- 时间跨度：3.30 - 至今
- 目前进度：简历挂了
- <https://talent.alibaba.com/personal/campus-application>

打 XCTF Finals 的最后一晚上，听 xdd 介绍了阿里云安全内部的一些业务情况。当问到我的方向时，他就推了这个岗位。虽然是做 Web 侧（Java，Go）的代码扫描，但如果能学到技术，而且可以和这么多 0ops 的学长混，感觉也是很好的。

简单面试了，就主要问了简历上的事情以及一些引申的问题：

1. 如何看待 LLVM Pass？
2. 如何实现二进制软件成分分析的检测？如何获取第三方库的漏洞信息？
3. 讲一些常见的混淆的办法？
4. 常见的 Linux 下的系统安全机制（ASLR）？漏洞利用方法？
5. 你对于虚拟化安全有什么研究，Docker 和 Qemu？
6. 你在 0ops 打比赛一般都做什么样的题目？如果是 reverse 的话，你对于 VMP 和 UPX 加壳有研究吗？

和之前聊的不一样，这个人说他们还是做二进制的安全，结合一些云上的安全场景。至于之后的流程怎么跟进，他说如果感兴趣的话还是有可能强行捞简历的。

## 阿里云智能物联网安全组

- 消息来源：官网投递
- 时间跨度：3.30 - 4.11
- 目前进度：一面挂了
- <https://talent.alibaba.com/personal/campus-application>

自己在官网投递的被分配到了阿里云智能的物联网安全部，安排了带有笔试的一面。这个面试完全就是走过场，面试官态度很差。首先是约好的 3 点，结果 3 点才发链接，自己 3:10 才进入会议室，然后丢下题目就跑了。四个题目也没什么价值，甚至感觉都没想让我好好回答：

1. 描述 Java ReadObject 中的可能发生的漏洞及其原理，如何在没有回显的情况下判断是否存在？反序列化漏洞
2. 写一个大整数加法的函数，输入位两个字符数组，需要判断进位。
3. 用 python 实现全站数据爬取并打包上传。requests 和 bs4 库的利用
4. 用 shell 运行程序 100 次并将结果按序输出。`sort -rn`

简单地写完题目之后，又说开始电话面试。问了我对于漏洞挖掘的一些了解，尤其是之前的那个 CVE 的流程，还问我做过那些印象深刻的 CTF 二进制题目，还问了一些 web 防火墙的问题。最后谈到这个部门想要实习生做一些运维审计的工作，问我感不感兴趣。最后又问了一些无聊的面经，然后就结束了。一共 2 个小时，感觉毫无收获。后面才知道这一类就是 KPI 面，不必太过认真了。

## 阿里云安全系统安全组

- 消息来源：捞人
- 时间跨度：4.14 - 至今
- 目前进度：卡在系统里了

阿里的两个流程走完之后，阿里云安全的人直接通过简历联系到我了，说是之后用钉钉联系。但目前我在系统中被另一个部门捞起来了，所以暂时不能被他们把简历调过去。

后面阿里这边也一直没捞人，估计没戏了

## 腾讯 QQ 客户端安全

- 消息来源：官网投递
- 时间跨度：3.26 - 4.19
- 目前进度：二面挂了
- <https://join.qq.com/progress.html>

在官网随意投的，本来不抱希望，以为就是纯刷经验。面试之前了解了一下，大概和游戏安全差不多，都是偏重逆向。~~可惜没有仔细看看面经了~~

面试一开始就问了很多安全的问题：

1. 熟悉哪些混淆方式？ollvm 说一遍
2. 熟悉哪些指令集架构？ARM 和 X86 有什么不同？
3. 介绍一下 x86 函数调用的过程？
4. 对于 VMP 熟悉吗？介绍一下自己做过的逆向题
5. 介绍一下污点分析的流程？

回答得比较磕磕绊绊，主要还是因为自己平常做的逆向题太少了。企业面对的安全攻击，对抗强度是很大的，所以这样的岗位也会比较累。

然后换到另一个人，他说他们最近有用 LLVM 进行安全加固的项目，也会和科恩有交流。这一块儿我比较感兴趣，也和他聊得比较好。这才把面试流程推进下去。唯一不足的是这个岗位在深圳总部。

之后也看了看腾讯的[游戏安全技术竞赛](https://gslab.qq.com/html/competition/2022/index.htm)，有空可以尝试做一下。

收到二面通知了，估计还是问计算机原理相关的问题，听说会问一些网安业界的动态。

二面其实并没有问任何面经，但给我也带来了小小的一点震撼。有两个面试官，首先就是问到了你的代表作是什么，把你最拿得出手的东西讲一下？这让我瞬间不知道该说啥，只好说自己做的太杂了。面试官还说到，之前做的静态代码分析，其实都不算安全的问题，你有没有实际地自动化地分析过一些安全问题？我表示自己也只是做过题目，并没有挖过真实的漏洞或者是复现。总之，说明自己还是要提高安全实战技能，就算是企业用来提供安全能力的部门（比如静态分析，安全加固）也需要懂得攻击。最后，还问了我开发大型软件（而不是写插件）的经历，我把之前做过的 nand2tetris 完整地讲了一遍。不过面试官问到我自己在中间语言层有没有什么优化，我回答的还是栈式虚拟机加法到底层指令的优化。感觉自己在做这些 lab 的同时，也需要有自己的思考。而且不能总之拘泥于 lab，而是要往真实世界的大型代码看齐。

当然二面还问了许多技术无关的问题，比如自己期待的工作地点，工作部门（中台），实习时长等等。整个面试大约 40 分钟，感觉不算顺利。

果然不出所料，我二面挂了。还是要提高自己二进制的能力吧，多做一点漏洞复现。

## 腾讯 TEG 安全平台部

- 消息来源：官网捞人
- 时间跨度：5.13 - 6.2
- 目前进度：通过 HR 面，准备接 offer
- <https://join.qq.com/progress.html>

本以为腾讯已经没戏了，结果在过了将近一个月之后又被深圳的部门捞了起来。这次感觉对方是有备而捞，不仅允许了我更换面试时间，而且在我迟到后还专门打电话过来。

刚开场，面试官就直接介绍了部门情况，部门属于腾讯对内的代码审计的部门，会用到很多静态分析工具，主要职责是对内的代码质量保障。还介绍了他们的诉求：想要招一个可以长期实习，将来转正的实习生。然后对我的简历也初步看过了。面试官也非常爽快，直接免去了常规的面经环节和简历介绍环节，把一面问成了二面，他主要问了几个开放性的问题：

- 挖掘，利用，修复一个漏洞的全部流程？
- 有哪些静态分析算法，可以分为哪几大类？详细说一下数据流分析算法的工作原理？
- 在蜚语实习期间的工作流程是什么？
- 了解 GPT 和 Transformer 模型吗？

还问了一些业务场景下的问题：

- 在使用现有的静态分析工具（例如 CSA）时经常会遇到编译工具链版本/种类不支持，导致无法开展分析，如何做？其实是在问对 robust parsing 这样一个领域的了解，以及 IR 设计的一些基本功
- 在使用静态分析工具时，缺少代码的依赖库，无法编译的时候怎么办？

最后问了一些个人情况相关的：

- 有没有发过论文？
- 将来打算读博还是工作？说到做静态分析，最重要的在于数据（也就是被分析的代码，也强调了数据库代码），企业级别的代码量大，能做出更好的成果。小公司的分析对象常常是更小的工作，其写出来的代码本身没有什么价值（甚至是抄的）

我也问了一些问题：

- 会用 coverity 这样的工具吗？其实它已经断供了。但得到的答案几乎是一样的，这些工具几乎都用过，但主要还是看你的目的
- 日常工作是代码审计多还是工具开发多？作为公司擦屁股的部门，主要是审计其他部门反馈的误报

二面的节奏也很快，面试官也主要问了一些开放性的问题：

1. 如何看待 ChatGPT 在静态分析上的使用？
2. 你用过哪些静态分析工具，有商业的工具吗？
3. 对比分析一下你是用过的这些工具，他们分别适用于哪些场景？
4. 平常有追踪前沿漏洞（尤其是大型软件的）的习惯吗？
5. 为什么不选择挖漏洞的工作？

这次面试官也答应得很爽快，说让我直接准备好下一轮。

三面的目的性不太一样了，面试官已经通过前两轮面试知道了我的背景情况，三面他主要是考察我的一个工作模式。首先面试官就问到了我目前的科研模式，如何和导师沟通，讨论科研 idea。随后面试官也介绍到了，在企业的商业逻辑中，技术、工具本身不是最重要的，能够用多少的成本来解决问题才是重要的。尤其是在安全部门，主要职责就在于如何减少问题，是保安的角色。最后，面试官还是问了 ChatGPT 相关的应用前景。

三面也很顺利，直接在第二天就进入了 HR 面。由于我的学生工作经历和类似的交流经验比较丰富，所以 HR 面对于我来说就是纯聊了。先后问了：

- 有哪些你想要达到的目标，并最终完成的经历
- 有哪些你和老师/同学发生分歧并解决的经历
- 有哪些遇到的挫折
- 有哪些压力比较大的时候

但还有以下几个关键问题：

- 工作地点在深圳，面试官问到如果同时获得了华为 offer，你会怎么选择
- 入职时间比较晚，到时候看情况是否延期实习生考核

最后还加了一轮面试，虽然是说由交叉部门的员工来进行联合面试，但从对方的身份上看来，更像是未来的产品经理想提前和我聊一聊。她主要问了我在过去的静态分析中所报告的一些结果和反馈流程，尤其想要知道一个精确的检测率。说明这对于业务来说是非常关键的了。她也给我灌输了很多业务向程序分析的价值观，即主要还是为了企业代码服务。

终于收获一个 offer 了，如果是对于找工作的同学来说的话，这样有稳定转正机会的实习真是非常好了。

## 华为云核心网产品线

- 消息来源：HR 微信
- 时间跨度：4.3 - 至今
- 目前进度：通过主管面
- <https://career.huawei.com/reccampportal/portal5/user-index.html>

~~华为 HR 真多~~，先后和无线网络产品线和云核产品线，一共 4 个 HR 联系过。虽然无线网络产品是华为的老本行，待遇更好。但我是奔着技术去的，还是觉得云核更合适一些。

和云核的白盒分析团队的聊了，他们也是主要做自动化安全能力，目前用到了 clang-tidy 和其他一些自研工具。

[华为的笔试形式](https://mp.weixin.qq.com/s/nK7Y7Gz_SPaoa1aKLiopTA)是根据职位来定的，通用软件开发对应编程题，而网络安全对应选择题。稳妥起见，还是做选择题好了。今年换了笔试的系统，所以进度慢一点，不过华为这边都会派 HR 跟进每个人的进度。

选择了网络安全（二进制方向）的笔试，时长一个小时，一共 30 道单选(2') + 10 道多选(4')，60 分即可通过。大多数题目都是根据经验做出判断，也会有少部分的细节知识点，总是都不太需要逻辑，其实很快就可以做完。这次的题目比之前知识覆盖面更广，比如：Windows 下 this 指针保存在哪个寄存器？AES-192 的加密轮数？而有些题目是我几乎没接触过的，但其实只要拿出做选择题的技巧和一点点的推理就可以得到答案，比如对于测信道的判断，对于 SQL 注入的防护方法？总之感觉这类题目没啥准备的好方法，平常多积累吧。

笔试之后是综合测评，和其他公司的类似，然后就是面试，上研所的面试预计要到 5.20 - 5.25 了。

综合测评真无聊，还让我做了两次。总之就是要符合愿意团队合作，踏实干活的风格。面试安排在了 5.25 线下面试，技术面和主管面同一天完成。我本来想换个时间，结果他说是专门给我安排了一个网络安全岗位的面试官。

多番沟通后决定还是线上面试了。技术面仍然考察了一道算法题（字符串找最长不重复子串的长度）。我花 5 分钟写了一个很简单的实现，随后按照面试官的暗示写了一些测试样例便结束了。随后，面试官也没有问常规的面经，而是问了简历的东西以及静态分析的工具的问题：

1. 用过哪些静态分析工具？主要是分析哪些语言？
2. 你在选择静态分析工具的时候会考虑哪些方面？Clang-tidy 和 CSA 有什么不同？
3. 用过 CodeQL 吗？写过查询语句吗？了解其原理吗？
4. 考虑到我有二进制的能力，问到有过哪些真实软件漏洞挖掘 / 复现的经历？

二面是主管面，几乎还是一样的问题，重点问了我设计 checker 的过程和学习 CTF 的过程。然后我也问了他们部门主要分析的代码对象和是否有形式化分析协议的工作（没有）。

完成二面后，就准备继续泡池子了，据说是 1-2 周会有录取结果。华为这边也基本有 offer 了，听说是 mentor 特意要招的，说明还是我的简历打动人了。

## 字节跳动无恒实验室

- 消息来源：jd 学长
- 没有 HC

## 蚂蚁集团 CTO 线基础安全部

- 消息来源：官网投递
- 时间跨度：3.26 - 至今
- 目前进度：一志愿简历挂，二志愿三面挂了
- <https://talent.antgroup.com/personal/campus-application>

一志愿是[天穹实验室](https://github.com/antgroup-arclab)，专门挖漏洞的，自己这方面的背景还是不够硬。

二志愿分配到了 CTO 线的基础安全部，进行了 1 个小时的简单电话面试，主要是聊一聊，没有问面经。

首先还是介绍了自己关于程序分析的两个项目，面试官对于 CSA 内存建模以及 use-after-move 的检测方式都表示很感兴趣。随后就开始聊一些程序分析工程实现上的问题，比如在遇到大规模代码时内存建模非常消耗资源，这时候可以采用反向数据流分析的方式，来追溯缓冲区的长度，目前最出色的商业静态分析工具 coverity 已经实现了这样的功能，但有时候误报也很高。看来我还是要更熟悉 CSA 的检测机制，把一个静态分析模型吃透。

终于面试官提到了他们部门的工作，是对接自研数据库 oceanbase 的业务安全，负责分析 C++ 代码并将问题反馈给对应的开发者，不需要写利用。这个部门分析主要依赖的是 coverity，感觉如果有接触商业工具的机会也不错。我顺便问了问为什么不像 PingCAP 一样使用内存安全的 Rust，结果面试官说那边照样有很多 unsafe 导致的问题。

随后聊到了该部门 fuzz 相关的工作，类似于 squirrel 这篇论文，目前主流的针对数据库 fuzz 的方式就是需要自己定义一套 SQL 语句的中间语言，实现对应的前端，并在此之上做变异。首先，面试官要我描述自己涉及一个 IR 的过程。虽然不了解 SQL 引擎的实现，但我就按照 LLVM IR 的设计逻辑来答了。然后，面试官问我有没有写过 bison，我表示自己玩过 antlr4，感觉功能差不多。面试官还问了自己有没有上手修改过 AFL 源码，我说没有，之后他也没继续问下去了。

最后我问了几个问题，比如 oceanbase 使用的 C++ 开发风格（C++11，少量 C++14，自己实现 STL）。总体感觉是负责业务安全的部门，面试官也是像办法采用各种安全手段来保障。而且如果可以和开发者对接的话，应该是可以提高很多开发经验的。

好久没有消息，突然打电话来，完成了 30 分钟的二面。感觉对方比较随意，希望不是 kpi 面吧。上来还是先问了白盒静态分析的东西，但也没问很多细节。然后就是问我了不了解一些相关领域（程序分析，汇编，堆溢出，网络通信，加密算法）然后对应地问一下面经（常见的分析算法，C/C++下面的漏洞类型，32/64位调用约定，UAF原理，TLS握手过程，PKI认证体系）的问题，看来我还是要真的背一点面经了。在面试官问到污点分析的算法时，我按照前段时间看的论文[《All You Ever Wanted to Know About Dynamic Taint Analysis and Forward Symbolic Execution》](https://oaklandsok.github.io/papers/schwartz2010.pdf)进行了详细的回答。之后还是被问到了最有成就感的事情是什么，我回答了自己自学的过程。然后还被面试官问到自己大四到现在以来的学习历程，我还是不得不提到了辅导员的这些事情。最后再确认了一下部门的业务方向：主要做白盒分析，但也有二进制。

过了一段时间和我约了三面，整个时间大约40分钟。最后一轮技术面就没有问面经了，而是问了我对于具体的业务场景和自己的一些经历，和我之前看的[面经](https://juejin.cn/post/7079599610590658567)类似。根据我的经历，主要问了以下几个问题：

1. 说一下你现在的研究方向？
2. 你在打 ctf 过程中都取得了哪些奖项，做了哪些贡献？
   1. 逆向时如何快速找到你要分析的函数？
   2. 逆过加壳的程序吗？逆过真实软件吗？
   3. 做过漏洞利用吗？有什么心得？
3. 说一下你之前实习时的工作？做过（大规模真实软件的）代码审计吗？
4. 给你一个大型项目，你会怎么开始对它进行程序分析？（很考验功底的一问

然后又结合业务场景问了一些问题，比如在静态分析业务逻辑相关（而不是 C/C++ 语言相关）的漏洞时，要使用什么样的思路？还让我以解码库为例进行说明。

最后，面试官还看到了我之前的面试经历，便问我这两年来有什么成长，感觉还是对我有点兴趣的。

查看官网，毫无征兆地挂了，可能还是自己的简历不够硬吧。

## 结语

2 个多月的面试终于到了结束的时候。总体来说，我准备得并不是很充分（没有做任何的编程题和面经），对于职位的选择很挑剔（只选择了程序分析相关的，共 10 个岗位）。最终收获了 2 个 offer，虽然不是业内顶级的团队，但也算符合我的预期了。至于是否要去实习，还是要看具体能够给我的毕设带来什么？会花费多少的时间成本？会给之后的科研生活，乃至之后的职业选择带来什么影响？这都是很现实的问题，慢慢学着用更加成熟的眼光来考虑问题吧。

想起一个有意思的段子：如果我真有一头牛，我宁愿捐一个亿（手动狗头）。真的要放弃的时候，反而在考虑沉没成本了。很多时候要坚持初心真的很难，下次做这种决定之前还是要有目标一点，别再走一步看一步了。