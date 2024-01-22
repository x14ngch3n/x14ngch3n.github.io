---
title: ICSE Student Research Competition 2024
category: [Research, Conference]
tag: [program analysis, c/c++]
---

> 在前端时间针对Tracer文章的改进，整理了一下投稿到ICSE SRC 2024。这是我第一次完全独立且全程参与的文章投稿与录用，麻雀虽小（类似大摘要，只有2页），但五脏俱全（包括了几乎正式论文的所有流程）。在此我将投稿和参会准备工作都记录下来。

## TODO：投稿过程

## 录用通知

按照官网通知的时间，录用通知在1/12前会发出，但我到了13号晚上一直没有收到邮件，HotCRP和会议官网没有更新。咨询了其他有经验的同学后，听说是不管录用与否都会有结果的，这种规模较小的track反而更有可能被committee放鸽子。于是在14号早上，当我看到会议官网的Notification DDL那一栏从绿变红了之后，我感觉可能是已经出结果了。于是马上从床上爬起来去查看HotCRP，发现了论文投递状态已经更新为Accepted。

![hotcrp](https://s2.loli.net/2024/01/18/lg6iyI5TbCR1Le7.png)

然后检查邮箱，发现也收到了录取通知的邮件。邮件里还附带了每位评委的评审意见和对于camera ready邮件的预告。

![camera-ready](https://s2.loli.net/2024/01/18/25VZts9p3zav1f4.png)

## 稿件准备

在收到录用通知后，第一时间就是需要根据审稿意见进行修改，保证好论文内容，并反馈修改结果给会议主办方。此外，还需要和出版社（例如ICSE的出版社为ACM，视具体的proceeding而定）进行邮件沟通，明确出版的规范。

虽然ICSE SRC采用的是单作者模式，但邮件内容中的很多说明都是针对多作者的。作为通讯作者，我们有义务将收到的每一封邮件都转发给合作者们。此外，如果投稿时自己为通讯作者，但论文需要设导师为通讯作者的话，请记得要在最后提交之前再在系统里设置成他为正式的通讯作者，不然所有的论文通知都会直接发给导师。导师如果忘记转发的话就可能造成麻烦了。

### TODO：内容

以ICSE SRC为例，我一共收到了5份审稿意见（A，B，C，D，E），其中最后1份是对前面4份的总结。每份意见的格式如下：

- Overall merit：给出一个综合分数，例如3. Weak accept和2. Weak Reject，这个决定了最终的录用结果
- Reviewer expertise：审稿者的领域了解情况，例如Knowledgeable和Expert
- Paper summary：审稿者会对你的文章内容，按照自己的理解写一个summary，可以对比着看看自己的abstract是不是漏掉了什么内容
- Comments for authors：审稿意见本体，如果是偏向于Accept，一般会先讲缺点再讲优点。

可能是由于我这是第一次写稿，所以没提前估计好时间，导致最后实际的2页内容只用了从截稿当天早上8点到晚上8点的12个小时来写。在我的审稿意见中到处可见关于“presentation issue”的字样（包括但不限于typo和逻辑不顺），甚至被要求再做一遍proofreading，感觉真是低级错误。

应该给自己设置一个DDL，要把每次的会议截止日期的时间当作本地时间来完成，这样最后才能留有足够的时间来检查内容。

### 版权

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

这些信息在论文PDF上都可以获取到，不需要额外准备，只需要检查即可。

### 出版

出版的邮件由IEEE的Lisa O'Conner发出（似乎其他的会议也是这位发的），相比于版权邮件需要提供更多关于论文本身的信息：

- page limitations
- paper formatting
- paper, source file, and copyright submission deadlines
- copyright release
- PDF eXpress for online file conversion/ PDF Validation
  - 这个是啥？
- paper submission (both PDF file and source file) - Your successful paper transmission will be notified with confirmation e-mail to the submitter. Please note that this Unique Paper ID MUST be included in the paper submission step of the Author Submission Site. This is the identification number of record for your ICSE Companion 2024 submission.
  - submission number指论文的投稿号，这在官网创建一个submission应用的时候就已经确定了 

也和版权的邮件来了一波联动。

> Copyright: ICSE 2024 and its associated publications are under ACM copyright. A separate email will be sent to complete the copyright process. You will need to complete copyright before completing final submission and include the copyright text with correct conference title, ISBN, DOI, etc. in your final PDF file.

在准备好上述信息后，需要填写IEEE提供的author kit Website上的问卷链接。最后，再次强调了要保证格式的规范性和符合camera ready的要求，不然会有重新投递的风险。