---
title: 'Convert Jupyter Notebooks to Markdown-Blogposts for Hugo'
date: '2025-01-06T13:25:33+01:00'
author: 'Giancarlo Rizzo'
draft: true
categories: []
color: '#f99157'
titleimage: 'content/projects/titleimages/CHANGEME.png'
---

## Prologue
In order to target my goal about publishing blogposts about evaluations I made with jupyter notebooks I discovered the need of creating a simple routine to automatically convert notebooks into markdown-files for this webblog.

## Workflow and Structure
The best ready-to-use package to convert notebooks into markdown-files I found is nbcovert. Because publishing a website with Hugo needs further meta-informations like creation-date, title, and more I needed to use nbconvert as package within a python-script to execute some basic operations for my hugo-project-structure.

Here is an overview of the planed hugo-project-structure:

```

/-
-|-/content
   |-/projects
   |-/evaluations
     |-/notebook-example-1.md
     |-/notebook-example-1.md
-|-/notebooks
   |-/notebook-example-1.ipynb
   |-/notebook-example-2.ipynb

```

As you can see i have a folder `notebooks` in which i add `.ipynb`-files which i want to convert and move into the `/content/evaluations/`-folder. Because I can not guaranty if I keep the structure that simple i want to add meta-informations depending on the destination of the created markdown-file. A notebook which will be converted into a `md`-file in the `/content/evaluations/`-folder should get different metainformations then another which will be converted and stored into the `/content/projects/`-folder.

Furthermore the image-sources of source-notebook have to be stored into a static-folder (in my case: `/static/img/<notebook-filename>/img_xy.png`) and the hyperlinks within the markdown-file have to be replaced with the targeted static files.

## Project and Future Adjustments

You can find the sourcecode for this [nb2hugo-markdown](https://github.com/protogia/nb2hugo-markdown) on GitHub. Right now I can use this utility in a suitable way but i want to add a feature to adjust the colors of the output diagrams according to my website colorscheme.