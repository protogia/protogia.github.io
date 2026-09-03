---
title: 'Formula 1 - GP Britain 2026 Review'
date: '2026-08-14T18:49:22.908695+00:00'
author: 'Giancarlo Rizzo'
draft: false
plotly: true
code_options: true
categories: [Formula 1, Analytics]
color: '#a09f93'
---

<a href="https://colab.research.google.com/github/protogia/formula1-evaluations/blob/main/gp-britain-2026-review.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Prologue

**Location:** Silverstone Circuit, Northamptonshire

The 2026 season arrives at the 'Home of British Motor Racing'.

Mercedes entered their home race with a formidable lineup: the experienced George Russell and the sensational rookie Kimi Antonelli. However, the British fans were also cheering for Lewis Hamilton, who aimed to reclaim his throne at the circuit he has dominated for over a decade, even though he lost the first test in the Sprint against Antonelli. Red Bull, with Verstappen and Hadjar, remained the technical benchmark despite rumors of reliability concerns.

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
      Cloning https://github.com/protogia/formula-1-plotly-utils.git to /tmp/pip-req-build-aq3o9q6d
      Running command git clone --filter=blob:none --quiet https://github.com/protogia/formula-1-plotly-utils.git /tmp/pip-req-build-aq3o9q6d
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
!pwd
```

    /home/working/protogia/projects/formula1-evaluations/2026

```python
# load data
import fastf1
from formula_1_plotly_utils import utils

Q = fastf1.get_session(2026, 'Britain', 'Q')
Q.load()
```

    req         WARNING 	DEFAULT CACHE ENABLED! (543.1 MB) /home/working/.cache/fastf1
    events      WARNING 	Correcting user input 'Britain' to 'British Grand Prix'
    core           INFO 	Loading data for British Grand Prix - Qualifying [v3.8.3]
    req            INFO 	No cached data found for session_info. Loading data...
    _api           INFO 	Fetching session info data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for driver_info. Loading data...
    _api           INFO 	Fetching driver list...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for session_status_data. Loading data...
    _api           INFO 	Fetching session status data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for track_status_data. Loading data...
    _api           INFO 	Fetching track status data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for _extended_timing_data. Loading data...
    _api           INFO 	Fetching timing data...
    _api           INFO 	Parsing timing data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for timing_app_data. Loading data...
    _api           INFO 	Fetching timing app data...
    req            INFO 	Data has been written to cache!
    core           INFO 	Processing timing data...
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
    core           INFO 	Finished loading data for 22 drivers: ['12', '16', '44', '63', '6', '1', '3', '81', '41', '30', '5', '10', '27', '87', '55', '23', '31', '77', '43', '11', '18', '14']

{{</details>}}

Unlike the elevation-heavy Red Bull Ring, Silverstone is a test of aerodynamic efficiency and lateral G-forces. The `plot_track` analysis showcases the legendary flow of the circuit.

The primary enemy is the sheer speed. The flat topography means wind direction plays a massive role in car balance, often shifting mid-session and catching out even experienced drivers.

Moreover, the relentless high-speed sweeps subject drivers to immense physical torture. A closer look at the FastF1 data highlights this intensity for the fastest lap of the qualifying: while the bolides touch the 300 km/h threshold on the straights, they simultaneously pull a neck-snapping 6G peak in the corners while maintaining an astonishing 230 km/h.

{{<details title="Show code">}}

```python
fig = utils.plot_track(
    position=Q.laps.pick_fastest().get_telemetry(),
    circuit_info=Q.get_circuit_info(),
    metrics=['lat_g', 'speed']
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_20.json" >}}

## Qualifying

The following chart details the Track and Air Temperatures during Qualifying. Despite the British reputation for rain, the 2026 event saw the tires teetering on the edge of their thermal limits. At Silverstone, high track temperatures are particularly dangerous because they compound the mechanical energy put through the tires in high-speed corners.

This leads to **blistering** on the tread surface as internal heat builds up, or **graining** if the tires slide across the abrasive surface.

{{<details title="Show code">}}

```python
fig = utils.plot_weather_data(Q.weather_data)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_19.json" >}}

Pirellis analysis confirmed that while the circuit's asphalt provides good grip, the high-energy corners generate considerable heat in the tires. Instead of pure mechanical wear, it's the internal thermal stress through Brooklands and Luffield that dictates tire life.

All drivers aside of Bortoleo and Hulkenberg started with the softest compound.

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

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_18.json" >}}

### Qualifying Summary

The next plot shows the evolution of the leading lap time during the qualifying.

In Q1, Isack Hadjar showed Red Bull's raw pace by topping the session ahead of its teammate Verstappen, while Ocon, Colapinto, and both Aston Martin and Cadillac drivers were eliminated.

Q2 saw Antonelli surge to the front, while both Audi drivers, Gasly, Bearman, and the Williams duo failed to make the cut.

In the final Q3 shootout, Kimi Antonelli secured pole position with a 1:28.111, ahead of the Ferrari duo of Charles Leclerc and Lewis Hamilton. Notably, Pierre Gasly received a three-place grid penalty for impeding Stroll in Q1, moving him down to P15 for the start.

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

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_17.json" >}}

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

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_16.json" >}}

Later observations made clear: Mercedes had arrived at Silverstone having used an [unusual but legal power-unit deployment technique in qualifying that was reported to have contributed to Antonelli's](https://www.the-race.com/formula-1/why-mclaren-was-surprised-by-revived-mercedes-engine-trick/) pole position.  

They developed a legal software trick to maximize the electrical power of its F1 engines just before crossing the start-finish line, bypassing the usual power reduction (ramp-down). By intentionally lifting off the throttle briefly right before the timing line, drivers like Kimi Antonelli and George Russell utilize this workaround to optimize ERS power for the lap, which surprised McLaren as a customer team. They did not yet have access to the same approach.

The next plot demonstrates the lift in Antonellis fastest lap in comparison to Piastris fastest lap.

{{<details title="Show code">}}

```python
figures = utils.plot_lap_telemetry_comparison(
    laps=Q.laps,
    circuit_info=Q.get_circuit_info(),
    driver1_code='ANT',
    driver2_code='PIA',
    driver1_lap='fastest',
    driver2_lap='fastest',
    metrics_to_plot=['Speed', 'Throttle'],
    highlight_distance=5754,
    highlight_label='Antonelli lifts'
)
for fig in figures:
    fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_15.json" >}}

## Race

Race day at Silverstone saw 160,000 fans packed into the grandstands. The heat haze over the Hangar Straight signaled a race where tire management would be just as important as engine power.

{{<details title="Show code">}}

```python
R = fastf1.get_session(2026, 'Britain', 'R')
R.load()
```

    events      WARNING 	Correcting user input 'Britain' to 'British Grand Prix'
    core           INFO 	Loading data for British Grand Prix - Race [v3.8.3]
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
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for timing_app_data. Loading data...
    _api           INFO 	Fetching timing app data...
    req            INFO 	Data has been written to cache!
    core           INFO 	Processing timing data...
    req            INFO 	No cached data found for car_data. Loading data...
    _api           INFO 	Fetching car data...
    _api           INFO 	Parsing car data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for position_data. Loading data...
    _api           INFO 	Fetching position data...
    _api           INFO 	Parsing position data...
    _api        WARNING 	Driver 241: Position data is incomplete!
    _api        WARNING 	Driver 242: Position data is incomplete!
    _api        WARNING 	Driver 243: Position data is incomplete!
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for weather_data. Loading data...
    _api           INFO 	Fetching weather data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for race_control_messages. Loading data...
    _api           INFO 	Fetching race control messages...
    req            INFO 	Data has been written to cache!
    core           INFO 	Finished loading data for 22 drivers: ['16', '63', '44', '1', '6', '30', '41', '5', '43', '10', '81', '87', '31', '11', '12', '77', '55', '14', '18', '3', '23', '27']

```python
fig = utils.plot_weather_data(R.weather_data)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_13.json" >}}

The race took place in warm and dry conditions at the Silverstone Circuit, with Pirelli expecting the 52-lap event to be a one-stop race for most of the field. Kimi Antonelli (Mercedes) started from pole position ahead of Charles Leclerc (Ferrari), while Leclerc's teammate Lewis Hamilton and George Russell (Mercedes) occupied the second row.

Pierre Gasly (Alpine) started fifteenth after a three-place grid penalty for impeding during qualifying, while Lance Stroll (Aston Martin) started last following a ten-place grid penalty for the use of additional power unit elements. All 22 drivers initially selected medium tyres, although Fernando Alonso (Aston Martin) stopped briefly during the formation lap and started from the pit lane.

Leclerc made the better launch when the lights went out and moved into the lead, while Hamilton also passed Antonelli to give Ferrari the leading two positions through the opening corners. Russell retained fourth ahead of Isack Hadjar (Red Bull), while the latter's teammate Max Verstappen gained a position to move into sixth. Further back, Oscar Piastri (McLaren) sustained front-wing damage after contact with Liam Lawson (Racing Bulls) at Brooklands and pitted at the end of the opening lap; he ended up circulating outside the points for the rest of the race. Alexander Albon (Williams) also damaged his car after making contact with Oliver Bearman (Haas), spinning the Haas driver at turn 6; Albon received a ten-second time penalty for causing the collision and later retired after Williams kept him circulating to gather data.

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

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_12.json" >}}

{{<details title="Show code">}}

```python
fig = utils.plot_laptime_distribution_per_compound(
    laps=R.laps,
    results=R.results,
    drivers=R.laps['Driver'].unique()
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_11.json" >}}

### Hamilton's Jump Start Analysis

The race report notes that 'Hamilton was noted for a potential false start and subsequently received a five-second time penalty.' Next Plot shows the comparison of Hamiltons first lap and Antonellis first lap to indicate the jump start. Unfortunately, FastF1 data seems not to provide enough detail to detect jump starts as the next plot tries to visualize by plotting the speed at the race start.

{{<details title="Show code">}}

```python
figures = utils.plot_lap_telemetry_comparison(
    laps=R.laps,
    circuit_info=R.get_circuit_info(),
    driver1_code='HAM',
    driver2_code='ANT',
    driver1_lap='1',
    driver2_lap='1',
    metrics_to_plot=['Speed', 'Throttle'],
)
for fig in figures:
    fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_10.json" >}}

At the beginning, Leclerc steadily extended his advantage while Hamilton reported front-left tyre graining and Antonelli closed on the Ferrari. Antonelli passed Hamilton on the inside at Copse on lap 11, moving into second place and beginning his pursuit of Leclerc, who was approximately four seconds ahead. Russell reported unusual downshifts from his gearbox, while Verstappen complained about the deployment and downshift behaviour of his Red Bull as he closed on the Mercedes ahead.

### Hamilton vs. Russell: The Mid-Race Battle

During the middle of the race, Hamilton and Russell fought hard for position. Their duel ended on lap 35 when Russell had to pit with a flat tire. Check out the gap between these two drivers to observe their direct on-track contest and the impact of the puncture.

{{<details title="Show code">}}

```python
fig = utils.plot_gap_between_d1_d2(R.laps, 'HAMlot_track ', 'RUS', event_lap=34, event_label='Russell pit for puncture')
fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_8.json" >}}

### Hamilton's Overtake on Verstappen at Wellington Straight (Lap 38)

Later one of the highlights happened when Hamilton passed Verstappen on the Wellington Straight on lap 38 to move into third place.

We can observe how Hamilton's speed might have peaked higher or for longer, without using DRS, allowing him to gain on and eventually pass Verstappen. The data indicates the on-track action described in the race report, showing Hamilton's superior pace in that section of the track during the overtake.

{{<details title="Show code">}}

```python
# Get telemetry for Hamilton and Verstappen on lap 38
ham_lap38 = R.laps.pick_driver('HAM').pick_lap(38).telemetry
ver_lap38 = R.laps.pick_driver('VER').pick_lap(38).telemetry

# Find a time window for Wellington Straight (approximating from track map and typical lap durations)
start_time_sec = 20
end_time_sec = 35

ham_telemetry_window = ham_lap38[(ham_lap38['Time'] >= pd.Timedelta(seconds=start_time_sec)) &
                                 (ham_lap38['Time'] <= pd.Timedelta(seconds=end_time_sec))]
ver_telemetry_window = ver_lap38[(ver_lap38['Time'] >= pd.Timedelta(seconds=start_time_sec)) &
                                 (ver_lap38['Time'] <= pd.Timedelta(seconds=end_time_sec))]

fig = go.Figure()

fig.add_trace(go.Scatter(x=ham_telemetry_window['Time'], y=ham_telemetry_window['Speed'], mode='lines', name='HAM Speed'))
fig.add_trace(go.Scatter(x=ver_telemetry_window['Time'], y=ver_telemetry_window['Speed'], mode='lines', name='VER Speed'))
fig.add_trace(go.Scatter(x=ham_telemetry_window['Time'], y=ham_telemetry_window['DRS'], mode='lines', name='HAM DRS', line=dict(dash='dot')))
fig.add_trace(go.Scatter(x=ver_telemetry_window['Time'], y=ver_telemetry_window['DRS'], mode='lines', name='VER DRS', line=dict(dash='dot')))


fig.update_layout(
    title='Speed and DRS Usage: Hamilton vs Verstappen (Lap 38 - Wellington Straight)',
    xaxis_title='Time into Lap (seconds)',
    yaxis_title='Speed (km/h)',
    hovermode='x unified'
)
fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_7.json" >}}

### Max Verstappen's Retirement Incident at Stowe (Lap 48)

In Lap 48 Verstappen lost the rear of his car at Stowe and became stranded in the gravel, bringing out the safety car. The telemetry data for Max Verstappen is plotted until  the Stowe corner on this lap to understand the dynamics of the incident.

{{<details title="Show code">}}

```python
figures = utils.plot_lap_telemetry_comparison(
    laps=R.laps,
    circuit_info=R.get_circuit_info(),
    driver1_code='VER',
    driver2_code='VER',
    driver1_lap='46',
    driver2_lap='47',
    metrics_to_plot=['Speed', 'Throttle', 'Brake', 'Gear'],
)

for fig in figures:
    fig.show()

fig = utils.plot_track(
    position=R.laps.pick_driver('VER').pick_lap(47).get_telemetry(),
    circuit_info=R.get_circuit_info(),
    metrics=['lat_g', 'lon_g']
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_6.json" >}}

A sudden drop in speed, combined with erratic G-force readings (especially lateral G-force indicating a loss of grip), and potentially a sudden throttle lift or brake application, would visually confirm the loss of control as described in the race report. This shows the precise moment his race ended due to the incident.

### Antonelli's Technical Degradation: Lap Times After Wheel Cover Failure

Kimi Antonelli suffered a broken left-front wheel shield on lap 41 and made a second stop to remove the damaged bodywork, returning to the track in tenth place and struggling with the handling of the car.

{{<details title="Show code">}}

```python
antonelli_laps = R.laps.pick_driver('ANT')

lap_of_incident = 41

laps_before_incident = antonelli_laps.loc[antonelli_laps['LapNumber'] < lap_of_incident]
laps_after_incident = antonelli_laps.loc[antonelli_laps['LapNumber'] >= lap_of_incident]

# Convert timedelta to seconds for easier plotting
laps_before_incident['LapTimeSeconds'] = laps_before_incident['LapTime'].dt.total_seconds()
laps_after_incident['LapTimeSeconds'] = laps_after_incident['LapTime'].dt.total_seconds()

# Plotting lap times
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=laps_before_incident['LapNumber'],
    y=laps_before_incident['LapTimeSeconds'],
    mode='lines+markers',
    name='Before Incident (Lap Times)',
    marker=dict(color='blue')
))

fig.add_trace(go.Scatter(
    x=laps_after_incident['LapNumber'],
    y=laps_after_incident['LapTimeSeconds'],
    mode='lines+markers',
    name='After Incident (Lap Times)',
    marker=dict(color='red')
))

fig.update_layout(
    title=f'Antonelli Lap Times Before and After Incident on Lap {lap_of_incident}',
    xaxis_title='Lap Number',
    yaxis_title='Lap Time (Seconds)',
    hovermode='x unified'
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_2.json" >}}

This plot clearly illustrates the impact of Kimi Antonelli's car damage on his lap times. Before lap 41, his lap times were relatively consistent and competitive. Immediately after the incident and the subsequent pit stop, his lap times significantly increased, indicating a substantial drop in performance due to the damaged bodywork and handling difficulties, as described in the race report. This visualization quantifies the struggling with the handling.

With Antonelli no longer challenging for the lead, Leclerc built an advantage of approximately 20 seconds over Hamilton. The race was transformed again on lap 48 when Verstappen lost the rear of his car at Stowe and became stranded in the gravel, bringing out the safety car. Leclerc and Hamilton both pitted for fresh soft tyres, while Russell remained on circuit on used medium tyres and moved ahead of Hamilton into second place. Race control initially indicated that the safety car would enter the pit lane to permit a final-lap restart, but the restart was cancelled after a software error. As the message permitting lapped cars to overtake had already been issued, the regulations required the safety car to return to the pits only at the end of the following lap, making a restart before the chequered flag impossible. The field therefore remained behind the safety car until the finish, with Leclerc taking the chequered flag to secure victory ahead of Russell and Hamilton.

Norris finished fourth, ahead of Hadjar in fifth. Lawson and Arvid Lindblad completed a double points finish for Racing Bulls in sixth and seventh, while Gabriel Bortoleto (Audi) took eighth, tripling Audi's points total for the season to that point. Nineteenth-placed Franco Colapinto (Alpine) recovered from a half-spin at Club on the opening lap to finish ninth, with Gasly completing the points positions in tenth after a slow first pit stop. Piastri recovered from his early front-wing change to finish eleventh, ahead of Carlos Sainz Jr. (Williams), Bearman, Ocon and Pérez. Valtteri Bottas (Cadillac), Alonso and Stroll followed Antonelli in the remaining classified positions. Verstappen was classified twentieth despite retiring after completing more than 90% of the race distance, while Albon and Hülkenberg were not classified following their retirements.

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
| 6 | 1.0 | LEC | 93.842659 | 0.693005 | 92.871 | 0.000000 |
| 9 | 2.0 | RUS | 94.096405 | 1.156133 | 92.489 | 0.253746 |
| 4 | 3.0 | HAM | 94.136884 | 0.933808 | 92.309 | 0.294225 |
| 8 | 4.0 | NOR | 94.339195 | 0.945127 | 92.625 | 0.496536 |
| 3 | 5.0 | HAD | 94.560833 | 1.021368 | 92.268 | 0.718174 |
| 5 | 6.0 | LAW | 95.152268 | 0.963507 | 93.648 | 1.309609 |
| 7 | 7.0 | LIN | 95.229071 | 0.970555 | 93.632 | 1.386412 |
| 0 | 8.0 | BOR | 95.379762 | 0.953946 | 93.650 | 1.537103 |
| 1 | 9.0 | COL | 95.643537 | 0.941402 | 94.281 | 1.800877 |
| 2 | 10.0 | GAS | 95.553390 | 0.942297 | 94.179 | 1.710731 |

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

{{< plotly json="/plotly/gp-britain-2026-review/plotly_chart_1.json" >}}

### Conclusion

The final chart, displaying the average lap time and consistency (standard deviation of lap times) for the top 10 finishers, offers valuable insights into each driver's overall race performance. Leclerc, the race winner, not only had one of the fastest average lap times but also demonstrated exceptional consistency, as evidenced by his low standard deviation. This combination of speed and unwavering performance was crucial to his victory.

Russell and Hamilton, finishing second and third respectively, also showed strong pace, but their consistency metrics suggest minor fluctuations, which could be attributed to their mid-race battle, tire management, or the specific incidents they encountered. Drivers like Norris and Hadjar, while fast, might show slightly higher consistency values, indicating moments where their pace varied more.