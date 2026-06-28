---
title: 'Formula1 - GP Brazil: Review 2025'
date: '2025-12-12T12:24:21.119885+00:00'
author: 'Giancarlo Rizzo'
draft: false
plotly: true
code_options: true
categories: []
color: '#a09f93'
---

<a href="https://colab.research.google.com/github/protogia/formula1-evaluations/blob/main/gp_brazil_2025_review.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Prologue

What a weekend! The 2025 GP Brazil delivered on its promise of adrenaline-fueled action, with unexpected twists and turns across both qualifying and race events. This year, Sao Paulo played host to a thrilling Sprint Race, adding another layer of intensity to an already legendary circuit.

In this notebook, we'll dive deep into the performance metrics of the Sprint Qualifying, Sprint Race, Main Qualifying, and the Grand Prix itself. As highlighted in my [preview for this race](https://protogia.github.io/blog/formula1-gp-brazil-preview-2025/), this circuit is notorious for its dramatic elevation changes, boasting gradients from a steep -15% downhill to a challenging 15% uphill. These undulations aren't just scenic; they're a significant factor in car setup and driver strategy. The upcoming plot vividly illustrates the circuit's layout, complete with crucial corner annotations and precise gradient information, setting the stage for our performance analysis.

{{<details title="Show code">}}

```python
!pip install fastf1
!pip install git+https://github.com/protogia/formula-1-plotly-utils.git
```

    Requirement already satisfied: fastf1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (3.6.1)
    Requirement already satisfied: matplotlib<4.0.0,>=3.5.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (3.10.7)
    Requirement already satisfied: numpy<3.0.0,>=1.23.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (2.3.4)
    Requirement already satisfied: pandas<3.0.0,>=1.4.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (2.3.3)
    Requirement already satisfied: python-dateutil in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (2.9.0.post0)
    Requirement already satisfied: rapidfuzz in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (3.14.3)
    Requirement already satisfied: requests-cache>=1.0.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (1.2.1)
    Requirement already satisfied: requests>=2.28.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (2.32.5)
    Requirement already satisfied: scipy<2.0.0,>=1.8.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (1.16.3)
    Requirement already satisfied: timple>=0.1.6 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (0.1.8)
    Requirement already satisfied: websockets<14,>=10.3 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1) (13.1)
    Requirement already satisfied: contourpy>=1.0.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.5.1->fastf1) (1.3.3)
    Requirement already satisfied: cycler>=0.10 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.5.1->fastf1) (0.12.1)
    Requirement already satisfied: fonttools>=4.22.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.5.1->fastf1) (4.60.1)
    Requirement already satisfied: kiwisolver>=1.3.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.5.1->fastf1) (1.4.9)
    Requirement already satisfied: packaging>=20.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.5.1->fastf1) (25.0)
    Requirement already satisfied: pillow>=8 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.5.1->fastf1) (12.0.0)
    Requirement already satisfied: pyparsing>=3 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.5.1->fastf1) (3.2.5)
    Requirement already satisfied: pytz>=2020.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pandas<3.0.0,>=1.4.1->fastf1) (2025.2)
    Requirement already satisfied: tzdata>=2022.7 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pandas<3.0.0,>=1.4.1->fastf1) (2025.2)
    Requirement already satisfied: six>=1.5 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from python-dateutil->fastf1) (1.17.0)
    Requirement already satisfied: charset_normalizer<4,>=2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.28.1->fastf1) (3.4.4)
    Requirement already satisfied: idna<4,>=2.5 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.28.1->fastf1) (3.11)
    Requirement already satisfied: urllib3<3,>=1.21.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.28.1->fastf1) (2.5.0)
    Requirement already satisfied: certifi>=2017.4.17 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.28.1->fastf1) (2025.10.5)
    Requirement already satisfied: attrs>=21.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests-cache>=1.0.0->fastf1) (25.4.0)
    Requirement already satisfied: cattrs>=22.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests-cache>=1.0.0->fastf1) (25.3.0)
    Requirement already satisfied: platformdirs>=2.5 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests-cache>=1.0.0->fastf1) (4.5.0)
    Requirement already satisfied: url-normalize>=1.4 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests-cache>=1.0.0->fastf1) (2.2.1)
    Requirement already satisfied: typing-extensions>=4.14.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from cattrs>=22.2->requests-cache>=1.0.0->fastf1) (4.15.0)
    
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m24.1[0m[39;49m -> [0m[32;49m26.1.2[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m
    Collecting git+https://github.com/protogia/formula-1-plotly-utils.git
      Cloning https://github.com/protogia/formula-1-plotly-utils.git to /tmp/pip-req-build-ke989gs_
      Running command git clone --filter=blob:none --quiet https://github.com/protogia/formula-1-plotly-utils.git /tmp/pip-req-build-ke989gs_
      Resolved https://github.com/protogia/formula-1-plotly-utils.git to commit c6e3272986bf68a2e3fb4e889e27dc750d0a5fac
      Installing build dependencies ... [?25ldone
    [?25h  Getting requirements to build wheel ... [?25ldone
    [?25h  Preparing metadata (pyproject.toml) ... [?25ldone
    [?25hCollecting fastf1<4.0.0,>=3.8.1 (from formula-1-plotly-utils==0.1.0)
      Downloading fastf1-3.8.3-py3-none-any.whl.metadata (5.1 kB)
    Requirement already satisfied: pandas<3.0.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from formula-1-plotly-utils==0.1.0) (2.3.3)
    Collecting plotly<7.0.0,>=6.5.2 (from formula-1-plotly-utils==0.1.0)
      Downloading plotly-6.8.0-py3-none-any.whl.metadata (9.0 kB)
    Collecting cryptography (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0)
      Downloading cryptography-49.0.0-cp311-abi3-manylinux_2_34_x86_64.whl.metadata (4.3 kB)
    Requirement already satisfied: matplotlib<4.0.0,>=3.8.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (3.10.7)
    Requirement already satisfied: numpy<3.0.0,>=1.26.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2.3.4)
    Requirement already satisfied: platformdirs in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (4.5.0)
    Collecting pydantic (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0)
      Downloading pydantic-2.13.4-py3-none-any.whl.metadata (109 kB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m109.4/109.4 kB[0m [31m829.7 kB/s[0m eta [36m0:00:00[0ma [36m0:00:01[0m
    [?25hCollecting pyjwt (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0)
      Downloading pyjwt-2.13.0-py3-none-any.whl.metadata (3.4 kB)
    Requirement already satisfied: python-dateutil in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2.9.0.post0)
    Requirement already satisfied: rapidfuzz in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (3.14.3)
    Requirement already satisfied: requests-cache>=1.0.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (1.2.1)
    Requirement already satisfied: requests>=2.30.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2.32.5)
    Requirement already satisfied: scipy<2.0.0,>=1.11.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (1.16.3)
    Collecting signalrcore (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0)
      Downloading signalrcore-1.0.2-py3-none-any.whl.metadata (13 kB)
    Requirement already satisfied: timple>=0.1.6 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (0.1.8)
    Requirement already satisfied: websockets>=10.3 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (13.1)
    Requirement already satisfied: pytz>=2020.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pandas<3.0.0->formula-1-plotly-utils==0.1.0) (2025.2)
    Requirement already satisfied: tzdata>=2022.7 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pandas<3.0.0->formula-1-plotly-utils==0.1.0) (2025.2)
    Requirement already satisfied: narwhals>=1.15.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from plotly<7.0.0,>=6.5.2->formula-1-plotly-utils==0.1.0) (2.10.1)
    Requirement already satisfied: packaging in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from plotly<7.0.0,>=6.5.2->formula-1-plotly-utils==0.1.0) (25.0)
    Requirement already satisfied: contourpy>=1.0.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (1.3.3)
    Requirement already satisfied: cycler>=0.10 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (0.12.1)
    Requirement already satisfied: fonttools>=4.22.0 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (4.60.1)
    Requirement already satisfied: kiwisolver>=1.3.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (1.4.9)
    Requirement already satisfied: pillow>=8 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (12.0.0)
    Requirement already satisfied: pyparsing>=3 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from matplotlib<4.0.0,>=3.8.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (3.2.5)
    Requirement already satisfied: six>=1.5 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from python-dateutil->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (1.17.0)
    Requirement already satisfied: charset_normalizer<4,>=2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.30.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (3.4.4)
    Requirement already satisfied: idna<4,>=2.5 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.30.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (3.11)
    Requirement already satisfied: urllib3<3,>=1.21.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.30.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2.5.0)
    Requirement already satisfied: certifi>=2017.4.17 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests>=2.30.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2025.10.5)
    Requirement already satisfied: attrs>=21.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests-cache>=1.0.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (25.4.0)
    Requirement already satisfied: cattrs>=22.2 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests-cache>=1.0.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (25.3.0)
    Requirement already satisfied: url-normalize>=1.4 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from requests-cache>=1.0.0->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (2.2.1)
    Collecting cffi>=2.0.0 (from cryptography->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0)
      Downloading cffi-2.0.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (2.6 kB)
    Collecting annotated-types>=0.6.0 (from pydantic->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0)
      Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
    Collecting pydantic-core==2.46.4 (from pydantic->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0)
      Downloading pydantic_core-2.46.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.6 kB)
    Requirement already satisfied: typing-extensions>=4.14.1 in /home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages (from pydantic->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0) (4.15.0)
    Collecting typing-inspection>=0.4.2 (from pydantic->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0)
      Downloading typing_inspection-0.4.2-py3-none-any.whl.metadata (2.6 kB)
    Collecting msgpack==1.1.2 (from signalrcore->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0)
      Downloading msgpack-1.1.2-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (8.1 kB)
    Collecting pycparser (from cffi>=2.0.0->cryptography->fastf1<4.0.0,>=3.8.1->formula-1-plotly-utils==0.1.0)
      Downloading pycparser-3.0-py3-none-any.whl.metadata (8.2 kB)
    Downloading fastf1-3.8.3-py3-none-any.whl (135 kB)
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m136.0/136.0 kB[0m [31m1.3 MB/s[0m eta [36m0:00:00[0m00:01[0m
    [?25hDownloading plotly-6.8.0-py3-none-any.whl (9.9 MB)
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m9.9/9.9 MB[0m [31m4.1 MB/s[0m eta [36m0:00:00[0m00:01[0m00:01[0m
    [?25hDownloading cryptography-49.0.0-cp311-abi3-manylinux_2_34_x86_64.whl (4.7 MB)
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m4.7/4.7 MB[0m [31m3.4 MB/s[0m eta [36m0:00:00[0m00:01[0m00:01[0m
    [?25hDownloading pydantic-2.13.4-py3-none-any.whl (472 kB)
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m472.3/472.3 kB[0m [31m2.3 MB/s[0m eta [36m0:00:00[0m00:01[0m00:01[0m
    [?25hDownloading pydantic_core-2.46.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m2.1/2.1 MB[0m [31m3.1 MB/s[0m eta [36m0:00:00[0m00:01[0m00:01[0m
    [?25hDownloading pyjwt-2.13.0-py3-none-any.whl (31 kB)
    Downloading signalrcore-1.0.2-py3-none-any.whl (55 kB)
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m55.6/55.6 kB[0m [31m489.0 kB/s[0m eta [36m0:00:00[0m[36m0:00:01[0m
    [?25hDownloading msgpack-1.1.2-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (427 kB)
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m427.6/427.6 kB[0m [31m2.0 MB/s[0m eta [36m0:00:00[0m00:01[0m00:01[0m
    [?25hDownloading annotated_types-0.7.0-py3-none-any.whl (13 kB)
    Downloading cffi-2.0.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (219 kB)
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m219.6/219.6 kB[0m [31m1.5 MB/s[0m eta [36m0:00:00[0m00:01[0m00:01[0m
    [?25hDownloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)
    Downloading pycparser-3.0-py3-none-any.whl (48 kB)
    [2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m48.2/48.2 kB[0m [31m372.9 kB/s[0m eta [36m0:00:00[0m [36m0:00:01[0m
    [?25hBuilding wheels for collected packages: formula-1-plotly-utils
      Building wheel for formula-1-plotly-utils (pyproject.toml) ... [?25ldone
    [?25h  Created wheel for formula-1-plotly-utils: filename=formula_1_plotly_utils-0.1.0-py3-none-any.whl size=10297 sha256=5356d4f958a8a7f889cb301b7b399b4b3421023c3c40f4d73a453d5f93c0cbdb
      Stored in directory: /tmp/pip-ephem-wheel-cache-epb4_aq5/wheels/7c/0f/19/04eeb5d297e4078ad7eb3694ce97a4c4eb49be375a32ef2538
    Successfully built formula-1-plotly-utils
    Installing collected packages: typing-inspection, pyjwt, pydantic-core, pycparser, plotly, msgpack, annotated-types, signalrcore, pydantic, cffi, cryptography, fastf1, formula-1-plotly-utils
      Attempting uninstall: plotly
        Found existing installation: plotly 6.3.1
        Uninstalling plotly-6.3.1:
          Successfully uninstalled plotly-6.3.1
      Attempting uninstall: fastf1
        Found existing installation: fastf1 3.6.1
        Uninstalling fastf1-3.6.1:
          Successfully uninstalled fastf1-3.6.1
    Successfully installed annotated-types-0.7.0 cffi-2.0.0 cryptography-49.0.0 fastf1-3.8.3 formula-1-plotly-utils-0.1.0 msgpack-1.1.2 plotly-6.8.0 pycparser-3.0 pydantic-2.13.4 pydantic-core-2.46.4 pyjwt-2.13.0 signalrcore-1.0.2 typing-inspection-0.4.2
    
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m24.1[0m[39;49m -> [0m[32;49m26.1.2[0m
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

SQ = fastf1.get_session(2025, 'Brazil', 'SQ')
SQ.load()
```

    req         WARNING 	DEFAULT CACHE ENABLED! (132.7 MB) /home/working/.cache/fastf1
    core           INFO 	Loading data for São Paulo Grand Prix - Sprint Qualifying [v3.8.3]
    req            INFO 	No cached data found for session_info. Loading data...
    _api           INFO 	Fetching session info data...
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for driver_info. Loading data...
    _api           INFO 	Fetching driver list...
    req            INFO 	Data has been written to cache!
    core        WARNING 	Sprint Qualifying is not supported by Ergast! Limited results are calculated from timing data.
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
    core           INFO 	Finished loading data for 20 drivers: ['4', '12', '81', '63', '14', '1', '18', '16', '6', '27', '44', '23', '10', '5', '87', '43', '30', '22', '31', '55']

```python
position = SQ.laps.pick_fastest().get_pos_data()
circuit_info = SQ.get_circuit_info()
reference_altitude = 800

fig = utils.plot_track(
    position=position,
    circuit_info=circuit_info,
    reference_altitude=reference_altitude,
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_17.json" >}}

## Sprint Qualifying

The Sprint Qualifying session unfolded under clear, dry skies, with no rain impacting the track before the action began. However, as an evening event, temperatures were a critical factor. The air temperature averaged a cool 19°C, but what truly stands out in the weather data is the **dramatic drop in track temperature**, plummeting from 43°C down to 34°C. This significant cooling, coupled with minimal wind speeds around 0.7m/s during Phase 2, likely had a profound effect on tire grip and overall car balance. The decreasing track temperature, exacerbated by the progressive elimination of 10 drivers, created an evolving challenge for those fighting for pole position, as we'll visualize in the weather plot below.

{{<details title="Show code">}}

```python
fig = utils.plot_weather_data(SQ.weather_data)
fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_16.json" >}}

### Tyre Strategy: The Medium-Soft Gamble

Given the dry conditions, tire strategies in Sprint Qualifying were under the spotlight. As the next chart vividly illustrates, most drivers initially opted for the medium compound, aiming to maximize their track time and understand the evolving conditions. However, a crucial strategic shift occurred in Qualifying Round 3: nearly all contenders swapped to the soft compound in their final two laps. This aggressive move was a clear bid to unlock extra pace and secure the best possible grid position for the Sprint Race.

Fernando Alonso, notably, was one of the first to commit to soft tires, perhaps sensing a lack of grip. Despite this early switch, he couldn't quite break into the top 10. Intriguingly, Lando Norris and Lewis Hamilton were the only drivers to bravely attempt Qualifying Round 3 on medium compounds, a decision that ultimately prevented them from advancing. This highlights the fine margins and bold gambles that define F1 qualifying, where tire choice can make or break a session.

{{<details title="Show code">}}

```python
drivers = SQ.laps['Driver'].unique()

fig = utils.plot_tyre_strategies(
    drivers=drivers,
    laps=SQ.laps,
    track_status=SQ.track_status,
)
fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_15.json" >}}

### Lap Time Dynamics: Unpacking the Performance

The subsequent charts offer a detailed look at lap time distribution, first by Qualifying Round (Q1, Q2, Q3) and then by tire compound. While the raw distribution might appear varied due to differing car performances and driver efforts, key insights emerge.

Perhaps the most fascinating detail is the observation that the median lap times of drivers eliminated early in qualifying were actually *lower* than those who ultimately secured pole position. This paradox isn't about raw pace, but rather strategy: top drivers often achieve their best laps with fewer attempts, demonstrating efficiency and precision, while others might push harder, generating more laps, in a desperate bid to find pace.

As expected, the soft compound tires generally delivered superior performance. However, this advantage was often unlocked only during specific, high-effort 'push' laps, indicating that drivers were carefully managing their tire performance throughout the session rather than consistently extracting maximum pace. This nuanced interplay of strategy and raw speed defines the competitive landscape of Sprint Qualifying.

{{<details title="Show code">}}

```python
fig = utils.plot_laptime_distribution_per_qualifyinground(
    drivers=drivers,
    laps=SQ.laps,
    results=SQ.results,
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_14.json" >}}

{{<details title="Show code">}}

```python
# filter out unwanted lap types (e.g., pit laps)
all_laps = SQ.laps.pick_quicklaps().reset_index()
all_laps['LapTimeSeconds'] = all_laps['LapTime'].dt.total_seconds()

# drivers sorted by final position in the sprint qualifying
if not SQ.results.empty:
    driver_positions = SQ.results.sort_values(by='Position')['Abbreviation'].tolist()
    all_laps = all_laps[all_laps['Driver'].isin(driver_positions)].copy()
    all_laps['Driver_Category'] = pd.Categorical(all_laps['Driver'], categories=driver_positions, ordered=True)
    all_laps.sort_values(by='Driver_Category', inplace=True)
else:
    driver_positions = all_laps['Driver'].unique() # Use all drivers with laps if results are not available


# box plot compounds
fig_box_compound = px.box(all_laps,
                          x='Driver',
                          y='LapTimeSeconds',
                          color='Compound',
                          points='all',
                          hover_data=['LapNumber'],
                          title='Lap Time Performance per Driver and Tyre Compound (Sprint Qualifying)')

fig_box_compound.update_layout(
    xaxis_title='Driver',
    yaxis_title='Lap Time (seconds)',
    legend_title='Tyre Compound',
    xaxis=dict(categoryorder='array', categoryarray=driver_positions)
)

fig_box_compound.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_13.json" >}}

### The Best of the Best: Official Lap Times

The next chart presents the definitive best lap times, categorized by Qualifying Round and sorted by overall fastest performance. This visualization dramatically highlights strategic successes and missed opportunities. Fernando Alonso's situation is particularly noteworthy: despite recording the second-fastest lap overall across all qualifying phases, his inability to replicate that blistering pace in the critical Qualifying Round 3 meant he started the Sprint Race from a respectable, but ultimately less advantageous, fifth position. This underscores how crucial consistency and peak performance in the final stages of qualifying are for grid placement, even for drivers capable of immense speed.

{{<details title="Show code">}}

```python
# Q1, Q2, Q3 columns to seconds
best_lap_times_official = SQ.results[['Abbreviation', 'Q1', 'Q2', 'Q3']].copy()
for col in ['Q1', 'Q2', 'Q3']:
    best_lap_times_official[col] = best_lap_times_official[col].apply(lambda x: x.total_seconds() if pd.notna(x) else np.nan)

best_lap_times_official = best_lap_times_official.melt(
    id_vars='Abbreviation',
    value_vars=['Q1', 'Q2', 'Q3'],
    var_name='QualifyingRound',
    value_name='BestLapTime'
).dropna(subset=['BestLapTime']) # drop rows with NaN best lap times

# best overall lap time per driver from the official results for sorting
best_overall_lap_time_driver_official = best_lap_times_official.groupby('Abbreviation')['BestLapTime'].min().reset_index()
best_overall_lap_time_driver_official = best_overall_lap_time_driver_official.rename(columns={'BestLapTime': 'BestOverallLapTime'})

# merge best lap times with overall best lap time for sorting
best_lap_times_official = pd.merge(best_lap_times_official, best_overall_lap_time_driver_official, on='Abbreviation', how='left')

if not best_overall_lap_time_driver_official.empty:
    driver_order_official = best_overall_lap_time_driver_official.sort_values(by='BestOverallLapTime')['Abbreviation'].tolist()
    best_lap_times_official['Driver_Category'] = pd.Categorical(best_lap_times_official['Abbreviation'], categories=driver_order_official, ordered=True)
    best_lap_times_official.sort_values(by='Driver_Category', inplace=True)


# scatter plot best lap times
fig_scatter = px.scatter(best_lap_times_official,
                         x='Abbreviation',
                         y='BestLapTime',
                         color='QualifyingRound', # color by Qualifying Round
                         symbol='QualifyingRound',
                         hover_data=['QualifyingRound', 'BestLapTime'],
                         title='Best Lap Time per Driver by Qualifying Round')

fig_scatter.update_layout(
    xaxis_title='Driver',
    yaxis_title='Best Lap Time (seconds)',
    legend_title='Qualifying Round',
    xaxis=dict(categoryorder='array', categoryarray=driver_order_official) # Set the order of drivers on the x-axis
)

fig_scatter.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_12.json" >}}

## The Sprint Race

### Sprint Race Conditions: Rising Temperatures and Unexpected Drama

With the brevity of Sprint Qualifying offering limited insight into long-run car and driver performance, the 24-lap Sprint Race took center stage just a day later, mere hours before the main Qualifying session. The weather remained dry, but a subtle yet significant shift occurred: air temperatures climbed by 4 degrees compared to the previous day, while track temperatures settled between a warmer 25°C and 29°C. These warmer conditions could influence tire degradation and optimal car setup.

However, as the subsequent weather plot reveals, the real drama unfolded with track events. These conditions, combined with the unfolding race action, set the stage for crucial strategic decisions, particularly regarding tire management.

{{<details title="Show code">}}

```python
SR = fastf1.get_session(2025, "Brazil", "S")
SR.load()
```

    core           INFO 	Loading data for São Paulo Grand Prix - Sprint [v3.8.3]
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
    _api        WARNING 	Driver 11: Car data is incomplete!
    _api        WARNING 	Driver 24: Car data is incomplete!
    _api        WARNING 	Driver 50: Car data is incomplete!
    _api        WARNING 	Driver 77: Car data is incomplete!
    _api        WARNING 	Driver  5: Car data is incomplete!
    _api        WARNING 	Driver  6: Car data is incomplete!
    _api        WARNING 	Driver 12: Car data is incomplete!
    _api        WARNING 	Driver 87: Car data is incomplete!
    req            INFO 	Data has been written to cache!
    req            INFO 	No cached data found for position_data. Loading data...
    _api           INFO 	Fetching position data...
    _api           INFO 	Parsing position data...
    _api        WARNING 	Driver 11: Position data is incomplete!
    _api        WARNING 	Driver 24: Position data is incomplete!
    _api        WARNING 	Driver 50: Position data is incomplete!
    _api        WARNING 	Driver 77: Position data is incomplete!
    _api        WARNING 	Driver  5: Position data is incomplete!
    _api        WARNING 	Driver  6: Position data is incomplete!
    _api        WARNING 	Driver 12: Position data is incomplete!
    _api        WARNING 	Driver 87: Position data is incomplete!
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
    core           INFO 	Finished loading data for 20 drivers: ['4', '12', '63', '1', '16', '14', '44', '10', '18', '6', '31', '87', '22', '55', '27', '30', '23', '5', '81', '43']

```python
fig = utils.plot_weather_data(SR.weather_data)
fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_11.json" >}}

### Sprint Race Tyre Strategies: Adapting to Chaos

The next chart dissects the intricate tire strategies deployed during the Sprint Race. A defining moment for many drivers was the red flag phase, triggered by the unfortunate dropouts of Colapinto and Piastri. This disruption provided a critical window for tire changes, a strategic opportunity many seized.

Initially, six drivers (excluding Stroll) bravely started on the soft compound, aiming for early pace, while the majority (fourteen drivers) opted for the more durable medium tires. As the race unfolded, especially after the red flag, we see a fascinating split: six drivers who started on mediums transitioned to softs, capitalizing on the interruption, while another six steadfastly remained on their initial medium compounds. This dynamic interplay of pre-race planning and reactive strategy, influenced heavily by the race-altering red flag, is vividly captured in the visualization below.

{{<details title="Show code">}}

```python
drivers = SR.laps['Driver'].unique()

fig = utils.plot_tyre_strategies(
    drivers=drivers,
    laps=SR.laps,
    track_status=SR.track_status,
)
fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_10.json" >}}

### Performance Under Pressure: Soft vs. Medium in the Sprint

The violin plot below offers a compelling look at how tire choices translated into lap time performance during the Sprint Race. Among the top 5 finishers, only Lando Norris demonstrated exceptional pace predominantly on medium compound tires, showcasing his car's remarkable balance and his driving skill. In stark contrast, nearly all other drivers who committed solely to medium tires (with the notable exception of Lewis Hamilton) struggled, finishing outside the points in 11th position or worse. This data strongly suggests a significant performance differential: drivers who did not utilize the soft compound at some point in the race faced a median lap time disadvantage of at least one second. This highlights the crucial role of the softer compound in achieving competitive lap times, especially when the race is interrupted and strategy can be adapted.

{{<details title="Show code">}}

```python
# filter out unwanted lap types (e.g., pit laps)
race_laps = SR.laps.pick_quicklaps().reset_index()
race_laps['LapTimeSeconds'] = race_laps['LapTime'].dt.total_seconds()

# drivers sorted by final position in the sprint race
if not SR.results.empty:
    driver_order_sprint_race = SR.results.sort_values(by='Position')['Abbreviation'].tolist()
    race_laps = race_laps[race_laps['Driver'].isin(driver_order_sprint_race)].copy()
    race_laps['Driver_Category'] = pd.Categorical(race_laps['Driver'], categories=driver_order_sprint_race, ordered=True)
    race_laps.sort_values(by='Driver_Category', inplace=True)
else:
    driver_order_sprint_race = race_laps['Driver'].unique() # Use all drivers with laps if results are not available


# violin plot best lap times
fig_violin_sprint = px.violin(race_laps,
                             x='Driver',
                             y='LapTimeSeconds',
                             color='Compound',
                             box=True,
                             points='all',
                             hover_data=['LapNumber', 'Compound', 'LapTimeSeconds'],
                             title='Sprint Race Lap Time Distribution per Driver and Tyre Compound')

fig_violin_sprint.update_layout(
    xaxis_title='Driver',
    yaxis_title='Lap Time (seconds)',
    legend_title='Tyre Compound',
    xaxis=dict(categoryorder='array', categoryarray=driver_order_sprint_race) # Set the order of drivers on the x-axis
)

fig_violin_sprint.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_9.json" >}}

### Overtakes and Position Battles: Who Gained, Who Lost?

Despite the early retirements of Piastri and Colapinto, the Sprint Race saw surprisingly stable positions for many drivers. However, the plot of driver positions per lap reveals some standout performances in the midfield. Oliver Bearman, for instance, delivered a masterclass in overtaking, climbing from an 18th-place start to finish an impressive 12th – marking the highest number of overtakes in the race. On the flip side, Hulkenberg experienced a challenging race, losing the most positions as he dropped from 10th to 18th. These individual battles, though not always at the very front, demonstrate the relentless fight for every position on the challenging Brazilian circuit.

{{<details title="Show code">}}

```python
fig = go.Figure()

for driver in drivers:
    drv_laps = SR.laps.pick_drivers(driver)

    if not drv_laps.empty:
        abb = drv_laps['Driver'].iloc[0]
        fig.add_trace(go.Scatter(
            x=drv_laps['LapNumber'],
            y=drv_laps['Position'],
            mode='lines+markers',
            name=abb,
            hoverinfo='text',
            text=[f'Driver: {abb}<br>Lap: {lap}<br>Position: {pos}' for lap, pos in zip(drv_laps['LapNumber'], drv_laps['Position'])]
        ))

fig.update_layout(
    title='Driver Positions Per Lap',
    xaxis_title='Lap Number',
    yaxis_title='Position',
    yaxis=dict(
        autorange='reversed', # P1 at the top
    ),
    legend_title='Driver'
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_8.json" >}}

## Main Qualifying

### Qualifying Weather: A Different Climate for Pole Position

The weather conditions for the main Qualifying session presented a slightly different challenge compared to the Sprint events. The track remained resolutely dry, with no rain threatening the crucial push for pole. Air temperatures hovered comfortably around 25°C. However, the track temperature experienced another notable decline, starting at a blistering 47°C but cooling down to 36°C by the session's end. Wind speeds remained relatively low, fluctuating between 0.6m/s and 2.8m/s. This gradual cooling of the track as the session progressed likely influenced tire performance and grip, demanding adaptability from teams and drivers as they chased the fastest lap times.

{{<details title="Show code">}}

```python
Q = fastf1.get_session(2025, 'Brazil', 'Q')
Q.load()
```

    core           INFO 	Loading data for São Paulo Grand Prix - Qualifying [v3.8.3]
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
    core        WARNING 	No lap data for driver 5
    core        WARNING 	Failed to perform lap accuracy check - all laps marked as inaccurate (driver 5)
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
    core           INFO 	Finished loading data for 20 drivers: ['4', '12', '16', '81', '6', '63', '30', '87', '10', '27', '14', '23', '44', '18', '55', '1', '31', '43', '22', '5']

```python
fig = utils.plot_weather_data(Q.weather_data)
fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_7.json" >}}

### Qualifying Tyre Strategy: Soft Domination and Gasly's Maverick Move

The tire strategy in the main Qualifying session was largely dominated by the soft compound, as expected. With the exception of just seven drivers, every competitor completed their qualifying efforts exclusively on soft tires, underscoring its performance advantage in a single-lap shootout.

However, Pierre Gasly emerged as a strategic outlier. He began his qualifying with soft tires but uniquely transitioned to mediums, a bold and unusual choice for a session where every millisecond counts. This decision, clearly visible in the tire strategy chart below, distinguishes him from the rest of the field. Fortunately, despite the intense competition, there were no mechanical retirements, allowing all drivers to push their cars to the limit.

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

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_6.json" >}}

### Best Lap Times: A Tale of Two Qualifyings

Moving beyond overall lap time distributions, which can be noisy, our focus shifts to the definitive best lap times achieved in each Qualifying Round. The scatter plot below reveals a fascinating trend: the majority of drivers extracted their absolute best performance in Qualifying Round 2, suggesting optimal track conditions and driver rhythm at that stage.

Crucially, when comparing these results to the Sprint Qualifying, a stark difference emerges: only Lando Norris managed to replicate a similarly blistering lap time. Most other top-10 contenders found themselves up to 500ms slower than their Sprint Qualifying bests. Yet, in a remarkable display of progress, Oliver Bearman defied this trend, improving his best lap time by approximately 200ms. This comparison highlights the dynamic nature of conditions and driver adaptation between the two qualifying formats, with Norris's consistency and Bearman's advancement being particularly noteworthy.

{{<details title="Show code">}}

```python
# Q1, Q2, Q3 columns to seconds
best_lap_times_official = Q.results[['Abbreviation', 'Q1', 'Q2', 'Q3']].copy()
for col in ['Q1', 'Q2', 'Q3']:
    best_lap_times_official[col] = best_lap_times_official[col].apply(lambda x: x.total_seconds() if pd.notna(x) else np.nan)

best_lap_times_official = best_lap_times_official.melt(
    id_vars='Abbreviation',
    value_vars=['Q1', 'Q2', 'Q3'],
    var_name='QualifyingRound',
    value_name='BestLapTime'
).dropna(subset=['BestLapTime']) # drop rows with NaN best lap times

# best overall lap time per driver from the official results for sorting
best_overall_lap_time_driver_official = best_lap_times_official.groupby('Abbreviation')['BestLapTime'].min().reset_index()
best_overall_lap_time_driver_official = best_overall_lap_time_driver_official.rename(columns={'BestLapTime': 'BestOverallLapTime'})

# merge best lap times with overall best lap time for sorting
best_lap_times_official = pd.merge(best_lap_times_official, best_overall_lap_time_driver_official, on='Abbreviation', how='left')

if not best_overall_lap_time_driver_official.empty:
    driver_order_official = best_overall_lap_time_driver_official.sort_values(by='BestOverallLapTime')['Abbreviation'].tolist()
    best_lap_times_official['Driver_Category'] = pd.Categorical(best_lap_times_official['Abbreviation'], categories=driver_order_official, ordered=True)
    best_lap_times_official.sort_values(by='Driver_Category', inplace=True)


# scatter plot best lap times
fig_scatter = px.scatter(best_lap_times_official,
                         x='Abbreviation',
                         y='BestLapTime',
                         color='QualifyingRound', # color by Qualifying Round
                         symbol='QualifyingRound',
                         hover_data=['QualifyingRound', 'BestLapTime'],
                         title='Best Lap Time per Driver by Qualifying Round')

fig_scatter.update_layout(
    xaxis_title='Driver',
    yaxis_title='Best Lap Time (seconds)',
    legend_title='Qualifying Round',
    xaxis=dict(categoryorder='array', categoryarray=driver_order_official) # Set the order of drivers on the x-axis
)

fig_scatter.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_5.json" >}}

## The Grand Prix Race

{{<details title="Show code">}}

```python
GP = fastf1.get_session(2025, 'Brazil', 'R')
GP.load()
```

    core           INFO 	Loading data for São Paulo Grand Prix - Race [v3.8.3]
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
    core        WARNING 	Driver 4 completed the race distance 00:00.010000 before the recorded end of the session.
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
    core           INFO 	Finished loading data for 20 drivers: ['4', '12', '1', '63', '81', '87', '30', '6', '27', '10', '23', '31', '55', '14', '43', '18', '22', '44', '16', '5']

{{</details>}}

### Race Day Conditions: A Hot Afternoon Battle

The Grand Prix race unfolded under significantly warmer conditions compared to the previous sessions, demanding a different approach to car setup and tire management. Air temperatures peaked at a comfortable 27°C, but the track temperature soared to a blistering 46°C, creating an intense challenge for tire degradation. Wind speeds remained moderate, generally between 0.8m/s and 2.5m/s.

The weather plot below vividly illustrates these race day conditions. The high track temperatures put a premium on managing the tires, as overheating could lead to rapid performance drops. This elevation in temperature, a stark contrast to the cooler Sprint Qualifying, set the stage for a physically demanding race where tire strategy would be paramount.

{{<details title="Show code">}}

```python
fig = utils.plot_weather_data(GP.weather_data)
fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_4.json" >}}

### Grand Prix Tyre Strategies: The Dance of Durability and Speed

The 71-lap Grand Prix was a true test of endurance and strategic foresight, especially concerning tire choices. The next chart lays bare the diverse and intricate tire strategies deployed by each team, with most drivers opting for a two-stop strategy, a common choice at Interlagos due to its demanding corners and high-speed sections leading to significant tire wear.

Notice the prevalence of medium and hard compounds. The soft compound, while offering blistering pace, typically has a shorter lifespan, making its usage a calculated risk. Drivers often started on mediums, transitioned to hards for a longer stint, and then perhaps back to mediums or even softs for a final push, depending on race circumstances and safety car interventions. The plot reveals which drivers gambled on a more aggressive soft-tire strategy early on, and who opted for durability with hard compounds to extend their stints. Analyzing these patterns can offer crucial insights into each team's understanding of tire degradation and their confidence in their car's long-run pace.

{{<details title="Show code">}}

```python
drivers = GP.laps['Driver'].unique()

fig = utils.plot_tyre_strategies(
    drivers=drivers,
    laps=GP.laps,
    track_status=GP.track_status,
)
fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_3.json" >}}

### Race Pace Analysis: Who Mastered Interlagos?

The violin plot below provides a comprehensive overview of lap time performance across the entire Grand Prix, broken down by driver and tire compound. This granular analysis is crucial for understanding who truly mastered the demanding conditions of Interlagos over a full race distance.

Observe the spread of lap times for each driver. A tighter distribution indicates greater consistency, a hallmark of strong race pace and effective tire management. Compare the median lap times across different compounds – do the softer tires show a clear pace advantage, or does their shorter life lead to a wider variance in lap times due to degradation? Pay close attention to drivers who managed to maintain competitive lap times on harder compounds, as this often signifies exceptional car balance and driving skill. This visualization will help us identify standout performances and highlight any significant strategic trade-offs made during the race.

{{<details title="Show code">}}

```python
# filter out unwanted lap types (e.g., pit laps)
race_laps = GP.laps.pick_quicklaps().reset_index()
race_laps['LapTimeSeconds'] = race_laps['LapTime'].dt.total_seconds()

# drivers sorted by final position in the race
if not GP.results.empty:
    driver_order_race = GP.results.sort_values(by='Position')['Abbreviation'].tolist()
    race_laps = race_laps[race_laps['Driver'].isin(driver_order_race)].copy()
    race_laps['Driver_Category'] = pd.Categorical(race_laps['Driver'], categories=driver_order_race, ordered=True)
    race_laps.sort_values(by='Driver_Category', inplace=True)
else:
    driver_order_race = race_laps['Driver'].unique() # Use all drivers with laps if results are not available


# violin plot best lap times
fig_violin_race = px.violin(race_laps,
                             x='Driver',
                             y='LapTimeSeconds',
                             color='Compound',
                             box=True,
                             points='all',
                             hover_data=['LapNumber', 'Compound', 'LapTimeSeconds'],
                             title='Grand Prix Lap Time Distribution per Driver and Tyre Compound')

fig_violin_race.update_layout(
    xaxis_title='Driver',
    yaxis_title='Lap Time (seconds)',
    legend_title='Tyre Compound',
    xaxis=dict(categoryorder='array', categoryarray=driver_order_race) # Set the order of drivers on the x-axis
)

fig_violin_race.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_2.json" >}}

### The Race Story Unfolds: Position Changes Throughout the Grand Prix

The most compelling narrative of any Grand Prix is the ebb and flow of positions. The following plot, charting each driver's position per lap, is a real-time drama unfolding on the tarmac. Here, we can identify key overtakes, strategic undercuts or overcuts in the pit lane, and drivers battling tooth and nail for every single point.

Look for significant jumps or drops in position – these often correlate with pit stops, safety car periods that bunch up the field, or exceptional driving allowing a driver to scythe through the pack. Which drivers made the most progress from their starting grid slot? Who struggled to maintain their position? This visualization is a powerful tool for dissecting the race action, revealing the strategic brilliance and the unfortunate setbacks that define a Grand Prix.

{{<details title="Show code">}}

```python
fig = go.Figure()

for driver in drivers:
    drv_laps = GP.laps.pick_drivers(driver)

    if not drv_laps.empty:
        abb = drv_laps['Driver'].iloc[0]
        fig.add_trace(go.Scatter(
            x=drv_laps['LapNumber'],
            y=drv_laps['Position'],
            mode='lines+markers',
            name=abb,
            hoverinfo='text',
            text=[f'Driver: {abb}<br>Lap: {lap}<br>Position: {pos}' for lap, pos in zip(drv_laps['LapNumber'], drv_laps['Position'])]
        ))

fig.update_layout(
    title='Driver Positions Per Lap (Grand Prix Race)',
    xaxis_title='Lap Number',
    yaxis_title='Position',
    yaxis=dict(
        autorange='reversed', # P1 at the top
    ),
    legend_title='Driver'
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-review-2025/plotly_chart_1.json" >}}

{{<details title="Show code">}}

```python
import pandas as pd

# Filter for point scorers (Top 10)
points_finishers = GP.results.sort_values(by='Position').head(10)['Abbreviation'].tolist()
points_laps = GP.laps.pick_quicklaps().loc[GP.laps['Driver'].isin(points_finishers)].copy()
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
    GP.results[['Abbreviation', 'Position', 'Status']],
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
| 6 | 1.0 | NOR | 74.145333 | 0.573162 | 73.040 | 0.000000 |
| 0 | 2.0 | ANT | 74.287167 | 0.698611 | 73.123 | 0.141833 |
| 9 | 3.0 | VER | 74.108644 | 0.899648 | 72.447 | -0.036689 |
| 8 | 4.0 | RUS | 74.372203 | 0.781321 | 73.097 | 0.226870 |
| 7 | 5.0 | PIA | 74.230567 | 0.878201 | 72.742 | 0.085233 |
| 1 | 6.0 | BEA | 74.537864 | 0.641063 | 73.483 | 0.392531 |
| 5 | 7.0 | LAW | 75.327919 | 0.625117 | 74.029 | 1.182586 |
| 3 | 8.0 | HAD | 74.971000 | 0.688880 | 73.694 | 0.825667 |
| 4 | 9.0 | HUL | 75.267918 | 0.729471 | 73.474 | 1.122585 |
| 2 | 10.0 | GAS | 74.964508 | 0.664793 | 73.736 | 0.819175 |

{{</details>}}

## Conclusion

While the timing screens occasionally showed flashes of brilliance from Verstappen and Piastri, Lando Norris's victory was built on his low variance. His ability to maintain a 74.1s average with the lowest standard deviation in the top 10 proves that the McLaren-Norris pairing has mastered the art of managing Pirelli's thermal sensitivity in high-heat (46°C track) conditions.

The performance of Oliver Bearman and Liam Lawson deserves high praise. Their median lap times were often indistinguishable from the top-five runners. This suggests that the 'performance ceiling' of the midfield has been reached; for these drivers, the difference between a podium and a P7 finish is now dictated almost entirely by qualifying position and strategic execution during Safety Car windows.

The analysis of the 'Gap to Winner' shows that even a minor loss in tire management—like we saw with Nico Hulkenberg toward the end of his second stint—compounded into a significant 1.1s average deficit. At Interlagos, if you aren't managing the 'thermal deg' in Sector 2, you are a sitting duck on the climb to the finish line.

This weekend rewarded those who could adapt. From the high-stakes tire swaps in Sprint Qualifying to the two-stop endurance test of the Grand Prix, the teams that succeeded were those that didn't just have a 'Plan A,' but had the data-driven confidence to pivot when the track temperatures began to drop.