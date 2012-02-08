---
layout: post
title: "配置博客的时候碰到的一些问题"
date: 2012-02-08 15:54
comments: true
categories: sth 
---
我在配置这个博客的时候遇到了各种各样的问题，在这里分享一下
最初我按照 [DF大牛牛](http://http://dangfan.me/)的博客，以及[jekyllbootstrap](http://jekyllbootstrap.com)提供的教程配置,但是没有成功，出现了各种各种的问题，实在无法解决，只好作罢。比如：

- bundle install的时候显示安装了某某，运行的时候提示找不到某某
- 不sudo执行命令说没有权限，sudo执行说没有该命令

接着我按照[Octopress](http://octopress.org/docs/setup/)提供的教程一步一步的做。发现:

1\. 我用*apt-get*安装的ruby环境不能用，在每一步都会出问题，上一段说的问题应该就是这个缘故。

2\. 于是我使用*rvm*管理版本。首先卸载掉之前*apt-get*装的一切ruby有关的内容，然后用rvm重新安装，见[Octopress](http://octopress.org/docs/setup/),在这里按说明安装好ruby,gem,bundle等包

3\. 官网上说使用*rake*，但是在依赖安装完之后我并没有rake可以使用，linux提示使用apt-get，但是这里如果用了就会出问题。原因见1. 网上有人说可以gem install rake，于是我就这么做了。结果是，依然错误。*gem install* 装的rake 版本为0.9.2，它需要0.9。解决方法是，卸载掉它们，进.rvm/bin发现，有一个*rake-ruby-1.9.2-p290* ,是ruby-1.9.2带的。用这个当rake，就可以继续进行了。


