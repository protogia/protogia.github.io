---
title: Opendata Overview
date: '2025-01-08T13:36:55.011988+00:00'
author: 'Giancarlo Rizzo'
draft: true
categories: []
color: '#ffcc66'
titleimage: 'content/blog/titleimages/CHANGEME.png'
---

<a href="https://colab.research.google.com/github/protogia/Braunschweig/blob/main/opendata-meta-information-overview.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# Opendata Meta Information Overview

## Prologue
This notebook is a trys to analyse the metadata informations of the provided [opendata sources](https://www.braunschweig.de/digitalisierung-online-services/open-data.php) from the city of Braunschweig. It uses an python-based govdata-client to extract some informations from the provided metdata.

## Setup

First we install the [govdata-client](https://pypi.org/project/govdata/) via pip and further dependencies we'll need to import in the next step.

*Furthermore we set some basic configuration for the diagram-layout which will be used later.*


```python
%%capture
!pip install govdata
!pip install pandas
```


```python
# SET DIAGRAM-LAYOUT FOR Jypter-Notebook

from IPython.core.display import display, HTML

# Set notebook width to 100%
display(HTML("<style>.container { width:100% !important; }</style>"))
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [16, 9]
plt.rcParams['figure.autolayout'] = True
```


<style>.container { width:100% !important; }</style>



```python
import govdata
import pandas as pd
```

Now we can import and initialize an **DKANPortalClient** for our city of interest. To test if the cityclient can establish a connection we can do a connectiontest:


```python
cityclient = DKANPortalClient(city="braunschweig", apiversion=3)
```


```python
cityclient.connectiontest()
```




    True



## Exposing the publisher-frequency

First we van list available packages for our choosen city. A package represents a topic like *infrastructure*, *traffic*, etc.


```python
cityclient.get_packages()
```




    ['verzeichnungsdaten-sterbefälle-1876',
     'passantenfrequenzen-innenstadt',
     'interessengebiete',
     'stadtkarte-1-5000',
     'stadtplan-1-20000',
     'stadtübersicht-1-40000',
     'radverkehrsnetz',
     'regionalkarte-1-100000',
     'stadtbezirke',
     'wahlbezirke',
     'statistische-bezirke',
     'höhenlinien',
     'rundgang-blik-kraheweg',
     'rundgang-blik-uhdeweg',
     'rundgang-blik-kleine-dörfer-weg',
     'rundgang-braunschweiger-ringgleis',
     'rundgang-natur-erleben-riddagshausen',
     'straßenverzeichnis',
     'demographie',
     'überschwemmungsgebiet-oker',
     'überschwemmungsgebiet-schunter',
     'überschwemmungsgebiet-wabe',
     'wasserschutzgebiet',
     'lärmkartierung-straße-nachtsüber-prognose-2025',
     'fahrstreifengenaue-straßenkarte-des-innenstadtrings',
     'fahrstreifengenaue-straßenkarte-vom-rebenring-zum-flughafen',
     'e-tretroller-geschäftsgebiet',
     'e-tretroller-parkverbotszonen',
     'verkehrsmengenkarte-öpnv-stand-2016',
     'verkehrsmengenkarte-kfz-stand-2016',
     'eigenwirtschaftliche-glasfaserausbaugebiete',
     'ifh-kundenbefragung-vitale-innenstädte-2022',
     'schülerinnenzahl-der-allgemein-bildenden-schulen-nach-schule-und-schuljahrgang',
     'schülerzahl-der-berufsbildenden-schulen-nach-schule-und-schuljahrgang',
     'abgängerinnen-von-allgemein-bildenden-schulen-nach-abschlussart-und-schulform',
     'flexibilisierung-des-einschulungsstichtages',
     'adressliste-der-schulen',
     'verwaltungsstruktur-der-stadt-braunschweig',
     'liste-der-oberbürgermeisterinnen-und-oberbürgermeister-der-stadt-braunschweig-seit-1848',
     'jugendzentren-kinder-und-teeny-klubs',
     'kindertagesstätten-adressen',
     'automatische-radverkehrszählung',
     'doppelhaushalt-stadt-braunschweig-20232024-investitionsprogramm',
     'doppelhaushalt-stadt-braunschweig-20232024-produktübersicht',
     'doppelhaushalt-stadt-braunschweig-20232024-teilhaushalte',
     'jahresbericht-2020-feuerwehr-braunschweig',
     'openbikesensor-braunschweig',
     'wetterstation-grundschule-rautheim',
     'wetterstation-grundschule-rheinring',
     'wetterstation-grundschule-veltenhof',
     'wetterstation-gymnasium-hoffmann-von-fallersleben',
     'wetterstation-gymnasium-kleine-burg',
     'wetterstation-igs-franzsches-feld',
     'wetterstation-igs-heidberg',
     'wetterstation-niebelungen-realschule',
     'wetterstation-realschule-maschstraße',
     'wetterstation-wilhelm-gymnasium',
     'pegelstand-oker',
     'pegelstand-schunter',
     'pegelstand-wabe',
     'luftqualität-hans-sommer-straße',
     'luftqualität-rudolfplatz',
     'opengeodatani',
     'entwurf-des-doppelhaushalts-der-stadt-braunschweig-20252026-teilhaushalte',
     'entwurf-des-doppelhaushalts-der-stadt-braunschweig-20252026-produktübersicht',
     'entwurf-des-doppelhaushalts-der-stadt-braunschweig-20252026-investitionsprogramm',
     'dlr-urban-traffic-datensatz-dlr-ut',
     'naturschutz-schutzgebiete-und-naturdenkmäler',
     'lärmkartierung-2022']



To get an total overview we'll fetch the packagenames and the relating metadata using the following api-function. We'll store the data into a `pandas.DataFrame` for easier data processing.


```python
total = cityclient.get_total_packages_with_resources()

df = pd.DataFrame(total)
df["metadata_created"] = pd.to_datetime(df["metadata_created"])
df['metadata_created'] = df['metadata_created'].apply(lambda x: x.replace(tzinfo=None) if x.tzinfo else x) # add tz-info if not available
df.columns.to_list()
```




    ['id',
     'name',
     'title',
     'author',
     'author_email',
     'maintainer',
     'maintainer_email',
     'license_title',
     'license_id',
     'notes',
     'url',
     'state',
     'private',
     'revision_timestamp',
     'metadata_created',
     'metadata_modified',
     'creator_user_id',
     'type',
     'resources',
     'tags',
     'log_message',
     'groups']



We got informations about authors, maintainers, resvision-dates, dataset-types and further. Now, we'll check the publisher-frequency of the opendata-providers in Braunschweig.

To do so, we group the packages into monthly-intervals:


```python
df.head(n=3)

monthly_grouped = df.groupby(pd.Grouper(key="metadata_created", freq="M")).sum(numeric_only=True)
monthly_grouped.columns = ["packages"]
monthly_grouped = monthly_grouped.sort_values(by="metadata_created", ascending=True)
monthly_grouped.plot(kind="bar")
```




    <Axes: xlabel='metadata_created'>




    
![alt-text](/img/Opendata-Overview/output_17_1.png)
    


As we see, it seems when Braunschweig started the project, they launched the most packages. Within 2023 they published the most packages per month.

Now I want to get more information about tag-diversity. We can use the information about tag-diversity to expose informations about periodical consitency of the publishing-frequency per `tag`.  

A `tag` represents the dataset-category. We'll plot the dataset-count per `tag` (category), whereas the category-names are listed on the x-axis.


```python
# create list of tags for x-axis of barplot
taglist = []
for entry in df.tags:
  for tag in entry:
    taglist.append(tag)

# group datasets by tag and count them
taglist = pd.DataFrame(taglist).drop(["id"], axis=1)
tag_grouped = taglist.groupby(by=["name"]).count()
tag_grouped.columns = ["count"]
tag_grouped = tag_grouped.sort_values(by=["count"], ascending=False)

# plot
tag_grouped.plot(kind="bar")
```




    <Axes: xlabel='name'>




    
![alt-text](/img/Opendata-Overview/output_19_1.png)
    


Without evaluating the quality of the single datasets we see that there is a quantitative focus on geospatial-, traffic- and population-datasets, whereas datasets about health, politics and economics are less published.

Now we should check how the publisher-frequency per tag changed over time.


```python
# Exploding the 'tags' list into separate rows
df_exploded = df.explode('tags')
df_exploded['tags'] = df_exploded['tags'].apply(lambda x: x['name'])

# group monthly
df_exploded['month_year'] = df_exploded['metadata_created'].dt.to_period('M')
result = df_exploded.groupby(['tags', 'month_year']).size().reset_index(name='count')
result.sort_values(by=['month_year'], ascending=True, inplace=True)
result.head(n=5)
```





  <div id="df-69e29718-b63d-4d84-8b87-d7227713d300" class="colab-df-container">
    <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>tags</th>
      <th>month_year</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bevölkerung</td>
      <td>2022-11</td>
      <td>3</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Infrastruktur, Bauen und Wohnen</td>
      <td>2022-11</td>
      <td>3</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Politik und Wahlen</td>
      <td>2022-11</td>
      <td>1</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Gesundheit</td>
      <td>2022-11</td>
      <td>1</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Soziales</td>
      <td>2022-11</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>
    <div class="colab-df-buttons">

  <div class="colab-df-container">
    <button class="colab-df-convert" onclick="convertToInteractive('df-69e29718-b63d-4d84-8b87-d7227713d300')"
            title="Convert this dataframe to an interactive table."
            style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960">
    <path d="M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z"/>
  </svg>
    </button>

  <style>
    .colab-df-container {
      display:flex;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    .colab-df-buttons div {
      margin-bottom: 4px;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

    <script>
      const buttonEl =
        document.querySelector('#df-69e29718-b63d-4d84-8b87-d7227713d300 button.colab-df-convert');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      async function convertToInteractive(key) {
        const element = document.querySelector('#df-69e29718-b63d-4d84-8b87-d7227713d300');
        const dataTable =
          await google.colab.kernel.invokeFunction('convertToInteractive',
                                                    [key], {});
        if (!dataTable) return;

        const docLinkHtml = 'Like what you see? Visit the ' +
          '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
          + ' to learn more about interactive tables.';
        element.innerHTML = '';
        dataTable['output_type'] = 'display_data';
        await google.colab.output.renderOutput(dataTable, element);
        const docLink = document.createElement('div');
        docLink.innerHTML = docLinkHtml;
        element.appendChild(docLink);
      }
    </script>
  </div>


<div id="df-1714a20c-adeb-4939-a682-6b0581701984">
  <button class="colab-df-quickchart" onclick="quickchart('df-1714a20c-adeb-4939-a682-6b0581701984')"
            title="Suggest charts"
            style="display:none;">

<svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
     width="24px">
    <g>
        <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
    </g>
</svg>
  </button>

<style>
  .colab-df-quickchart {
      --bg-color: #E8F0FE;
      --fill-color: #1967D2;
      --hover-bg-color: #E2EBFA;
      --hover-fill-color: #174EA6;
      --disabled-fill-color: #AAA;
      --disabled-bg-color: #DDD;
  }

  [theme=dark] .colab-df-quickchart {
      --bg-color: #3B4455;
      --fill-color: #D2E3FC;
      --hover-bg-color: #434B5C;
      --hover-fill-color: #FFFFFF;
      --disabled-bg-color: #3B4455;
      --disabled-fill-color: #666;
  }

  .colab-df-quickchart {
    background-color: var(--bg-color);
    border: none;
    border-radius: 50%;
    cursor: pointer;
    display: none;
    fill: var(--fill-color);
    height: 32px;
    padding: 0;
    width: 32px;
  }

  .colab-df-quickchart:hover {
    background-color: var(--hover-bg-color);
    box-shadow: 0 1px 2px rgba(60, 64, 67, 0.3), 0 1px 3px 1px rgba(60, 64, 67, 0.15);
    fill: var(--button-hover-fill-color);
  }

  .colab-df-quickchart-complete:disabled,
  .colab-df-quickchart-complete:disabled:hover {
    background-color: var(--disabled-bg-color);
    fill: var(--disabled-fill-color);
    box-shadow: none;
  }

  .colab-df-spinner {
    border: 2px solid var(--fill-color);
    border-color: transparent;
    border-bottom-color: var(--fill-color);
    animation:
      spin 1s steps(1) infinite;
  }

  @keyframes spin {
    0% {
      border-color: transparent;
      border-bottom-color: var(--fill-color);
      border-left-color: var(--fill-color);
    }
    20% {
      border-color: transparent;
      border-left-color: var(--fill-color);
      border-top-color: var(--fill-color);
    }
    30% {
      border-color: transparent;
      border-left-color: var(--fill-color);
      border-top-color: var(--fill-color);
      border-right-color: var(--fill-color);
    }
    40% {
      border-color: transparent;
      border-right-color: var(--fill-color);
      border-top-color: var(--fill-color);
    }
    60% {
      border-color: transparent;
      border-right-color: var(--fill-color);
    }
    80% {
      border-color: transparent;
      border-right-color: var(--fill-color);
      border-bottom-color: var(--fill-color);
    }
    90% {
      border-color: transparent;
      border-bottom-color: var(--fill-color);
    }
  }
</style>

  <script>
    async function quickchart(key) {
      const quickchartButtonEl =
        document.querySelector('#' + key + ' button');
      quickchartButtonEl.disabled = true;  // To prevent multiple clicks.
      quickchartButtonEl.classList.add('colab-df-spinner');
      try {
        const charts = await google.colab.kernel.invokeFunction(
            'suggestCharts', [key], {});
      } catch (error) {
        console.error('Error during call to suggestCharts:', error);
      }
      quickchartButtonEl.classList.remove('colab-df-spinner');
      quickchartButtonEl.classList.add('colab-df-quickchart-complete');
    }
    (() => {
      let quickchartButtonEl =
        document.querySelector('#df-1714a20c-adeb-4939-a682-6b0581701984 button');
      quickchartButtonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';
    })();
  </script>
</div>

    </div>
  </div>





```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set the plot size and style
plt.figure(figsize=(12, 6))
sns.set(style="whitegrid")

# Create the bar plot
sns.barplot(x='month_year', y='count', hue='tags', data=result, palette='tab10')

# Set labels and title
plt.title('Count per Tag over Time')
plt.xlabel('Publishing date')
plt.ylabel('Count')
plt.legend(title='Tags', loc='upper right')

# Display the plot
plt.tight_layout()
plt.show()

```


    
![alt-text](/img/Opendata-Overview/output_22_0.png)
    


As we can see the most periodical publishing is done in the category **Traffic, Government and Taxes, and Geographical Datasets**.

It seems like they have a periodic publishing rate of 2 quaters, whereas datasets in the category of **social** are published yearly.

## Conclusion

This evaluation was just a basic overview of a datasource to get familiar with the opendata-structure.

I plan to checkout certain datasets in detail and also compare the publishing rate Braunschweig with other cities.
