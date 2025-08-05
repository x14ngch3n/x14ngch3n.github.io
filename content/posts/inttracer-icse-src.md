+++
date = '2024-01-14T20:30:08+08:00'
title = "IntTracer for ICSE SRC '24"
tags = ['integer overflow', 'conference']
showTableOfContents = true
type = 'post'
+++

> 在前段时间针对Tracer文章的改进，整理了一下投稿到ICSE SRC 2024。这是我第一次完全独立且全程参与的文章投稿与录用，麻雀虽小（类似大摘要，只有2页），但五脏俱全（包括了几乎正式论文的所有流程）。在此我将投稿和参会准备工作都记录下来。

## 录用通知

按照官网通知的时间，录用通知在1/12前会发出，但我到了13号晚上一直没有收到邮件，HotCRP和会议官网没有更新。咨询了其他有经验的同学后，听说是不管录用与否都会有结果的，这种规模较小的track反而更有可能被committee放鸽子。于是在14号早上，当我看到会议官网的Notification DDL那一栏从绿变红了之后，我感觉可能是已经出结果了。于是马上从床上爬起来去查看HotCRP，发现了论文投递状态已经更新为Accepted。

![hotcrp](https://s2.loli.net/2024/01/18/lg6iyI5TbCR1Le7.png)

然后检查邮箱，发现也收到了录取通知的邮件。邮件里还附带了每位评委的评审意见和对于camera ready邮件的预告。

![camera-ready](https://s2.loli.net/2024/01/18/25VZts9p3zav1f4.png)

## 稿件准备

在收到录用通知后，第一时间就是需要根据审稿意见进行修改，保证好论文内容，并反馈修改结果给会议主办方。此外，还需要和出版社（例如ICSE的出版社为ACM，视具体的proceeding而定）进行邮件沟通，明确出版的规范。

虽然ICSE SRC采用的是单作者模式，但邮件内容中的很多说明都是针对多作者的。作为通讯作者，我们有义务将收到的每一封邮件都转发给合作者们。此外，如果投稿时自己为通讯作者，但论文需要设导师为通讯作者的话，请记得要在最后提交之前再在系统里设置成他为正式的通讯作者，不然所有的论文通知都会直接发给导师。导师如果忘记转发的话就可能造成麻烦了。

### 内容

以ICSE SRC为例，我一共收到了5份审稿意见（A，B，C，D，E），其中最后1份是对前面4份的总结。每份意见的格式如下：

- Overall merit：给出一个综合分数，例如3. Weak accept和2. Weak Reject，这个决定了最终的录用结果
- Reviewer expertise：审稿者的领域了解情况，例如Knowledgeable和Expert
- Paper summary：审稿者会对你的文章内容，按照自己的理解写一个summary，可以对比着看看自己的abstract是不是漏掉了什么内容
- Comments for authors：审稿意见本体，如果是偏向于Accept，一般会先讲缺点再讲优点。

可能是由于我这是第一次写稿，所以没提前估计好时间，导致最后实际的2页内容只用了从截稿当天早上8点到晚上8点的12个小时来写。在我的审稿意见中到处可见关于“presentation issue”的字样（包括但不限于typo和逻辑不顺），甚至被要求再做一遍proofreading，感觉真是低级错误。

应该给自己设置一个DDL，要把每次的会议截止日期的时间当作本地时间来完成，这样最后才能留有足够的时间来检查内容。

这次平均每个reviewer给了我10个修改意见，我一共花了3-4天的时间来修改。因为这次的录用流程不包括Rebuttal，所以你对于修改意见的反馈其实不再影响录用结果。但按照规范，最好还是能够在提交之后附上一个文档，记录针对每一条修改意见的修改说明（Responding Letter）。总结一下修改意见可以分为如下几类：

- Bigger Vision：SRC，以及类似的short paper类型的文章，都需要花一定的篇幅（比full paper中的比例更大）来讲述文章的整体愿景（对现实社会的影响），以及后续工作展望。注意这并不是用来水字数，而是要符合CFP的要求。
- 图文对应：由于我当天写的比较仓促，很多时候figure/table/listing和文字部分是没有对应起来的，会导致只看浮动体/文字的话无法理解。
- 逻辑衔接：如何用Introduction来引入到你的方案设计，即如何讲好这个故事。
- 术语使用：写论文不是写教科书，很多时候使用一些没有上下文的定义，会导致专家并不一定能反应过来。
- Typo：一些语法上的问题，多半集中在第三人称单数，复数形式，时态等方面

除了内容之外，这次我还有一个尴尬的地方在于**我在标题中发现了typo**，而且我是在提交了版权信息之后才发现的这个问题。为了不影响后续的提交，我马上联系了Committee chair，感谢Mattia的即使回复，我们用几乎一天一次的邮件频率解决了这个问题：即重新提交了版权信息，事实证明修改标题也并不会影响DOI号，但之后还是不要麻烦别人了。

最后，由于实验室项目和导师的“要求”，需要我加上致谢和基金号。对于full paper来说，致谢的部分在盲审时不会出现，在最终版提交的时候会可以自行加上。但由于SRC一开始就不是盲审，我额外在邮件中问了一下，得到的回答是“可以，但不能超过page limit”。

### 版权（Copyright）

版权方面，会收到来自rightsreview@acm.org的邮件（可能会多次重复发送）。当你的论文被录用时，论文的使用权被移交给出版社，这是在很多CallForPaper界面就已经说明了的，不过ACM还提供了两种不同权限的出版方式，如邮件里所说：

> - Exclusive Licensing Agreement: Authors choosing this option will retain copyright of their work while providing ACM with exclusive publishing rights.
> - Non-exclusive Permission Release: Authors who wish to retain all rights to their work must choose ACM's author-pays option, which allows for perpetual open access to their work through ACM's digital library. Choosing this option enables authors to display a Creative Commons License on their works.

第一种方式即将出版权交给ACM，由ACM按照自己的出版规则发布在网站上。第二种情况则可以理解为作者保留所有的论文权利，但由ACM负责托管到网站上公开发布，但需要额外花钱（会员700\$，非会员1000\$）。大部分人会采用前一种方案，对于专利有要求的会可能采用后一种方案。作为在校学生，学校一般都会购买ACM论文的数据库，所以我们在校园网内一般感受不到两者的区别。但对于社会人士，只对网站上开放了权限（Open Access）的论文可见。

此外，ACM还要求所有出版的作者提供ORCID，这是唯一标识每个作者的ID。在ORCID的网站上，作者还可以认领自己的所有论文，但这一步不是ACM要求的。

在做好上述准备工作后，需要填写邮件提供的链接问卷。在该问卷中需要保证以下字段和最终版本的论文PDF是严格匹配的：

- title
- author data, including the author order and each author's
  - name
  - affiliation
    - 即作者的单位
  - e-mail address

这些信息在论文PDF上都可以获取到，不需要额外准备，只需要检查即可。填写问卷的过程中会问你关于是否来自政府部门，是否接受会议录音、是否使用第三方材料、是否收到（美国）基金项目资助等问题，基本上按照默认回答即可。我顺便在提交问卷前注册了一个学生会员，一方面是可以在注册费上打折，另一方面就是可以减少不必要的麻烦。

在提交问卷后，会收到一个ACM提供的本论文的DOI号和会议的ISBN号等信息，需要补充到ACM模板的对应位置。其实在题目和作者已经确定的情况下，这部分工作和论文修改是可以完全并行的。注意这个DOI号暂时是无效的，需要等Proceedings正式出版后才会链接到相关网页。

### 出版（Camera Ready）

出版的邮件由IEEE的Lisa O'Conner发出（似乎其他的会议也是这位发的），相比于版权邮件需要提供更多关于论文本身的信息：

- page limitations
- paper formatting
- paper, source file, and copyright submission deadlines
- copyright release
- PDF eXpress for online file conversion / PDF Validation
  - PDF eXpress 是一个IEEE提供的用于编译LaTeX源码/验证PDF合法性的网站，作者需要先获取会议ID，并在该网站上提交自己的论文稿件并通过审核，获得论文编号。值得注意的是，这个网站并不负责论文提交，只保证论文PDF的正确性。
- paper submission (both PDF file and source file) - Your successful paper transmission will be notified with confirmation e-mail to the submitter. Please note that this Unique Paper ID MUST be included in the paper submission step of the Author Submission Site. This is the identification number of record for your ICSE Companion 2024 submission.
  - 论文最终版需要在Author Kit的网站上提交，一定要注意信息正确，需要附带submission number指PDF eXpress中给出的论文编号

同时也和版权的邮件来了一波联动，即最终的论文中是要包含正确的版权信息的。大多数版权信息已经由ACM的LaTeX模板自动填充了，只需要（从）复制一些引用信息即可。

> Copyright: ICSE 2024 and its associated publications are under ACM copyright. A separate email will be sent to complete the copyright process. You will need to complete copyright before completing final submission and include the copyright text with correct conference title, ISBN, DOI, etc. in your final PDF file.

在准备好上述信息后，需要填写IEEE提供的author kit Website上的问卷链接。最后，再次强调了要保证格式的规范性和符合要求，不然会有重新投递的风险。

由于我是第一次准备，故想参考一下往年的情况，这样看似“保险”的方案反而闹出了许多意想不到的问题。首先符合预期的是，从过去几年的Proceedings来看，SRC将会和Poster等Session一起出版在带有"Companion"后缀的论文集中。但让我百思不得其解的是，在查看2023年的Companion Proceedings时，发现所有的文章都是使用的IEEE的会议模板，而今年的要求确是ACM模板。本来出版这一块儿交给IEEE就搞的有点懵了，我就下意识地以为我需要在正式提交前转成IEEE模板。

这下问题可不简单了，因为SRC只要求2页，我肯定是要顶格写的。如果连论文模板都不确定，那我根本无法保证充分利用版面。好在感谢宣慧的提醒，我又看了去年的CFP，发现在提交的时候就是要求的IEEE会议模板。然后我又找去年录取了SRC的作者之一Wenjing Deng进行了确认，确实是我多虑了。还是按照邮件里给的要求按部就班地做就好，事实证明ACM版的论文是可以通过PDF eXpress验证的。

啰嗦两句。在我当负责人的时候，明明是很多按照官方流程做就可以搞定的事情，总有人会用各种理由，例如“去年就是这么做的”，“xxx也是这么做的”，“我和xxx说过了，这么做没问题”来给我的工作造成麻烦。当时我就觉得为什么有这么多想不按规矩办事的人，为什么可以问出这么多无厘头的问题出来。这次我反而成为了之前讨厌的那一种人。可能是事关毕业，几乎没有试错成本，我太怕出现失误了。不管怎么说，自己还是要先调研清楚，首先按照规矩来做。

## 参会（Competition）

在完成camera ready的提交之后，文章的准备工作就先告一段落，接下来需要准备的就是会议注册（以及相关的签证）。今年的ICSE在里斯本举办，一起举办的还有软工领域相关的会议（例如我比较感兴趣的“Klee Workshop on Symbolic Execution”）和Workshop（例如“Intl. Workshop on Search-Based and Fuzz Testing”）。此外，由于SRC属于Competition[^cfc]，提交论文仅仅是第一关，最终的比赛结果还需要经过第二关，即会议现场的Presentation和Poster来评定。如果表现得好，则可以获得对应的奖金，还可以晋级整个ACM的Student Research Competition。

[^cfc]: https://conf.researchr.org/track/icse-2024/icse-2024-SRC#Call-for-Contributions