---
title: 'Git Issue Reporter'
date: '2026-03-27T22:17:16+01:00'
author: 'Giancarlo Rizzo'
draft: true
categories: []
color: '#a09f93'
---

## Prologue
This project based on a noisy problem I am facing quite a lot since I started scraping data from curtin sources. Everytime an API or the structure of a website or service changes my scraper fails. For bigger services I would imlpement some monitoring via Prometheus and Grafana, but in my current project I scraped racing data from the [formula e](https://www.fiaformulae.com/en) website, and even if the API was consistent (was since November 2025) the data itself differs between each season and sometimes between events.

Going through all seasons and events and finding differences manually is quite hard. So I thought about writing a little script that is indicating all columns and datatypes. This is a good solutions for the first engineering, but I realized that I could face braking changes in future too and not only in this project. And because I start to improve and automate my private workflow to be able to keep more track on my projects (especially documenting them), I created the [git-issue-reporter](https://github.com/protogia/git-issue-reporter) for python.

The package has the following features:

- allows publishing to GitHub and GitLab
- allows template-based issues
- avoids and indicates duplicates
- allows custom labeling
- supports reporting of errors and assertions

## How to use it:

First you need to create a fine-grained-token.

_For Github:_ Go to Settings → Developer Settings → Personal Access Tokens

- repository: read and write
- issues: read and write

_For Gitlab:_ In you project go to Settings → Access Tokens

- role: Guest
- scopes: api

Afterwards you can install it via poetry by referencing the git-repository.

```bash
poetry add git+https://github.com/protogia/git-issue-repoter
```

Now you can import and use the utility. Here is an example using the decorator:

```py
from git_issue_reporter import report_on_error

@report_on_error(labels=["parsing", "data"])
def parse_file(filepath):
    with open(filepath) as f:
        return json.load(f)

# If parse_file() raises an exception, an issue is created automatically
parse_file("data.json")
```

And here is another example using the `IssueReporter`-Class-Object in combination with the `__debug__`-flag. (For explaination: If you run your script via `python -O main.py`, then `__debug__` is set to true. It's like an directive in C/CPP)

```py
from git_issue_reporter import IssueReporter

reporter = IssueReporter()

try:
    result = risky_operation()
except Exception as e:
    if __debug__: 
        reporter.report_error(
            exception=e,
            title="Data Processing Failed",
            context={"file": "data.json", "operation": "parse"},
            labels=["error", "data-pipeline"],
        )
```


## When to use this utility

I thought a little bit about this and I think in choosen fuctions it can be usefull if you run a pipeline of multiple services in a test setup. You could easily spot the source of error and how the whole pipeline would react on it. You would have a first documentation consisting of multiple Issues and their traceback. Based on this first experiences you can improve the further monitoring system for the production state.

## About the project

You can find, clone and review the GitHub-repo: [git-issue-reporter](https://github.com/protogia/git-issue-reporter). I am open to any contributions.


