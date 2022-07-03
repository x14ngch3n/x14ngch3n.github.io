---
title: 2022年开源操作系统训练营学习笔记
category: [course, website]
tags: [self-learning, rust]
---

> 之前一直就想完完整整地做一次操作系统的Lab，但值得学习的课程资料实在是太多了，经典的xv6，modern的OSTEP，包括IPADS的ChCore...不过借着清华这样一次开源操作系统训练营的机会，就从rCore开始吧，这篇博客用来记录我在训练营中的笔记

## 7.1 Day1

今天仔细看了本次训练营的大概内容[^schedule]，主要关注workload，目前看来代码量不是特别大，每天做一点的话应该是能完成的，关键在于要多提问题并记录在issue中

- 在学习实践过程记录表上登记自己每日/周学习记录情况的repo网址，并在这个repo上记录每日/周学习记录情况 (成绩分数：20%)
- 在第一阶段学习issues上的提问和回答问题情况，在第一阶段OS学习项目 、 rCore Tutorial v3的详细实验指导内容 上的Pull Request提交情况（代码改进、文档改进、文档错误等） (成绩分数：15%)
- step 0 要求的编程代码的完成情况 (成绩分数：15%)
- step 2 第一阶段OS学习项目的5个实验的完成情况 (成绩分数：50%)

- [^schedule]: https://github.com/LearningOS/rust-based-os-comp2022/blob/main/scheduling.md

## 7.2 Day2

今天进行了[第零章：实验环境配置](https://learningos.github.io/rust-based-os-comp2022/0setup-devel-env.html)的工作。其实我在之前就配置过 rCore 相关的 Qemu，riscv64-gnu 工具链和 Rust 开发环境了，所以很流畅地就把 hello world 给跑起来了。不过我也尝试了一下 Github classroom 的新功能，感觉还是挺有意思，可以通过 CI 的方式来提交作业。就是可能受到网速和云主机的影响，运行起来没有那么快，这也是 cloud editing 的一些通病吧。

最后决定还是使用本地开发了，明天开始看看 Rust 系统编程的资料，捡一捡 Rust 语言基础。