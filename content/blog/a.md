---
title: 'A'
date: '2023-10-26T02:41:48+02:00'
author: 'Giancarlo Rizzo'
draft: true
tags: offtopic
categories: []
color: '--base0a'
---

# Test title

something about a

**test bold** _italic_ 

[links](https://github.com/protogia)

```bash
sudo systemctl status your.service
```

```py
import pandas as pd

df = pd.DataFrame()
df.head
```

```mermaid
graph TB
  subgraph HOST_A
    A_eth0[eth0]
  end

  subgraph HOST_B
    B_eth0[eth0]
    B_eth1[eth1]
  end

  subgraph HOST_C
    C_eth0[eth0]
  end

  A_eth0 -->|Communicate| B_eth0
  B_eth1 -->|Communicate| C_eth0

  B_eth0 -->|Communicate| A_eth0
  C_eth0 -->|Communicate| B_eth1

```