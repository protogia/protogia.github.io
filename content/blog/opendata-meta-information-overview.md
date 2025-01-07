---
title: opendata meta information overview
date: '2025-01-07T15:23:14.448639+00:00'
author: 'Giancarlo Rizzo'
draft: true
categories: []
color: '#ffcc66'
titleimage: 'content/blog/titleimages/CHANGEME.png'
---

<a href="https://colab.research.google.com/github/protogia/Braunschweig/blob/main/opendata-meta-information-overview.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

This notebook is a try to analyze the opendata-sources of Braunschweig. It uses an python-based govdata-client to extract some informations from the provided metdata

First install the *govdata-client*


```python
!pip install govdata
```

Now import and initialize an **DKANPortalClient** for your city of interest. Test if your cityclient can establish a connection!


```python
from govdata import DKANPortalClient

cityclient = DKANPortalClient(city="braunschweig", apiversion=3)
```


```python
cityclient.connectiontest()
```




    True



List available packages for your city. A package represents a topic like *infrastructure*, *traffic*, etc.


```python
cityclient.get_packages()
```

To take a look at metadata from a specific packaged provide the target-packagename. In this example I choose just the first package from the list. That way you can view details if you want to.


```python
first_packagename = cityclient.get_packages()[0]
cityclient.get_package_metadata(package_name=first_packagename)
```




    {'id': '1b400a05-7ca5-4dbb-bb3c-c05e97b745d0',
     'name': 'verzeichnungsdaten-sterbefälle-1876',
     'title': 'Verzeichnungsdaten Sterbefälle 1876',
     'author': 'Stadt Braunschweig',
     'author_email': 'stadtarchiv@braunschweig.de',
     'maintainer': 'Braunschweig',
     'maintainer_email': 'noreply@stadt-koeln.de',
     'license_title': 'http://creativecommons.org/licenses/by/4.0/',
     'license_id': 'cc-by/4.0',
     'notes': '<p>Der Datensatz enthält die Namen der im Jahr 1876 im Bereich des Standesamtes der Stadt Braunschweig verstorbenen Personen. Außerdem ist jeweils die Nummer des Eintrages in den Standesamtsregistern der Stadt Braunschweig genannt.</p>\n',
     'url': 'https://opendata.braunschweig.de/dataset/verzeichnungsdaten-sterbef%C3%A4lle-1876',
     'state': 'Active',
     'private': True,
     'revision_timestamp': '2023-02-22T16:03:37+01:00',
     'metadata_created': '2022-11-09 07:37:22',
     'metadata_modified': '2022-11-09 07:37:22',
     'creator_user_id': '69cb4099-b802-4f49-8d40-72a7d121497e',
     'type': 'Dataset',
     'resources': [{'id': '901db21d-f18f-45f5-89f3-932cee982de4',
       'revision_id': '',
       'url': 'https://opendata.braunschweig.de/sites/default/files/E_34_1876_Sterbe_Daten.csv',
       'description': '<p>Der Datensatz enthält die Namen der im Jahr 1876 im Bereich des Standesamtes der Stadt Braunschweig verstorbenen Personen. Außerdem ist jeweils die Nummer des Eintrages in den Standesamtsregistern der Stadt Braunschweig genannt.</p>\n',
       'format': 'csv',
       'state': 'Active',
       'revision_timestamp': '2022-11-30T09:40:17+01:00',
       'name': 'Verzeichnungsdaten Sterbefälle 1876 (csv)',
       'mimetype': 'text/csv',
       'size': '258.5 KB',
       'created': '2022-11-09T07:42:30+01:00',
       'resource_group_id': '7d648cd3-a1f2-4e00-99c1-9dcf9817fee2',
       'last_modified': 'Date changed  2022-11-30T09:40:17+01:00'},
      {'id': 'f335fd55-0183-4475-baf4-c6ff3c08531b',
       'revision_id': '',
       'url': 'https://opendata.braunschweig.de/sites/default/files/E_34_1876_Sterbe_Daten.zip',
       'description': '<p><span style="color: rgb(59, 59, 59); font-family: Ubuntu, &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 16px;">Der Datensatz enthält die Namen der im Jahr 1876 im Bereich des Standesamtes der Stadt Braunschweig verstorbenen Personen. Außerdem ist jeweils die Nummer des Eintrages in den Standesamtsregistern der Stadt Braunschweig genannt.</span></p>\n',
       'format': 'slk',
       'state': 'Active',
       'revision_timestamp': '2022-11-30T09:40:40+01:00',
       'name': 'Verzeichnungsdaten Sterbefälle 1876 (slk)',
       'mimetype': 'application/zip',
       'size': '34.26 KB',
       'created': '2022-11-30T09:39:49+01:00',
       'resource_group_id': '7d648cd3-a1f2-4e00-99c1-9dcf9817fee2',
       'last_modified': 'Date changed  2022-11-30T09:40:40+01:00'}],
     'tags': [{'id': '857d861d-078f-47b1-9ab2-e0b5b7492084',
       'vocabulary_id': '2',
       'name': 'Bevölkerung'}],
     'groups': [{'description': '',
       'id': '7d648cd3-a1f2-4e00-99c1-9dcf9817fee2',
       'image_display_url': 'https://opendata.braunschweig.de/sites/default/files/Logo%20Braunschweig.png',
       'title': 'Stadt Braunschweig',
       'name': 'group/stadt-braunschweig'}]}



But to get an total overview, its easier to fetch the packagenames and its according metadata within one api-call. Store the data into a pandas.DataFrame for easier dataprocessing and to get familiar with


```python
total = cityclient.get_total_packages_with_resources()

import pandas as pd
df = pd.DataFrame(total)
df["metadata_created"] = pd.to_datetime(df["metadata_created"])
df.columns
```




    Index(['id', 'name', 'title', 'author', 'author_email', 'maintainer',
           'maintainer_email', 'license_title', 'license_id', 'notes', 'url',
           'state', 'log_message', 'private', 'revision_timestamp',
           'metadata_created', 'metadata_modified', 'creator_user_id', 'type',
           'resources', 'tags', 'groups'],
          dtype='object')



First, I'm interested into the publisher-frequency of Braunschweig. I group the packages into quarter-intervals:


```python
monthly_grouped = df.groupby(pd.Grouper(key="metadata_created", freq="Q")).sum(numeric_only=True)
monthly_grouped.columns = ["packages"]
monthly_grouped = monthly_grouped.sort_values(by="metadata_created", ascending=True)
monthly_grouped.plot(kind="bar")
```




    <Axes: xlabel='metadata_created'>




    
![https://github.com/protogia/protogia.github.io/tree/master/content/blog/opendata-meta-information-overview_files/output_14_1.png](https://github.com/protogia/protogia.github.io/tree/master/content/blog/opendata-meta-information-overview_files/output_14_1.png)
    


As you see, it seems when Braunschweig started the project, they launched the most packages. Within 2023 they published up to 10 packages per quarter.

Now I want to get more information about tag-diversity and how many authors and maintainers are working for this project.


```python
df.author.unique()
```




    array(['Stadt Braunschweig', 'Stadt Braunsschweig',
           'Deutsche Zentrum für Luft- und Raumfahrt e. V. (DLR)'],
          dtype=object)




```python
df.maintainer.unique()
```




    array(['Braunschweig'], dtype=object)




```python
taglist = []
for entry in df.tags:
  for tag in entry:
    taglist.append(tag)

taglist = pd.DataFrame(taglist).drop(["id"], axis=1)
tag_grouped = taglist.groupby(by=["name"]).count()
tag_grouped.columns = ["count"]
tag_grouped = tag_grouped.sort_values(by=["count"], ascending=False)
tag_grouped.plot(kind="bar")
```




    <Axes: xlabel='name'>




    
![https://github.com/protogia/protogia.github.io/tree/master/content/blog/opendata-meta-information-overview_files/output_18_1.png](https://github.com/protogia/protogia.github.io/tree/master/content/blog/opendata-meta-information-overview_files/output_18_1.png)
    


As you can see there are only two official contributors publishing datasets to the opendata-plattform of Braunschweig (until Q3/2023).
The most packages are about traffic, geography, environment and health-data.

If you want to get deeper into the data just fetch the resources of your target-package and download process the resource-dataset.


```python

```
