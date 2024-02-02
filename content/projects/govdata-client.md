---
title: 'GovData-client'
date: '2024-01-27T10:37:49+01:00'
author: 'Giancarlo Rizzo'
draft: false
categories: [python, govdata]
color: '#f99157'
---

# Prologue

As a result of the Open Data legislation and the Open Data strategy, requiring authorities of the immediate federal administration to publicly provide collected data. These datasets are now available in the OpenData-Portal of each city like for Braunschweig at [OpenData - Braunschweig](https://opendata.braunschweig.de/).

# Project

You can serve the datasets there and download it manually or just access and analyze them from your codebase. For accessing the OpenData datasets, I have implemented a simple [REST client based on the DKAN Portal API](https://github.com/protogia/govdata). At the time of this publication, it only supports read-only access, allowing the retrieval, download, and processing of datasets from Python.

# Example

To get in touch with it you can try the example in the repository and open it in [google-colab](https://colab.research.google.com/github/protogia/govdata/blob/main/govadata_client_example.ipynb).   
