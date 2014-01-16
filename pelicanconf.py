#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'\u6e05\u98ce\u672a\u660e'
SITENAME = u'\u8bb0\u5f55'
SITEURL = ''

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'zh'

#Plugin
PLUGIN_PATH = u"pelican-plugins"
PLUGINS = ["sitemap","code_include","latex"]

SITEMAP = { "format": "xml", "priorities": { "articles": 0.7, "indexes": 0.5, "pages": 0.3, }, "changefreqs": { "articles": "monthly", "indexes": "daily", "pages": "monthly", }}
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DISQUS_SITENAME = u"ghdawn"

STATIC_PATHS = [u"content/img"]

THEME = "bootstrap2"
# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
