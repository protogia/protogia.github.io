---
title: 'A portrait made of data: Braunschweig'
date: '2023-10-30T14:12:47+01:00'
author: 'Giancarlo Rizzo'
draft: false
categories: [data-analytics, python, braunschweig]
color: 'var(--base0a)'
---

# Prologue

The city of Braunschweig has undergone significant changes in recent years. I aim to visualize these changes and their perception in the public using various data sources. This blog post marks the beginning of a series that focuses on a data-based portrait of Braunschweig.

To accomplish this, I will initially utilize the following data sources:

[OpenData - Braunschweig](https://opendata.braunschweig.de/)

For accessing the OpenData datasets, I have implemented a simple [REST client based on the DKAN Portal API](https://github.com/protogia/govdata). At the time of this publication, it only supports read-only access, allowing the retrieval, download, and processing of datasets from Python.

GovData/Open Data is the result of Open Data legislation and the Open Data strategy, requiring authorities of the immediate federal administration to publicly provide collected data.

[Google Trends](https://trends.google.com/trends/)

I intend to access historical Google Trends results through the unofficial [pytrends API](https://pypi.org/project/pytrends/). The challenge here will be to systematically draw conclusions based on search terms and relate the results to the OpenData datasets.

# Traceability

For better traceability of my analyses, the data can also be analyzed under [google.colab](https://colab.research.google.com/) itself. The prerequisite is a Google account with age verification. The use of Colab is free as long as no additional packages are purchased.

When using the notebooks, it must be considered that all APIs I use are unofficial implementations, which means changes to the interface of the data sources can lead to malfunctions.