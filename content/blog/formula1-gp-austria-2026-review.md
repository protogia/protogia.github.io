---
title: 'Formula1 - GP Austria: 2026'
date: '2026-08-14T18:42:29.077997+00:00'
author: 'Giancarlo Rizzo'
draft: false
plotly: true
code_options: true
categories: [Formula 1, Analytics]
---
<a href="https://colab.research.google.com/github/protogia/formula1-evaluations/blob/main/gp-austria-2026-review.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Prologue

**Location:** Red Bull Ring, Spielberg

The 2026 season reaches one of its peaks in the Styrian Mountains. A scorching hot weekend, with track temperatures soaring to 50°C, pushed both man and machine to their absolute limits, setting the stage for a race fraught with challenges.

The initial analysis of the practice sessions pointed to strong performances from Antonelli, Piastri, and Russell. However, whispers in the paddock suggested Russell's setup might not have been perfectly aligned with his teammate, a crucial detail that could unravel as the weekend progressed.

Red Bull, traditionally dominant on home turf, found themselves in a precarious position. Significant configuration and technical component changes seemed to plague the team, with both Verstappen and Hadja battling intermittent RPM drops. The critical question remains: did they have enough time to validate these changes and gather sufficient data in the intense Austrian heat?

{{<details title="Show code">}}

```python
!pip install fastf1
!pip install git+https://github.com/protogia/formula-1-plotly-utils.git
```

    Requirement already satisfied: fastf1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (3.8.3)
    Requirement already satisfied: cryptography in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (50.0.0)
    Requirement already satisfied: matplotlib<4.0.0,>=3.8.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (3.11.1)
    Requirement already satisfied: numpy<3.0.0,>=1.26.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (2.5.2)
    Requirement already satisfied: pandas<3.0.0,>=2.1.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (2.3.3)
    Requirement already satisfied: platformdirs in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (4.11.3)
    Requirement already satisfied: pydantic in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (2.13.4)
    Requirement already satisfied: pyjwt in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (2.13.0)
    Requirement already satisfied: python-dateutil in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (2.9.0.post0)
    Requirement already satisfied: rapidfuzz in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (3.14.5)
    Requirement already satisfied: requests-cache>=1.0.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (1.3.3)
    Requirement already satisfied: requests>=2.30.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (2.34.2)
    Requirement already satisfied: scipy<2.0.0,>=1.11.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (1.18.0)
    Requirement already satisfied: signalrcore in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (1.0.2)
    Requirement already satisfied: timple>=0.1.6 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (0.1.8)
    Requirement already satisfied: websockets>=10.3 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (17.0.1)
    Requirement already satisfied: contourpy>=1.0.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1) (1.3.3)
    Requirement already satisfied: cycler>=0.10 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1) (0.12.1)
    Requirement already satisfied: fonttools>=4.28.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1) (4.63.0)
    Requirement already satisfied: kiwisolver>=1.3.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1) (1.5.0)
    Requirement already satisfied: packaging>=20.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1) (26.3)
    Requirement already satisfied: pillow>=9 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1) (12.3.0)
    Requirement already satisfied: pyparsing>=3 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1) (3.3.2)
    Requirement already satisfied: pytz>=2020.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pandas<3.0.0,>=2.1.1->fastf1) (2026.3.post1)
    Requirement already satisfied: tzdata>=2022.7 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pandas<3.0.0,>=2.1.1->fastf1) (2026.3)
    Requirement already satisfied: six>=1.5 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from python-dateutil->fastf1) (1.17.0)
    Requirement already satisfied: charset_normalizer<4,>=2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.30.0->fastf1) (3.5.0)
    Requirement already satisfied: idna<4,>=2.5 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.30.0->fastf1) (3.18)
    Requirement already satisfied: urllib3<3,>=1.26 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.30.0->fastf1) (2.7.0)
    Requirement already satisfied: certifi>=2023.5.7 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.30.0->fastf1) (2026.7.22)
    Requirement already satisfied: attrs>=21.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests-cache>=1.0.0->fastf1) (26.1.0)
    Requirement already satisfied: cattrs>=22.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests-cache>=1.0.0->fastf1) (26.1.0)
    Requirement already satisfied: url-normalize>=2.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests-cache>=1.0.0->fastf1) (3.0.0)
    Requirement already satisfied: cffi>=2.0.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from cryptography->fastf1) (2.1.1)
    Requirement already satisfied: annotated-types>=0.6.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pydantic->fastf1) (0.8.0)
    Requirement already satisfied: pydantic-core==2.46.4 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pydantic->fastf1) (2.46.4)
    Requirement already satisfied: typing-extensions>=4.14.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pydantic->fastf1) (4.16.0)
    Requirement already satisfied: typing-inspection>=0.4.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pydantic->fastf1) (0.4.4)
    Requirement already satisfied: msgpack==1.1.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from signalrcore->fastf1) (1.1.2)
    Requirement already satisfied: pycparser in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from cffi>=2.0.0->cryptography->fastf1) (3.0)
    
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m24.1[0m[39;49m -> [0m[32;49m26.2.1[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m
    Collecting git+https://github.com/protogia/formula-1-plotly-utils.git
      Cloning https://github.com/protogia/formula-1-plotly-utils.git to /tmp/pip-req-build-es9t163w
      Running command git clone --filter=blob:none --quiet https://github.com/protogia/formula-1-plotly-utils.git /tmp/pip-req-build-es9t163w
      Resolved https://github.com/protogia/formula-1-plotly-utils.git to commit f0fa166b5c51320d2436607772ed28c405c3a41a
      Installing build dependencies ... [?25ldone
    [?25h  Getting requirements to build wheel ... [?25ldone
    [?25h  Preparing metadata (pyproject.toml) ... [?25ldone
    [?25hRequirement already satisfied: fastf1<4.0.0,>=3.8.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from formula-1-plotly-utils==0.1.0) (3.8.3)
    Requirement already satisfied: pandas<3.0.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from formula-1-plotly-utils==0.1.0) (2.3.3)
    Requirement already satisfied: plotly<7.0.0,>=6.5.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from formula-1-plotly-utils==0.1.0) (6.9.0)
    Requirement already satisfied: cryptography in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (50.0.0)
    Requirement already satisfied: matplotlib<4.0.0,>=3.8.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (3.11.1)
    Requirement already satisfied: numpy<3.0.0,>=1.26.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2.5.2)
    Requirement already satisfied: platformdirs in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (4.11.3)
    Requirement already satisfied: pydantic in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2.13.4)
    Requirement already satisfied: pyjwt in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2.13.0)
    Requirement already satisfied: python-dateutil in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2.9.0.post0)
    Requirement already satisfied: rapidfuzz in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (3.14.5)
    Requirement already satisfied: requests-cache>=1.0.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (1.3.3)
    Requirement already satisfied: requests>=2.30.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2.34.2)
    Requirement already satisfied: scipy<2.0.0,>=1.11.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (1.18.0)
    Requirement already satisfied: signalrcore in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (1.0.2)
    Requirement already satisfied: timple>=0.1.6 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (0.1.8)
    Requirement already satisfied: websockets>=10.3 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (17.0.1)
    Requirement already satisfied: pytz>=2020.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pandas<3.0.0->formula-1-plotly-utils==0.1.0) (2026.3.post1)
    Requirement already satisfied: tzdata>=2022.7 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pandas<3.0.0->formula-1-plotly-utils==0.1.0) (2026.3)
    Requirement already satisfied: narwhals>=1.15.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from plotly<7.0.0,>=6.5.2->formula-1-plotly-utils==0.1.0) (2.24.0)
    Requirement already satisfied: packaging in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from plotly<7.0.0,>=6.5.2->formula-1-plotly-utils==0.1.0) (26.3)
    Requirement already satisfied: contourpy>=1.0.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (1.3.3)
    Requirement already satisfied: cycler>=0.10 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (0.12.1)
    Requirement already satisfied: fonttools>=4.28.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (4.63.0)
    Requirement already satisfied: kiwisolver>=1.3.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (1.5.0)
    Requirement already satisfied: pillow>=9 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (12.3.0)
    Requirement already satisfied: pyparsing>=3 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (3.3.2)
    Requirement already satisfied: six>=1.5 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from python-dateutil->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (1.17.0)
    Requirement already satisfied: charset_normalizer<4,>=2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.30.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (3.5.0)
    Requirement already satisfied: idna<4,>=2.5 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.30.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (3.18)
    Requirement already satisfied: urllib3<3,>=1.26 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.30.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2.7.0)
    Requirement already satisfied: certifi>=2023.5.7 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.30.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2026.7.22)
    Requirement already satisfied: attrs>=21.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests-cache>=1.0.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (26.1.0)
    Requirement already satisfied: cattrs>=22.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests-cache>=1.0.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (26.1.0)
    Requirement already satisfied: url-normalize>=2.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests-cache>=1.0.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (3.0.0)
    Requirement already satisfied: cffi>=2.0.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from cryptography->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2.1.1)
    Requirement already satisfied: annotated-types>=0.6.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pydantic->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (0.8.0)
    Requirement already satisfied: pydantic-core==2.46.4 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pydantic->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2.46.4)
    Requirement already satisfied: typing-extensions>=4.14.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pydantic->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (4.16.0)
    Requirement already satisfied: typing-inspection>=0.4.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pydantic->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (0.4.4)
    Requirement already satisfied: msgpack==1.1.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from signalrcore->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (1.1.2)
    Requirement already satisfied: pycparser in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from cffi>=2.0.0->cryptography->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (3.0)
    Building wheels for collected packages: formula-1-plotly-utils
      Building wheel for formula-1-plotly-utils (pyproject.toml) ... [?25ldone
    [?25h  Created wheel for formula-1-plotly-utils: filename=formula_1_plotly_utils-0.1.0-py3-none-any.whl size=17296 sha256=480f68c7391772cbef84e095bafd68e98ff932ca36a0472262a0db8c7b20b5ae
      Stored in directory: /tmp/pip-ephem-wheel-cache-dy2mzkyh/wheels/7c/0f/19/04eeb5d297e4078ad7eb3694ce97a4c4eb49be375a32ef2538
    Successfully built formula-1-plotly-utils
    Installing collected packages: formula-1-plotly-utils
    Successfully installed formula-1-plotly-utils-0.1.0
    
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m24.1[0m[39;49m -> [0m[32;49m26.2.1[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m

```python
# log-config
import warnings
warnings.filterwarnings('ignore')

# layout-config
from IPython.core import display
display.display_html(display.HTML(""))

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
```

```python
# load data
import fastf1
from formula_1_plotly_utils import utils

Q = fastf1.get_session(2026, 'Austria', 'Q')
Q.load()
```

    req         WARNING 	DEFAULT CACHE ENABLED! (441.34 MB) /home/working/.cache/fastf1
    core           INFO 	Loading data for Austrian Grand Prix - Qualifying [v3.8.3]
    req            INFO 	Using cached data for session_info
    req            INFO 	Using cached data for driver_info
    req            INFO 	Using cached data for session_status_data
    req            INFO 	Using cached data for track_status_data
    req            INFO 	Using cached data for _extended_timing_data
    req            INFO 	Using cached data for timing_app_data
    core           INFO 	Processing timing data...
    req            INFO 	Using cached data for car_data
    req            INFO 	Using cached data for position_data
    req            INFO 	Using cached data for weather_data
    req            INFO 	Using cached data for race_control_messages
    core           INFO 	Finished loading data for 22 drivers: ['63', '16', '44', '12', '3', '1', '81', '6', '30', '41', '10', '5', '87', '27', '31', '43', '55', '23', '11', '77', '14', '18']

{{</details>}}

## The Track's True Test: Elevation and Gradient

Let us take a look first on the track itself. The Red Bull Ring, while seemingly compact, is a relentless test of engineering and driving prowess, largely due to its significant elevation changes. As the next track visualizations clearly illustrate, the circuit is far from flat. The `plot_track` analysis, highlights the dramatic shifts in elevation that drivers navigate on every lap. From the steep uphill run after Turn 1, demanding immense torque and precise throttle control, to the undulating sections through the middle of the lap, the track constantly challenges the car's balance and aerodynamic setup.

{{<details title="Show code">}}

```python
fig = utils.plot_track(
    position=Q.laps.pick_fastest().get_telemetry(),
    circuit_info=Q.get_circuit_info(),
    metrics=['elevation', 'speed']
)


fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-austria-2026-review/plotly_chart_13.json" >}}

The `plot_track_elevation` further dissects this challenge, pinpointing the exact moments of ascent and descent along the circuit.

Nestled at a brisk 660 meters above sea level, the Red Bull Ring presents the first true high-altitude test of the season, a critical factor for engine performance. This thinner air means less oxygen, directly impacting combustion and demanding more from the power units. Coupled with spectacular inclines of up to 12 percent and equally dramatic descents reaching 9.3 percent, alongside a total altitude difference of 65 meters across the circuit, it's a relentless workout for every component. The altitude means the turbocharger is under significantly greater strain compared to other races. Without components like the MGU-H, which is no longer part of the 2026 regulations, the vital assistance for the turbocharger is gone, making the correct operation of both the turbocharger and the engine at such high altitudes a formidable task.

Corners like the unforgiving Turn 3 (Remus) and the rapid run through Turns 6 and 7 are shown to have notable altitude gradients. These gradients not only stress the power units but also amplify the braking demands and can catch out drivers pushing the limits, as evidenced by multiple dropouts in the final corner throughout the sessions. Cadillac, in particular, seemed to struggle with the technical intricacies, facing various issues exacerbated by these track characteristics.

{{<details title="Show code">}}

```python
fig = utils.plot_track_elevation(
    position = Q.laps.pick_fastest().get_pos_data(),
    circuit_info = Q.get_circuit_info(),
    reference_altitude = 639.5
  )

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-austria-2026-review/plotly_chart_12.json" >}}

## Qualifying

The next Chart show the Track Temperatures and Air Temperatures during the Qualifying. For the teams and drivers at the Red Bull Ring, the blistering temperatures meant one thing: the tires were constantly teetering on the edge of their optimal operating window. When rubber compounds get this hot, they become softer and far more susceptible to wear, leading to a much faster decline in grip and performance. We're talking about accelerated thermal degradation, where the internal structure of the tire itself begins to break down.

This aggressive breakdown often manifests as [blistering – small chunks of rubber literally detaching from the tire surface – or graining, where the soft rubber rolls into small balls that dramatically reduce the contact patch](https://www.reddit.com/r/F1Technical/comments/vsw6s1/tyre_blistering_and_graining_explanation_causes/). Both are kryptonite to a driver's pace, making the car squirm and slide, demanding a delicate touch that few can sustain lap after lap.

Crucially, these high temperatures push tires beyond their sweet spot, leading to what strategists ominously call 'falling off a cliff' – a sudden, catastrophic drop in performance. This forces teams to consider more aggressive pit strategies, sometimes opting for shorter stints or harder compounds to cope with the relentless heat. It's a high-stakes gamble: push too hard, and you melt your tires; manage them too conservatively, and you lose crucial track position.

Beyond the rubber, the heat poses a significant challenge to the power units themselves. High ambient and track temperatures demand peak performance from cooling systems, pushing engines to their absolute limit.

{{<details title="Show code">}}

```python
fig = utils.plot_weather_data(Q.weather_data)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-austria-2026-review/plotly_chart_11.json" >}}

Pirelli, recognizing the brutal conditions, arrived with their softest compounds – C3, C4, and C5 – anticipating that thermal degradation, rather than outright wear, would be the dominant factor.

Their analysis confirmed that while the Red Bull Ring's aged asphalt, with its high micro and macro-roughness, generates considerable heat in the tires, overall wear isn't the primary concern. Instead, it's the internal thermal stress that dictates tire life. Grip levels, however, tend to improve over the weekend as more rubber is laid down on the track from the numerous motorsport events held there throughout the year.

All drivers started with the Soft Compound to reach the best laptimes.

{{<details title="Show code">}}

```python
drivers = Q.laps['Driver'].unique()

fig = utils.plot_tyre_strategies(
    drivers=drivers,
    laps=Q.laps,
    track_status=Q.track_status,
)
fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-austria-2026-review/plotly_chart_10.json" >}}

In the battle for pole position, five drivers laid claim to the fastest lap at various stages. Q1 saw Antonelli and Leclerc briefly topping the charts, signaling their intent early on.

However, it was in Q2 that Max Verstappen, usually an unassailable force at the Red Bull Ring, initially dominated, confidently retreating to the garage, seemingly certain his time was untouchable. He gambled, electing to conserve his car and tires, a strategic 'poker face' suggesting he had enough in hand for a comfortable Q3 berth.

Yet, the relentless pace of his rivals proved his confidence a touch premature. Both Hamilton and Leclerc unleashed top performance, eclipsing Verstappen's benchmark within Q2.

{{<details title="Show code">}}

```python
fig = utils.plot_leading_laptimes(
    laps=Q.laps,
    track_status=Q.track_status,
    drivers=Q.laps['Driver'].unique()
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-austria-2026-review/plotly_chart_9.json" >}}

Then in Q3, all kicked off. A crash by Verstappen, caused by losing grip in **corner 9**, led to a single-yellow-flag phase. All drivers immediately stopped to hunt for the pole, except George Russell.

He considered that due to the regulations, drivers need to cut off the gas.

_From the FIA sporting regs:_
> 26) GENERAL SAFETY 26.1 a) Single Waved Yellow Flag: Any driver passing through a waved yellow flag marshalling sector must reduce their speed and be prepared to change direction. In order for the stewards to be satisfied that any such driver has complied with these requirements they are expected to have braked earlier and/or discernibly reduced speed in the relevant marshalling sector.


In the next plot we compare the best lap of Leclerc and Russel. Leclercs best lap was lap 14 at this moment. The choosen Lap for Russel is the one where Verstappen crashed and Russel cut of his speed for a short period. You can see the moment when Verstappen crashed in in the throttle chart of Russel at _3558.5 meters_. He immediately stepped off the gas pedal. Look at the map and the line chart for the throttle telemetry which indicates the difference between Russels and Leclercs best lap. In the speed chart you see that Russel had higher speed then Leclerc before Verstappen's crash and looses immidiatly due to the gas lift but had been in fortune that he needed to reduce his speed for corner 9 and corner 10 anyway. With the recuperation working during this lift, he was even able to gain energy in this period to accelerate even faster after the final corner, driving the best lap time over the finish line.

{{<details title="Show code">}}

```python
figures = utils.plot_lap_telemetry_comparison(
    laps=Q.laps,
    circuit_info=Q.get_circuit_info(),
    driver1_code='LEC',
    driver2_code='RUS',
    driver1_lap='fastest',
    driver2_lap='fastest',
    highlight_distance=3558.554,
    highlight_label="Verstappen's Crash Corner",
    metrics_to_plot=['Speed', 'Throttle', 'Brake']
)
for fig in figures:
    fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-austria-2026-review/plotly_chart_8.json" >}}

Finally the Qualifying ended with the following Starting grid and lap times for Q1, Q2 and Q3:

{{<details title="Show code">}}

```python
fig = utils.plot_best_laptime(
    results=Q.results,
    drivers=Q.laps['Driver'].unique(),
    criteria="qualifying"
)
fig.show()

```

{{</details>}}

{{< plotly json="/plotly/gp-austria-2026-review/plotly_chart_5.json" >}}

## Race

As the sun reached its zenith over the Spielberg peaks, the atmosphere in the grandstands shifted from the frantic energy of qualifying to the heavy, focused tension of race day. 200,000 fans, a sea of orange and red, watched as the asphalt shimmered under a heat haze that threatened to turn the Austrian GP into a war of attrition.

While George Russell occupied the pole position, the narrative was far from settled. The Mercedes camp looked calm, but the proximity of Leclerc and a resurgent Hamilton meant any slip-off the line would be punished instantly. Further back, the questions surrounding Red Bull’s technical stability remained the talk of the grid. Verstappen, starting out of his usual position after his Q3 shunt, but his confidence tested on a track that usually bows to his command.

Strategy was the second protagonist of the day. With track temperatures refusing to drop, the 'cliff' wasn't just a metaphor; it was a looming reality. The pit wall engineers were no longer just looking at lap times—they were monitoring internal tire carcasses and engine thermal loads with precision. One missed cooling cycle or one overly aggressive defense could end a race before the halfway mark.

{{<details title="Show code">}}

```python
R = fastf1.get_session(2026, 'Austria', 'R')
R.load()
```

    core           INFO 	Loading data for Austrian Grand Prix - Race [v3.8.3]
    req            INFO 	No cached data found for session_info. Loading data...
    _api           INFO 	Fetching session info data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for driver_info. Loading data...
    _api           INFO 	Fetching driver list...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for session_status_data. Loading data...
    _api           INFO 	Fetching session status data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for lap_count. Loading data...
    _api           INFO 	Fetching lap count data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for track_status_data. Loading data...
    _api           INFO 	Fetching track status data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for _extended_timing_data. Loading data...
    _api           INFO 	Fetching timing data...
    _api           INFO 	Parsing timing data...
    _api        WARNING 	Failed to align laps for drivers: ['77']
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for timing_app_data. Loading data...
    _api           INFO 	Fetching timing app data...
    req            INFO 	Data has been written to cache!
    core           INFO 	Processing timing data...
    core        WARNING 	Driver 63 completed the race distance 00:00.530000 before the recorded end of the session.
    req            INFO 	No cached data found for car_data. Loading data...
    _api           INFO 	Fetching car data...
    _api           INFO 	Parsing car data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for position_data. Loading data...
    _api           INFO 	Fetching position data...
    _api           INFO 	Parsing position data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for weather_data. Loading data...
    _api           INFO 	Fetching weather data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for race_control_messages. Loading data...
    _api           INFO 	Fetching race control messages...
    req            INFO 	Data has been written to cache!
    core           INFO 	Finished loading data for 22 drivers: ['63', '3', '12', '81', '44', '6', '1', '16', '30', '41', '5', '27', '10', '87', '43', '31', '23', '14', '18', '55', '11', '77']

```python
fig = utils.plot_weather_data(R.weather_data)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-austria-2026-review/plotly_chart_4.json" >}}

### The Start: Chaos and Attrition

George Russell converted his pole into an immediate lead, while Lewis Hamilton used his experience to snatch second from Charles Leclerc by Turn 5. Kimi Antonelli, fighting for grip, ran wide at both Turns 1 and 3, which opened the door for Max Verstappen. By the end of the second lap, Verstappen had clinically dispatched both Leclerc and Antonelli to move into third.

Reliability became an early story of the day with a disastrous double blow for Cadillac. Valtteri Bottas limped into the pits with brakes ablaze after just two laps, followed shortly by Sergio Pérez, who reported smoke in the cockpit. Both were forced to retire within the first five laps due to overheating brakes, ending Cadillac's race prematurely.

### Strategic Gambles and Virtual Safety Cars

The mid-race phase was defined by varying strategies. Ferrari attempted to offset a lack of raw pace with aggression, bringing Leclerc and Hamilton in early. Hamilton and Verstappen engaged in a fierce wheel-to-wheel battle on lap 11, where Verstappen was forced onto the gravel at the exit of Turn 6.

A Virtual Safety Car (VSC), triggered by Carlos Sainz's electrical failure on the pit straight, further complicated the math. While Russell and Verstappen stayed on two-stop paths, Ferrari committed Hamilton to a three-stop strategy, banking on fresh Soft tyres for a late-race charge.

**Key Strategic Shift:** Look at the 'Position per Lap' logic in the context of the tyre chart. Hamilton (Driver 44) sacrificed track position during the VSC for a tyre-age advantage, while Antonelli's pit timing just before the VSC dropped him behind the Ferraris temporarily.

{{<details title="Show code">}}

```python
fig = utils.plot_tyre_strategies(
    drivers=R.laps['Driver'].unique(),
    laps=R.laps,
    track_status=R.track_status,
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-austria-2026-review/plotly_chart_3.json" >}}

### Tyre Strategies

- *Two-Stop-Strategy* Russell and Verstappen maximized the Hard compound's durability. The chart shows Verstappen's late second stint (diagonal shift to the right), designed to give him an offset for the final attack.
- *The Three-Stop-Strategy* Both Ferrari drivers (LEC and HAM) appear with more frequent vertical bars, indicating their attempt to stay in the 'optimal grip window' by sacrificing pit lane time for fresher rubber.

Despite the high temperatures, the Hard tyre (white/grey indicators) became the mandatory race tyre for the final stints, as the Softs (red) proved too volatile for long-distance management under the Styrian sun.

{{<details title="Show code">}}

```python
fig = utils.plot_gap_between_d1_d2(
    laps=R.laps,
    driver1_code='RUS',
    driver2_code='VER',
    event_lap=43,
    event_label="Russell's Final Pit Stop")
fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-austria-2026-review/plotly_chart_2.json" >}}

At lap 43 Russell had its second and final pit stop, where he took on hard tires and rejoined the track ahead of those yet to pit. Red Bull, however, chose to keep Verstappen out for an additional five laps, stopping him on lap 49 for new hard tires. This decision aimed to give Verstappen a tire-age advantage for the final stint, but it cost him track position, as he rejoined approximately ten seconds behind Russell with 22 laps remaining.

Observe how the gap fluctuates before and after these events, indicating the impact of pit strategy and on-track pace management from both drivers. Verstappen, despite his newer tires, was unable to close the gap sufficiently to attempt an overtake. Russell, despite briefly running wide on lap 58, maintained a strong pace to control the lead, ultimately crossing the finish line 1.6 seconds ahead of Verstappen.

### Conclusion

In the end, Verstappen ran out of laps. Russell crossed the line a mere 1.6 seconds ahead of the Red Bull, with Antonelli completing the podium just a second behind Verstappen.

Beyond the top three, the pace dropped significantly. Liam Lawson and Arvid Lindblad were nearly 1.2 seconds per lap slower on average than the leaders due to the 2 stop-strategy.

{{<details title="Show code">}}

```python
# Filter for point scorers (Top 10)
points_finishers = R.results.sort_values(by='Position').head(10)['Abbreviation'].tolist()
points_laps = R.laps.pick_quicklaps().loc[R.laps['Driver'].isin(points_finishers)].copy()
points_laps['LapTimeSeconds'] = points_laps['LapTime'].dt.total_seconds()

# Calculate consistency (Standard Deviation of lap times) and Average Pace
performance_stats = points_laps.groupby('Driver').agg(
    AvgLapTime=('LapTimeSeconds', 'mean'),
    MedianLapTime=('LapTimeSeconds', 'median'),
    Consistency=('LapTimeSeconds', 'std'),
    FastestLap=('LapTimeSeconds', 'min')
).reset_index()

# Merge with final positions for context
performance_summary = pd.merge(
    performance_stats,
    R.results[['Abbreviation', 'Position', 'Status']],
    left_on='Driver',
    right_on='Abbreviation'
).sort_values(by='Position')

# Calculate gap to winner's average pace
winner_avg = performance_summary.iloc[0]['AvgLapTime']
performance_summary['GapToWinner_Avg'] = performance_summary['AvgLapTime'] - winner_avg

# Use the display function correctly
from IPython.display import display as ipy_display
ipy_display(performance_summary[['Position', 'Driver', 'AvgLapTime', 'Consistency', 'FastestLap', 'GapToWinner_Avg']])
```

| Position | Driver | AvgLapTime | Consistency | FastestLap | GapToWinner_Avg |
| --- | --- | --- | --- | --- | --- |
| 8 | 1.0 | RUS | 71.808349 | 0.760112 | 70.683 | 0.000000 |
| 9 | 2.0 | VER | 71.743661 | 0.793297 | 70.483 | -0.064688 |
| 0 | 3.0 | ANT | 71.765234 | 0.955327 | 70.374 | -0.043115 |
| 7 | 4.0 | PIA | 72.080079 | 0.919412 | 70.595 | 0.271730 |
| 2 | 5.0 | HAM | 72.000921 | 0.727563 | 70.946 | 0.192571 |
| 1 | 6.0 | HAD | 72.195365 | 0.772216 | 70.947 | 0.387016 |
| 6 | 7.0 | NOR | 72.159694 | 0.880250 | 70.652 | 0.351344 |
| 4 | 8.0 | LEC | 72.032557 | 0.918557 | 70.606 | 0.224208 |
| 3 | 9.0 | LAW | 72.983787 | 0.826471 | 71.547 | 1.175438 |
| 5 | 10.0 | LIN | 73.089098 | 0.815516 | 71.587 | 1.280749 |

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Sort by position for the plot
plot_data = performance_summary.sort_values('Position')

# Create a multi-axis plot
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add Average Pace (Bar)
fig.add_trace(
    go.Bar(
        x=plot_data['Driver'],
        y=plot_data['AvgLapTime'],
        name="Avg Lap Time (s)",
        opacity=0.7,
        text=plot_data['AvgLapTime'].round(3),
        textposition='outside'
    ),
    secondary_y=False,
)

# Add Consistency (Line)
fig.add_trace(
    go.Scatter(
        x=plot_data['Driver'],
        y=plot_data['Consistency'],
        name="Consistency (Std Dev)",
        mode='lines+markers+text',
        line=dict(color='orange', width=3),
        text=plot_data['Consistency'].round(3),
        textposition='top center'
    ),
    secondary_y=True,
)
    metrics=['elevation', 'speed']
fig.update_layout(
    title="Performance Metrics: Average Pace vs. Consistency (Top 10)",
    xaxis_title="Driver (Ordered by Final Position)",
    legend=dict(x=1.1, y=1),
    yaxis=dict(title="Seconds", range=[plot_data['AvgLapTime'].min() - 0.5, plot_data['AvgLapTime'].max() + 0.5]),
    yaxis2=dict(title="Consistency (Lower is Better)", overlaying='y', side='right')
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-austria-2026-review/plotly_chart_1.json" >}}