---
title: 'How is this website build?'
date: '2026-03-15T21:47:42+01:00'
author: ''
draft: false
plotly: true
color: '#a09f93'
---
Its a static website created via Hugo. You can find the [source-code](https://github.com/protogia/protogia.github.io) and [theme](https://github.com/protogia/formula-1-theme) on my GitHub. The plotly-graphs are loaded via javascript as locally-stored json-files. I created a [jupyter-notebook2markdown-converter](https://github.com/protogia/nb2hugo-markdown) that fits the needs of this webblog to render this interactive graphs on this static website.