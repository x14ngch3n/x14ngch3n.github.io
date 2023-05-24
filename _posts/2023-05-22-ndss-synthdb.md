---
title: SynthDB Synthesizing Database via Program Analysis for Security Testing of Web Applications
category: [Research, Software Security]
tags: [program analysis, concolic execution, paper reading]
---

> 最近在面试中遇到过很多针对数据库代码的程序分析问题，也有面试官也指出过数据库是程序分析走向领域化的一个重要对象，所以也学习一篇关于使用数据库合成技术辅助 web 应用测试的工作。

背景介绍部分，作者指出当前针对 web 程序**运行时产生代码**的特点，更多的时候需要采用动态测试。而 web 后端代码的运行时行为非常依赖于 SQL 查询的结果，所以在测试这类代码时，我们需要尽可能地提供真实且足量的数据库条目，才能覆盖到更多的程序执行分支。但出于对于数据隐私的保护，想要获取商业公司中的真实数据用于测试是非常困难的。从而，研究者转而采用数据库合成（Database Synthesis）的技术，来向 web 测试框架提供合法且全面的数据库，辅助安全分析。且这样的数据库合成有以下 3 个限制：

1. 没有具体的输入
2. 没有初始的数据库
3. 没有 SQL 的查询记录

在合成数据库时，我们首先需要考虑的是数据库的设计方案（Schema），即显式关系。但如果考虑到处理这些查询的代码，其实还包含了一种数据之间的隐式关系。为此，作者总结出了一个良好的用于测试的数据库应该满足的 5 类约束：

1. schema constraints - for database integrity
2. query condition constraints
3. pre-query constraints
4. post-query constraints
5. synchronized_query constraints - define integrity and consistency rules between multiple database records

作者以 [SchoolMate](https://sourceforge.net/projects/schoolmate/files/SchoolMate/) 这一个 web 后台管理程序作为例子说明了合成数据库的难点。如下图所示，该代码片段中存在两处 SQL 注入和一处 XSS 注入点。如果想要触发这些漏洞，首先需要数据库中存在的数据满足代码进入 `while` 和 `switch` 语句。

![image.png](https://s2.loli.net/2023/05/23/3VeNZpUAzd46JQm.png)

作者首先使用了两类传统方法（都需要手动提供初始查询数据）生成数据库。首先是 Scheme-based 方法，由于其没有利用到程序输入（即手动提供的 POST 参数），导致 `q1` 的查询结果为空，无法进入主循环。随后演示了 Query-based 方法，即生成了和 POST 参数对应的数据库值，且关联列（比如 `courseid`）的对应随机值也相同，从而可以符合 `q2` 中包含的联合查询，但其 `dotw` 列的数据由于是随机生成的，还是不能够满足 swtich 语句所对应的 case。而如果使用本文的方法，即可以考虑到影响程序控制流的分支点（上图中1-4），生成能够覆盖造成漏洞的控制流的数据库内容。

![image-20230524113807286](https://s2.loli.net/2023/05/24/QMYVNpi1UARFOcE.png)

SynthDB 使用了混合符号执行的方法，其整体架构如下图所示。首先分析出每次查询所涉及到的数据列以及他们的关系，如果某一变量在后续的查询中被使用，则需要对其进行追踪，得到数据列的值的约束集合，并进行求解。SynthDB 使用了[Vulcan Logic Dumper](https://github.com/derickr/vld) 执行 php 代码，并将动态收集到的 5 类约束条件输入到 z3 求解器中。

![image-20230524151836200](https://s2.loli.net/2023/05/24/EAxdc6HNeYpkiw1.png)

从软件工程的角度，作者先测试了 SynthDB 在代码覆盖率上的表现。作者选取了 17 个真实的 PHP 程序，来自于之前测试得较多，且包含一定数量 SQL 查询的项目。作者还额外引入了 3 类 PHP 应用的最广泛的领域（CMS, eCommerce platform, and online forum）的主流项目。

![image-20230524162834814](https://s2.loli.net/2023/05/24/4onWrR1CTAvBbLg.png)

从结果来看，SynthDB 在取得了 63.9% 代码覆盖率和 77.1% 的查询语句覆盖率（能够返回合理结果且不报错）。经过对比分析，作者指出这源于其对于 post-query 的约束处理。

![image-20230524163924171](https://s2.loli.net/2023/05/24/rJce4oN6H5Railt.png)

随后，作者评估了使用 SynthDB 辅助漏洞扫描器 BurpSuite 进行安全测试的表现。作者用 BS 的自动测试模式对包含历史 CVE 的项目进行了测试并自动生成 payload。 如上图所示，在 SynthDB 合成的数据库的辅助下，能够达到最好的漏洞复现和挖掘新漏洞的效果。

![image-20230524170444567](C:\Users\10152\AppData\Roaming\Typora\typora-user-images\image-20230524170444567.png)

最后，作者还给出了 SynthDB 在先前的 Fuzzing 工作（Wfuzz 和 webFuzz）上的表现，主要体现为提高覆盖率。

## 参考链接

- https://www.ndss-symposium.org/wp-content/uploads/2023-632-paper.pdf