---
title: 'Does this blog use analytics?'
date: '2026-03-15T11:21:38+01:00'
author: ''
draft: false
plotly: true
color: '#a09f93'
---

No, currently it is not using analytics. The only thing I track for fun is how many times my project-repositories are cloned and similar statistics. 
I use the Github-API to fetch the data daily and save it in a separate public repository [github-repo-stats](https://github.com/protogia/github-repo-stats).
The plots are embedded in this website by referring them using this shortcode: `{{ plotly json="https://raw.githubusercontent.com/USERNAME/github-repo-stats/main/plots/clones.json"}}`.

If you want to do so too, just fork that repo, follow the instructions and change the _USERNAME_ in the shortcode.

{{< plotly json="https://raw.githubusercontent.com/protogia/github-repo-stats/main/plots/clones.json" >}}