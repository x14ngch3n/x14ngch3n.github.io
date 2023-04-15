---
title: GitHub Codespaces 使用体验
category: [Misc]
tags: [devops]
---

> 最近看到 GitHub主页又打出了 Codespaces 的广告，就想着来试试，看看和之前的 github.dev 相比有什么进步，是不是真的能用到日常的开发环境当中

随着云计算越来越火，**云开发**的概念也逐渐进入到开发者的视野中。从目前的发展来看，基于浏览器的云 IDE 是一个不错的解决方案，它甚至可以让你在 iPad 中连接到开发环境。GitHub 作为最大的开源社区，又加上有微软的算力加持，自然也不会落下这一趋势。如果能够直接将 repository 的某个 commit 绑定到某个开发环境（具体来说是一个容器），并使用浏览器就可以编写、部署代码，可以免去传统开发流程中的不少麻烦，甚至提供了一种全新的开发思路。而这，便是 [GitHub Codespaces](https://docs.github.com/en/codespaces/overview) 提供的功能。

## 基本使用

如果你使用过云服务器，那么可以无缝对接到 GitHub Codespaces 的使用，具体的使用可以看 [quickstart](https://docs.github.com/en/codespaces/getting-started/quickstart)。需要注意的两点是：

1. 可以直接用第三方的 repo 创建 Codespace，然后再选择是否创建自己的 repo，并将改动 push 到自己的 repo
2. 新创建的 Codespace 默认使用了你 VS Code 账号中设置了**同步**的插件，对于插件较多的小伙伴来说可能启动有些慢

但总体来说体验还是很顺畅的，不到一分钟就能创建好一个已经预置了许多编程语言环境的实例[^default]。实例的硬件规格（2核4G / 4核8G，Xeon Platinum）也足够跑一些小的项目，最重要的是连接 GitHub 和其他代码仓库的速度特！别！快！几乎可以达到 100MB/s，妈妈再也不用担心我卡在部署环境这一步了。个人账户最多可以拥有 10 个实例，还可以申请到 32 核 64G 和带有 GPU 的实例，~~可惜我目前还没申请到~~，微软真是大善人。

## 高级使用

### Dotfiles

对于一些基本的命令行工具安装，可以使用自定义的 [dotfiles](https://docs.github.com/en/codespaces/customizing-your-codespace/personalizing-github-codespaces-for-your-account#dotfiles) repo，让 Codespace 在创建时就自动地执行脚本。

### Codespaces secrets

对于一些不方便公开的密钥或 token，可以使用 [secrets](https://docs.github.com/en/codespaces/managing-codespaces-for-your-organization/managing-encrypted-secrets-for-your-repository-and-organization-for-github-codespaces)，将关键信息加密后以环境变量的方式传递给 Codespace。

### dev containers

虽然 GitHub Codespaces 提供了开箱即用的方式，但它的高级用法在于定制化地使用。你只需要在 repo 的 `.devcontainer` 目录下添加配置文件 `devcontainer.json`，就可以为每个项目定制 Codespace 环境[^devcontainer]，即所谓的 `Configuration as Code`。

GitHub 官方已经提供的一些开发框架的模板，对于前端和人工智能的开发者非常友好：

![official template](https://tva1.sinaimg.cn/large/008vxvgGgy1h8od7yphb6j31rm0u0dka.jpg)

GitHub 官方也演示了如何使用预定义的模板[为自己的项目定制 Codespace 环境](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/setting-up-your-project-for-codespaces)。其本质上是对 Dockerfile 的一层封装，加上了对于 VS Code 的一些配置选项。配置文件中一些常用字段的用法见文档[^jsondoc]。

除了上面的模板之外，其实微软官方在 VS Code 的插件中提供了针对更多语言的模板[^template]。在插件中搜索 `Codespaces: Add Dev Container Configuration Files...` 就可以使用模板，并添加到当前仓库的 `.devcontainer` 目录下。然后，可以根据自己的需求再修改字段内容，比如使用 `features`[^features]。最后，使用 `Codespaces: Rebuild Container` 重新构建当前的容器即可。

还有些更高级的操作，比如使用 [prebuilds](https://docs.github.com/en/codespaces/prebuilding-your-codespaces/about-github-codespaces-prebuilds) 来加速构建 Codespace 和使用 [template repo](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/setting-up-a-template-repository-for-github-codespaces) 来为其他人提供 Codespace 模板，我就先不玩了～

### 一个简单的 devcontainer.json 实例

对于常见的 Linux 下开发环境的搭建，我在 Ubuntu 的最小化实例上进行了简单的定制，配置文件见：<https://gist.github.com/cascades-sjtu/065ae8723702318b48f303e6e595c402>

## 原理

关于 Codespaces 的更多细节[^deepdive]，由于我不是相关方向的，有空再了解啦～

## 一些使用建议

- 在 <https://github.com/codespaces> 或 [VS Code GitHub Codespaces](https://marketplace.visualstudio.com/items?itemName=GitHub.codespaces) 中查看当前你使用的实例状态、连接实例
- 定期地连接实例，防止 GitHub 在你超过 30 天不使用后回收
- 定期查看 [Codespaces usage](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/viewing-your-github-codespaces-usage)，不要超出使用额度了
- 可以在 GitHub Setting 中默认修改为使用 VS Code desktop 来连接，保持主题的统一

## 目前遇到的一些坑

- 个人账户创建的实例是通过 GitHub 账号来验证的，Codespace 并不会提供公开访问的地址，而且禁用了对于网卡的访问，就连端口也是临时转发的，那么如何共用一个 Codespace 呢？必须要使用 Organization 的付费版本吗？
- 连接实例的速度较慢，即使已经选择了 South Asia 地区，但在终端敲命令时还是经常会感觉到到延迟。如果采用[端口转发](https://docs.github.com/en/codespaces/developing-in-codespaces/forwarding-ports-in-your-codespace)来测试某些前端页面的话，则需要等待更长时间
- 虽然说是免费，但每个月的使用还是有限的[^billing]。对于 GitHub Pro 账户来说，Codespaces 的使用额度是`180 core-hours/month`，所以不是说选择配置越高的实例就越好
- 使用默认的模板会导致占用系统空间较多，对于 32GB 的 Codespace 来说有点吃不消，也不符合最小化部署的原则

## 扩展阅读

[^default]: https://github.com/microsoft/vscode-dev-containers/tree/main/containers/codespaces-linux
[^devcontainer]: https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/introduction-to-dev-containers
[^jsondoc]: https://containers.dev/implementors/json_reference/
[^template]: https://github.com/microsoft/vscode-dev-containers
[^features]: https://github.com/devcontainers/features
[^deepdive]: https://docs.github.com/en/codespaces/getting-started/deep-dive
[^billing]: https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces
