---
title: 使用 Git 来管理 Microsoft Excel
category: [Misc, Git]
tags: [git, excel]
---

## 起因

众所周知，高校办公自动化的程度目前也仅限于使用Excel来处理各类数据，但难免遇到以下几个问题：

1. 数据量大的时候甚至打不开Excel文件
2. Excel和各种国产的表格软件之间存在不兼容的问题
3. 不方便进行版本管理，往往要在命名上花很多心思和管理的成本
4. 只能写一些简单的公式（会vlookup的就不错了），不方便做数据处理
5. 不方便做数据的统一备份

上述问题很难说用一种方案来解决，但我们可以选择优先解决在当前办公场景下成为工作效率瓶颈的那个问题。当遇到周期较长的工作，需要经常迭代时，版本管理和数据备份就成为了亟待解决的问题。

一个朴素的想法是通过Git来解决这两个问题。Excel主要的文件格式为`xls`和`xslx`，本质上是xml打包压缩后的文件，所以被Git当作二进制文件。Git默认只检测二进制文件的改动情况，并不会做细粒度的`diff`。所以最主要的目标就是找到可以处理Excel的diff工具。

Git仓库的备份服务器也需要仔细考虑。一是避免Github这样可能需要科学上网的服务器，二是减少账号注册等过程，三是可能需要提高仓库的保密性。可以通过Gitee+token+private的组合来完成。我选择自己尝试搭建一个服务器，也是增加运维经验。

此外，当Excel文件较大时，由于Git需要对每次commit都备份，可能会导致仓库尺寸过大。这时候也许需要使用[git-lfs](https://github.com/git-lfs/git-lfs)来缓存一些大的二进制文件，并延迟加载不同版本的二进制文件，具体原理可以看[^git-lfs]。

## 工具

### Diff

我首先发现了[git-xl](https://github.com/xlwings/git-xl)这样一个开源工具。但似乎效果一般，目前只能在Windows上运行，进行粗粒度的diff，而功能更全的版本则需要收费。

随后我又看到了[ExcelCompare](https://github.com/na-ka-na/ExcelCompare)。这个通过Java开发，跨平台的支持更好，也有细粒度的结果。此外，它还支持在diff的时候添加ignore的参数，来针对性地diff。但不方便的地方是只支持两个文件之间的比较，和`git diff`的命令格式有一些差距。

```console
excel_cmp <diff-flags> <file1> <file2> [--ignore1 <sheet-ignore-spec> ..] [--ignore2 <sheet-ignore-spec> ..]
```

最开始我想到的是手动checkout来切换版本，并导出为新的文件作为`excel_cmp`的输入。但在搜索issue后，我发现了更符合Git风格的做法[^issue]，背后的原理可以看[^git-diff]。简而言之就是将`excel_cmp`添加为xlsx文件的driver，当git工作时读取配置文件`~/.gitconfig`，便可以使用对应的工具来diff。而diff本质上也是签出对应版本的文件来进行比较，所以可以通过修改提供给diff的参数来符合`excel_cmp`的命令格式。

```console
# 查看与上一次commit的不同
git diff ^HEAD
# diff结果显示增加了一个cell，内容为test
EXTRA Cell in WB1 Sheet1!A6 => 'test'
----------------- DIFF -------------------
Sheets: []
Rows: []
Cols: []
----------------- EXTRA WB1 -------------------
Sheets: [Sheet1]
Rows: [6]
Cols: [A]
----------------- EXTRA WB2 -------------------
Sheets: []
Rows: []
Cols: []
-----------------------------------------
Excel files Book1.xlsx and /var/folders/yq/nx698dzs09s9td0pntdr3zqw0000gn/T/Bw04LD_Book1.xlsx differ
fatal: external diff died, stopping at Book1.xlsx
# 可以看出diff的时候是从之前commit中临时生成了新的文件
```

### Git Server

大多数内部网络都是使用Gitlab来搭建内部的Git server，我则找到了一个更轻量，方便使用Docker搭建的[gogs](https://github.com/gogs/gogs)。所有环境搭建工作都是一键完成，基本的功能也有。尤其是它提供了官方的Docker镜像，从而不怕影响到我的服务器本地环境。

![placeholder](https://s2.loli.net/2022/05/29/5SzPt1WNbvJRkTp.png)

## 流程

目前设想的工作流大致如下：

1. 处理表格前，先`git pull`
2. 本地通过Excel处理表格，`git push -u origin master`到服务器上统一的仓库
3. 管理人员定期处理PR，通过diff看改变情况
4. 在遇到问题时可以回滚到之前的版本

## 一些小坑

目前还没有正式实践，不知道会有什么问题，我目前想到的就这些：

* 要忽略掉Excel的临时文件，或者每次commit前关闭Excel
* 需要统一commit的格式[^commit]，不然不方便review

[^git-lfs]: https://zhuanlan.zhihu.com/p/146683392
[^issue]: https://github.com/na-ka-na/ExcelCompare/issues/30
[^git-diff]: https://programmaticallyspeaking.com/git-diffing-excel-files.html
[^commit]: https://cbea.ms/git-commit/
