title: "又是octopress博客的问题"
date: 2012-12-02 21:57
Tags: Boring,blog
Category: Study 

假期换了电脑，在新电脑上写了博客，但是怎么也提交不上去，一直提示：

	## Pushing generated _deploy website
	Everything up-to-date

在[这里](https://github.com/imathis/octopress/issues/336)找到了解决方法：

运行

`rake setup_github_pages`

输入博客的git地址，即可更新
