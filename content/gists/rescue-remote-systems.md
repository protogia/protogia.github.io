---
title: 'How to rescue a full remote system without losing data'
date: '2023-11-03T14:34:06+01:00'
author: 'Giancarlo Rizzo'
draft: false
categories: [linux]
color: '#99cc99'
---

# Prologue

It shouldn't happen, but the reality is often different. Remote servers that may not be included in monitoring or for which there is no alerting become full as soon as several users use them extensively and system maintenance is forgotten. In the worst case, the filling log files are even important and must not be lost.


## Identify the most storage intensive folders

1. First you should find the location of the problem. You list all directories and their memory usage.

```bash
sudo you -sh /*
```

2. If you want to find out the core of the problem, you should sort the output and then filter the top 10 entries:

```bash
sudo du -sh ./* | sort -h | head -n 10
```

## Transfer and delete

Now you can start transferring the folder with the largest memory usage. If there is an insecure connection such as via LTE, you should proceed file by file so as not to risk a broken pipe error. You use rsync for this

```bash
mkdir ~/Downloads/save_bckp
rsync --remove-source-files -av remoteuser@<remoteip>:/path/to/big/folder/* ./Downloads/save_bckp
```

The process takes a long time, but it clears the hard drive and backs up the data at the same time. In case of connection failures, you can restart the command without leaving out any files. If the connection is considered secure, you can also use scp recursively. This works faster, but there is a risk.

## If login is no longer possible

If remote login is no longer possible, you can try to restart the host using a hard reset, provided it can be switched off using an external switching unit.