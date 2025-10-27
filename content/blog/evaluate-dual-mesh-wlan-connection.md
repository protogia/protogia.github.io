---
title: Bandwidth and Latency Evaluation for a Two-Node Wi-Fi Mesh Network
date: '2025-10-17T21:48:43.708182+00:00'
author: 'Giancarlo Rizzo'
draft: true
plotly: true
categories: []
color: '#a09f93'
---

## Bandwith-Evaluation (MESH)

### 1. Install dependencies


```python
%%capture
!pip install ipykernel;
!pip install matplotlib;
!pip install seaborn;
!pip install folium;
!pip install plotly;
!pip install nbformat;
```


```python
import sys
import nbformat

print("Python Executable Path:", sys.executable)
print("nbformat version:", nbformat.__version__)
```

    Python Executable Path: /home/working/.cache/pypoetry/virtualenvs/wifi-mesh-bandwith-evaluation-ZZPij1Nn-py3.12/bin/python
    nbformat version: 5.10.4



```python
import pandas as pd;
import geopandas as gpd;
import folium;
import os;
import seaborn as sns;
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
```

### 2. Load testtraces


```python
folder = 'results'

testtraces = {}
for dir in os.listdir(folder):
      testtraces[dir] = []
      try:
          for file in os.listdir(os.path.join(folder, dir)):
              if "pcap" not in file:
                  file_path = os.path.join(folder, dir, file)
                  df = pd.read_csv(file_path)
                  testtraces[dir].append(df)
      except Exception as e:
          print(f"Failed to read {file_path}: {e}")

```


```python
testtraces['bandwithtest_09072924_mesh_wlan-b'][0].head()
```




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
      <th>Unnamed: 0</th>
      <th>Time</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Bitrate</th>
      <th>Latency</th>
      <th>DISTANCE_CENTER</th>
      <th>DISTANCE_AP_RUESTHALLE</th>
      <th>DISTANCE_AP_GARAGE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>11:41:55.248000</td>
      <td>52.315723</td>
      <td>10.564559</td>
      <td>1.31</td>
      <td>3.74</td>
      <td>189.419552</td>
      <td>228.346361</td>
      <td>146.736744</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>11:41:56.248000</td>
      <td>52.315727</td>
      <td>10.564529</td>
      <td>0.00</td>
      <td>154.00</td>
      <td>187.333062</td>
      <td>226.257243</td>
      <td>144.663165</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>11:41:57.248000</td>
      <td>52.315732</td>
      <td>10.564495</td>
      <td>1.57</td>
      <td>383.00</td>
      <td>184.941540</td>
      <td>223.862744</td>
      <td>142.286387</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>11:41:58.248000</td>
      <td>52.315735</td>
      <td>10.564457</td>
      <td>0.00</td>
      <td>300.00</td>
      <td>182.369709</td>
      <td>221.288577</td>
      <td>139.727164</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>11:42:00.248000</td>
      <td>52.315744</td>
      <td>10.564365</td>
      <td>1.56</td>
      <td>13.60</td>
      <td>176.021568</td>
      <td>214.936401</td>
      <td>133.404155</td>
    </tr>
  </tbody>
</table>
</div>



### 3.1. Bandwit results: Distance to center


```python
# Concatenate all dataframes to plot on a single figure
all_dfs = []
for testname, list_of_dfs in testtraces.items():
    all_dfs.extend(list_of_dfs)

combined_df = pd.concat(all_dfs, ignore_index=True)

# Outlier removal
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

combined_df_filtered = combined_df.copy()
combined_df_filtered = remove_outliers_iqr(combined_df_filtered, 'Bitrate')
combined_df_filtered = remove_outliers_iqr(combined_df_filtered, 'DISTANCE_CENTER')
```


```python
# plottling
scatter_fig = px.scatter(
    combined_df_filtered,
    x='DISTANCE_CENTER',
    y='Bitrate',
    title='Bitrate vs. Distance to Center with Trendline (Outliers Removed)',
    labels={'DISTANCE_CENTER': 'Distance to Center [m]', 'Bitrate': 'Bitrate [MBit/s]'},
    trendline='lowess',
)

histogram_fig = go.Figure(go.Histogram2dContour(
    x=combined_df_filtered['DISTANCE_CENTER'],
    y=combined_df_filtered['Bitrate'],
    colorscale='Viridis',
    colorbar=dict(title='Density'),
    contours=dict(coloring='heatmap'),
))

# Create subplots
fig = make_subplots(rows=1, cols=2, subplot_titles=('Bitrate vs. Distance to Center with Trendline', 'Spread of Bitrate vs. Distance to Center (Heatmap)'))

for trace in scatter_fig['data']:
    fig.add_trace(trace, row=1, col=1)

for trace in histogram_fig['data']:
     fig.add_trace(trace, row=1, col=2)


fig.update_layout(
    title_text='Bitrate Visualizations',
    template='none'
)

fig.update_xaxes(title_text='Distance to Center [m]', row=1, col=1)
fig.update_yaxes(title_text='Bitrate [MBit/s]', row=1, col=1)
fig.update_xaxes(title_text='Distance to Center [m]', row=1, col=2)
fig.update_yaxes(title_text='Bitrate [MBit/s]', row=1, col=2)

fig.show()
```


{{< plotly json="/plotly/plotly_chart_1.json" >}}


### 3.2. Latency results: Distance to center


```python
# Concatenate dataframes with 'Latency' column
all_dfs_latency = []
for testname, list_of_dfs in testtraces.items():
    for df in list_of_dfs:
        if 'Latency' in df.columns:
            all_dfs_latency.append(df)

combined_df_latency = pd.concat(all_dfs_latency, ignore_index=True)

# Outlier removal using IQR for Latency and DISTANCE_CENTER
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

combined_df_latency_filtered = combined_df_latency.copy()
combined_df_latency_filtered = remove_outliers_iqr(combined_df_latency_filtered, 'Latency')
combined_df_latency_filtered = remove_outliers_iqr(combined_df_latency_filtered, 'DISTANCE_CENTER')
```


```python
# plotting
scatter_fig_latency = px.scatter(
    combined_df_latency_filtered,
    x='DISTANCE_CENTER',
    y='Latency',
    title='Latency vs. Distance to Center with Trendline (Outliers Removed)',
    labels={'DISTANCE_CENTER': 'Distance to Center [m]', 'Latency': 'Latency [ms]'},
    trendline='lowess'
)

histogram_fig_latency = go.Figure(go.Histogram2dContour(
    x=combined_df_latency_filtered['DISTANCE_CENTER'],
    y=combined_df_latency_filtered['Latency'],
    colorscale='Viridis',
    colorbar=dict(title='Density'),
    contours=dict(coloring='heatmap'),
))

# Create subplots
fig_latency = make_subplots(rows=1, cols=2, subplot_titles=('Latency vs. Distance to Center with Trendline (Outliers Removed)', 'Spread of Latency vs. Distance to Center (2D Histogram, Outliers Removed)'))

for trace in scatter_fig_latency['data']:
    fig_latency.add_trace(trace, row=1, col=1)

for trace in histogram_fig_latency['data']:
     fig_latency.add_trace(trace, row=1, col=2)


fig_latency.update_layout(
    title_text='Latency Visualizations (Outliers Removed)',
    showlegend=False,
    template='none'
)

fig_latency.update_xaxes(title_text='Distance to Center [m]', row=1, col=1)
fig_latency.update_yaxes(title_text='Latency [ms]', row=1, col=1)
fig_latency.update_xaxes(title_text='Distance to Center [m]', row=1, col=2)
fig_latency.update_yaxes(title_text='Latency [ms]', row=1, col=2)

fig_latency.show()
```


{{< plotly json="/plotly/plotly_chart_2.json" >}}


### 4. Bandwith and Latency on geomap


```python
# Concatenate all dataframes for plotting
all_dfs_map = []
for testname, list_of_dfs in testtraces.items():
    for df in list_of_dfs:
        all_dfs_map.append(df)

combined_df_map = pd.concat(all_dfs_map, ignore_index=True)

# Outlier removal using IQR
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

combined_df_map_filtered = combined_df_map.copy()
combined_df_map_filtered = remove_outliers_iqr(combined_df_map_filtered, 'Bitrate')
combined_df_map_filtered = remove_outliers_iqr(combined_df_map_filtered, 'DISTANCE_CENTER')

# Drop rows with NaN in Latency column for plotting size and color on the Latency map
if 'Latency' in combined_df_map_filtered.columns and not combined_df_map_filtered['Latency'].isnull().all():
    combined_df_map_filtered = remove_outliers_iqr(combined_df_map_filtered, 'Latency')

combined_df_map_latency_filtered = combined_df_map_filtered.dropna(subset=['Latency']).copy()
```


```python
# plotting
fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'mapbox'}, {'type': 'mapbox'}]],
                    subplot_titles=('Bitrate Map (Outliers Removed)', 'Latency Map (Outliers Removed)'))

fig.add_trace(go.Scattermapbox(
    lat=combined_df_map_filtered["Latitude"],
    lon=combined_df_map_filtered["Longitude"],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=16, # Increased marker size
        color=combined_df_map_filtered["Bitrate"],
        colorscale='viridis',
        colorbar=dict(title='Bitrate [MBit/s]', x=0.45) # Adjust x position
    ),
    text=combined_df_map_filtered["Bitrate"].apply(lambda x: f'Bitrate: {x:.2f}'),
    name='Bitrate'
), row=1, col=1)

green_to_red = [(0, 'green'), (0.5, 'grey'), (1, 'red')]
if not combined_df_map_latency_filtered.empty: # Check if there's data after dropping NaNs
    fig.add_trace(go.Scattermapbox(
        lat=combined_df_map_latency_filtered["Latitude"],
        lon=combined_df_map_latency_filtered["Longitude"],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=16, # Increased marker size
            color=combined_df_map_latency_filtered["Latency"],
            colorscale=green_to_red,
            colorbar=dict(title='Latency [ms]', x=1.0) # Adjust x position
        ),
        text=combined_df_map_latency_filtered["Latency"].apply(lambda x: f'Latency: {x:.2f}'),
        name='Latency'
    ), row=1, col=2)
else:
     print("No Latency data available after outlier removal for mapping.")


# mapbox subplots
fig.update_layout(
    mapbox1=dict(
        style="carto-positron",
        center=dict(lat=combined_df_map_filtered["Latitude"].mean(), lon=combined_df_map_filtered["Longitude"].mean()),
        zoom=16
    ),
    mapbox2=dict(
        style="carto-positron",
        center=dict(lat=combined_df_map_latency_filtered["Latitude"].mean(), lon=combined_df_map_latency_filtered["Longitude"].mean()),
        zoom=16
    ),
    showlegend=False,
)

fig.show()
```

    /tmp/ipykernel_653059/3453872979.py:5: DeprecationWarning:
    
    *scattermapbox* is deprecated! Use *scattermap* instead. Learn more at: https://plotly.com/python/mapbox-to-maplibre/
    
    /tmp/ipykernel_653059/3453872979.py:21: DeprecationWarning:
    
    *scattermapbox* is deprecated! Use *scattermap* instead. Learn more at: https://plotly.com/python/mapbox-to-maplibre/
    



{{< plotly json="/plotly/plotly_chart_3.json" >}}

