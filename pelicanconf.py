#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'\u6e05\u98ce\u672a\u660e'
SITENAME = u'\u8bb0\u5f55'
SITEURL = ''

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'
STATIC_PATHS = [u"image"]


#Plugin
PLUGIN_PATH = u"pelican-plugins"
PLUGINS = ["sitemap","code_include","latex"]

SITEMAP = { "format": "xml", "priorities": { "articles": 0.7, "indexes": 0.5, "pages": 0.3, }, "changefreqs": { "articles": "monthly", "indexes": "daily", "pages": "monthly", }}
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DISQUS_SITENAME = u"ghdawn"
GOOGLE_ANALYTICS = u"UA-29027763-1"


FEED_RSS = u"feeds/all.rss.xml" 
CATEGORY_FEED_RSS=u"feeds/%s.rss.xml"

THEME = "bootstrap2"
# Blogroll
LINKS =  (('DFDNN', 'https://dangfan.me/zhs'),
          ('Dumbear', 'http://dumbear.com/'),
          ('逆铭', 'http://www.tomtung.com/'),
          )

# Social widget
SOCIAL = (('github', 'https://github.com/ghdawn'),
          ('饭否', 'http://fanfou.com/home'))
DEFAULT_PAGINATION = 7

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
