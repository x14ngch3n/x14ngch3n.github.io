---
title: 二进制漏洞检测工具 cwe_checker 学习
category: [tool, Rust]
tags: [binary analysis, rtfsc]
---

> cwe_checker是一个Rust编写的，利用Ghidra反汇编出的PCode，对ELF二进制文件进行程序分析的工具，目前已覆盖十余种CWE规则的检测。

## 安装与使用

和大多数的Github项目一样，[cwe_checker](https://github.com/fkiecad/cwe_checker)提供了本地安装和Docker两种方法。同时，它也作为核心组件被集成到了FACT_core[^fact]和EMBArk[^embark]等固件分析框架中。

### 本地安装

安装环境为Ubuntu-22.04的WSL，参考官方命令即可，需要手动安装`openjdk`才能使用headless版本的Ghidra。安装过程中会在根目录写入一些json配置文件，和CWE规则有关。安装完成后直接检测即可，命令如下：

```bash
sudo apt install openjdk-11-jdk
make all GHIDRA_PATH=/path/to/ghidra
cwe_checker /path/to/binary
```

### Docker安装

在AMD64/AArch64平台均可通过Docker安装，如果不安装对应架构的镜像会导致运行速度慢5-10倍，详细查看这个[PR](https://github.com/fkie-cad/cwe_checker/pull/321)。以M1 MBP为例，在命令行使用Docker的EntryPoint功能进行分析，参数如下：

```bash
# 我为cwe_checker构建的AArch64的镜像
docker pull cascadessjtu/cwe_checker
# --rm 为运行后删除容器，适合单次检测
# -v 为目录挂载，将主机目录对应到容器中的/tmp目录
# 将/tmp/cwe_190_arm_clang.out作为参数传递给entrypoint指定的cwe_checker，开始分析
docker run --rm -v /Users/chenxiang/Test/cwe_checker-0.5/test/artificial_samples/build:/tmp cascadessjtu/cwe_checker /tmp/cwe_190_arm_clang.out
```

### 集成到项目

FACT_core是FKIE-CAD和cwe_checker一起推出的项目。在FACT_core中，cwe_checker通过Docker安装。

EMBArk的核心分析功能由emba提供。emba是一个纯shell脚本写成的命令行工具，它集成了各类安全分析工具。在emba中，cwe_checker通过本地安装，安装脚本见[I120_cwe_checker.sh](https://github.com/e-m-b-a/emba/blob/master/installer/I120_cwe_checker.sh)。对比参考自动化脚本来分析自己本地安装出现的问题，是一个不错的debug思路。

## 功能分析

批量测试作者提供的[CWE测试集](https://github.com/fkie-cad/cwe_checker/tree/master/test)，也可以试试Juliet[^juliet]给出的CWE测试集。首先是需要构建编译二进制数据集需要的Docker镜像，再通过SCons这个构建工具得到各种编译器生成，各种架构下，各位CWE的二进制文件，命令如下：

```bash
make compile_test_files
# 如果上一步出现问题了，修改一下SCons的构建命令即可
docker run --rm -v $(pwd)/build:/home/cwe/artificial_samples/build cross_compiling sudo python3 -m SCons
make test
```

## 源码分析

## 扩展思路

* 参考nazz[^nazz]，添加PCode符号执行引擎，减少误报
* 添加其他CWE/安全编码规则(MISRA[^misra])，减少漏报
* 适配其他的二进制文件格式，比如RTOS
* 提高运行速度，参考星澜科技的BinCraft[^bincraft]项目合集

## 扩展阅读

[^fact]: https://github.com/fkie-cad/FACT_core
[^embark]: https://github.com/e-m-b-a/EMBArk
[^nazz]: https://github.com/borzacchiello/naaz
[^misra]: https://www.misra.org.uk
[^juliet]: https://samate.nist.gov/SRD/testsuite.php
[^bincraft]: https://github.com/StarCrossPortal/bincraft
