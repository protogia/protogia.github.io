---
title: 'Wifi-Mesh-Evlauation: Analysing Bandwith and Latency Measurements for a two-node WiFi-Mesh'
date: '2025-02-03T18:12:41.013471+00:00'
author: 'Giancarlo Rizzo'
draft: false
plotly: true
categories: []
color: '#a09f93'
---

## Prologue
This evaluation contains the result from my WiFi- Mehs Test Setup. The goal was to find out if a WiFi Mesh cosisting of two accesspoints with a total distance of 100 meters  in between would allow a prototype autonomous vehicle to stream its video data via wifi to a host (See my [previous post](https://protogia.github.io/blog/wifi-bandwith-to-distance-relation/) about the test setup). 

After recoding multiple test traces and syncing the logging-outputs of iperf3 and gpspipe we'll visualise in this article the limitations of the setup.
To make sure that the setup will suit to the requirements, we have to evaluate the relation between bandwith and distance and as well as between latency and distance. To discover wifi blindspots in the test area we will also plot the results on a map.

## Install dependencies

{{<details title="Show code">}}

```python
%%capture
!pip install ipykernel;
!pip install matplotlib;
!pip install seaborn;
!pip install folium;
!pip install plotly;
```

```python
import pandas as pd;
import numpy as np;
import geopandas as gpd;
import folium;
import os;
import seaborn as sns;
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
```

{{</details>}}

## Load testtraces

We recorded multiple traces in two different setups. The synced testtraces within _results/bandwithtest_09072024_mesh_wlan-b_ contain additional informations about the latency. For the bandwith evaluation we will use all of them.

{{<details title="show code">}}

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

| Unnamed: 0 | Time | Latitude | Longitude | Bitrate | Latency | DISTANCE_CENTER | DISTANCE_AP_RUESTHALLE | DISTANCE_AP_GARAGE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 11:41:55.248000 | 52.315723 | 10.564559 | 1.31 | 3.74 | 189.419552 | 228.346361 | 146.736744 |
| 1 | 1 | 11:41:56.248000 | 52.315727 | 10.564529 | 0.00 | 154.00 | 187.333062 | 226.257243 | 144.663165 |
| 2 | 2 | 11:41:57.248000 | 52.315732 | 10.564495 | 1.57 | 383.00 | 184.941540 | 223.862744 | 142.286387 |
| 3 | 3 | 11:41:58.248000 | 52.315735 | 10.564457 | 0.00 | 300.00 | 182.369709 | 221.288577 | 139.727164 |
| 4 | 4 | 11:42:00.248000 | 52.315744 | 10.564365 | 1.56 | 13.60 | 176.021568 | 214.936401 | 133.404155 |

{{</details>}}

The data consists of the following informations:

| Entity                 | Unit        |
|------------------------|-------------|
| Time                   | [localtime] |
| Latitude               | [wgs84]     |
| Longitude              | [wgs84]     |
| Bitrate                | [MB/s]      |
| Latency                | [ms]        |
| DISTANCE_CENTER        | [m]         |
| DISTANCE_AP_RUESTHALLE | [m]         |
| DISTANCE_AP_GARAGE     | [m]         |

The values for _DISTANCE_CENTER_, _DISTANCE_AP_RUESTHALLE_ and _DISTANCE_AP_GARAGE_ are calculated. _DISTANCE_CENTER_ describes the distance between the vehicle position and the middle point between both accesspoints. _DISTANCE_AP_RUESTHALLE_ and _DISTANCE_AP_GARAGE_ are describing the distance between accesspoint-1/accesspoint-2.The last two distances are calculated for proofing reasons.

## Outlier Removal

For the evaluation we'll concatenate the single recordings to one dataframe. In the next step we'll remove the outliers for this we need to visualise the distribution and check for the most suitable methods. 

### IQR

IQR removes outliers by calculating thresholds of normal distributions. Each value that exceeds this threshold is signed as outlier. As you can see in the next plots the distribution of values for _Bitrate_ and _Latency_ is not a normal distribution. The Shapiro-Wilk-Test confirms this by calculating values for p that do not fulfill _p>0.05_. So IQR is not a suitable method for this dataset.

{{<details title="show code">}}

```python
# Concatenate all dataframes to plot on a single figure
all_dfs = []
for testname, list_of_dfs in testtraces.items():
    all_dfs.extend(list_of_dfs)

combined_df = pd.concat(all_dfs, ignore_index=True)
```

```python
from scipy import stats

# plot distributions
fig = make_subplots(rows=1, cols=2,
                    subplot_titles=('Distribution of Bitrate-data', 'Distribution of Latency-data'))

# bitrate
fig.add_trace(
    go.Histogram(
        x=combined_df['Bitrate'],
        nbinsx=100,
        name='Bitrate',
    ),
    row=1, col=1
)

# latency
fig.add_trace(
    go.Histogram(
        x=combined_df['Latency'],
        nbinsx=100,  
        name='Latency',
    ),
    row=1, col=2
)

fig.update_layout(
    title_text="Distribution of Bitrate and Latency Data",
    showlegend=False
)

fig.update_xaxes(title_text="Bitrate", row=1, col=1)
fig.update_xaxes(title_text="Latency", row=1, col=2)

fig.update_yaxes(title_text="Count", row=1, col=1)
fig.update_yaxes(title_text="Count", row=1, col=2)

fig.show()

# calculate IQR
Q1 = combined_df['Bitrate'].quantile(0.25)
Q3 = combined_df['Bitrate'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Shapiro-Wilk-Test
stat, p_value = stats.shapiro(combined_df['Bitrate'].dropna())
print(f'Shapiro-Wilk: statistical value = {stat:.4f}, p-value = {p_value:.4f} for Bitrate')

stat, p_value = stats.shapiro(combined_df['Latency'].dropna())
print(f'Shapiro-Wilk: statistical value = {stat:.4f}, p-value = {p_value:.4f} for Latency')
```

    Shapiro-Wilk: statistical value = 0.7010, p-value = 0.0000 for Bitrate
    Shapiro-Wilk: statistical value = 0.5886, p-value = 0.0000 for Latency

{{</details>}}

{{< plotly json="/plotly/evaluate-dual-mesh-wifi-connection/plotly_chart_7.json" >}}

Outlier Removal through z-score-method

The z-score measures how many standard deviations a value differs from the mean of a dataset. A common rule for outlier detection is a threshold of _z-score>3_. We'll calculate this for bitrate and latency and as you can see in the next plot all values on the right side of the threshold are identified as outliers.

{{<details title="show code">}}

```python
combined_df['z_score_bitrate'] = (combined_df['Bitrate'] - combined_df['Bitrate'].mean()) / combined_df['Bitrate'].std()
combined_df['z_score_latency'] = (combined_df['Latency'] - combined_df['Latency'].mean()) / combined_df['Latency'].std()

outliers_z_b = combined_df[np.abs(combined_df['z_score_bitrate']) > 3]
outliers_z_l = combined_df[np.abs(combined_df['z_score_latency']) > 3]
```

```python
outliers_z_b
```

| Unnamed: 0 | Time | Latitude | Longitude | Bitrate | Latency | DISTANCE_CENTER | DISTANCE_AP_RUESTHALLE | DISTANCE_AP_GARAGE | z_score_bitrate | z_score_latency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 60 | 2 | 11:35:55 | 52.316230 | 10.560745 | 510.0 | 182.0 | 81.589517 | 46.878905 | 123.901565 | 9.883251 | 0.54971 |
| 62 | 4 | 11:35:57 | 52.316238 | 10.560775 | 521.0 | 253.0 | 80.285808 | 46.167503 | 122.430535 | 10.118899 | 1.05948 |

```python
outliers_z_l
```

| Unnamed: 0 | Time | Latitude | Longitude | Bitrate | Latency | DISTANCE_CENTER | DISTANCE_AP_RUESTHALLE | DISTANCE_AP_GARAGE | z_score_bitrate | z_score_latency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 59 | 1 | 11:35:54 | 52.316229 | 10.560738 | 0.0 | 754.0 | 81.947953 | 47.140851 | 124.284874 | -1.042272 | 4.656589 |
| 164 | 28 | 11:40:33.500000 | 52.315911 | 10.560682 | 0.0 | 833.0 | 75.890957 | 37.326354 | 118.707602 | -1.042272 | 5.223798 |
| 245 | 50 | 11:35:30 | 52.316008 | 10.560837 | 0.0 | 1570.0 | 66.827893 | 28.036789 | 110.126673 | -1.042272 | 10.515353 |
| 246 | 51 | 11:35:31 | 52.316017 | 10.560805 | 10.5 | 547.0 | 69.193007 | 30.439653 | 112.494562 | -0.817335 | 3.170358 |
| 343 | 37 | 11:37:54.248000 | 52.315712 | 10.561602 | 0.0 | 544.0 | 22.399245 | 35.217764 | 55.648914 | -1.042272 | 3.148819 |

```python
# outlier flags
Z = 3
combined_df['Outlier_Bitrate'] = np.where(np.abs(combined_df['z_score_bitrate']) > Z, 'Outlier (> 3σ)', 'Normal')
combined_df['Outlier_Latency'] = np.where(np.abs(combined_df['z_score_latency']) > Z, 'Outlier (> 3σ)', 'Normal')


# plotting
def plot_distribution_with_outliers(df, data_col, z_col, title):
    mean_val = df[data_col].mean()
    std_val = df[data_col].std()
    
    outlier_flag_col = f'Outlier_{data_col}' 

    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        row_heights=[0.6, 0.4]
    )

    hist_fig = px.histogram(
        df, 
        x=data_col, 
        color=outlier_flag_col,
        color_discrete_map={
            'Normal': '#4C72B0',
            'Outlier (>|3σ|)': '#DC3912'
        },
        marginal="box", # Adds a box plot on top
        nbins=100
    )

    # Add histogram traces to the main figure
    for trace in hist_fig.data:
        if trace.type == 'histogram':
            fig.add_trace(trace, row=1, col=1)

    # Add vertical lines for the Z-score thresholds (Mean ± 3*StdDev)
    z_thresholds = [
        {'x': mean_val - 3 * std_val, 'text': 'Z=-3σ', 'pos': 'top left'},
        {'x': mean_val + 3 * std_val, 'text': 'Z=+3σ', 'pos': 'top right'}
    ]
    
    for threshold in z_thresholds:
        fig.add_vline(
            x=threshold['x'], 
            line_width=2, 
            line_dash="dash", 
            line_color="gray",
            annotation_text=threshold['text'],
            annotation_position=threshold['pos'],
            row=1, col=1
        )
        
    temp_y_col = 'dummy_y_axis_for_strip_plot'
    df[temp_y_col] = 0 # Create the temporary column
    
    scatter_fig = px.scatter(
        df, 
        x=data_col, 
        y=temp_y_col, # Use the unique column name
        color=outlier_flag_col,
        color_discrete_map={
            'Normal': '#4C72B0',
            'Outlier (>|3σ|)': '#DC3912'
        },
        # Update hover_data to use the new temp_y_col key
        hover_data={data_col: ':.4f', z_col: ':.4f', temp_y_col: False}
    )
    # Clean up the temporary column after plotting
    del df[temp_y_col] 
    
    for trace in scatter_fig.data:
        if trace.type == 'scatter':
            fig.add_trace(trace, row=2, col=1)


    fig.update_layout(
        height=700, 
        title_text=f'{title} Distribution with Z-Score Outliers',
        showlegend=True
    )
    
    # Update axes titles and properties
    fig.update_xaxes(title_text=data_col, row=2, col=1)
    fig.update_yaxes(title_text='Count', row=1, col=1)
    fig.update_yaxes(showticklabels=False, row=2, col=1, title_text='Data Points')
    fig.show()


plot_distribution_with_outliers(
    combined_df, 
    data_col='Bitrate', 
    z_col='z_score_bitrate', 
    title='Bitrate'
)

plot_distribution_with_outliers(
    combined_df, 
    data_col='Latency', 
    z_col='z_score_latency', 
    title='Latency'
)
```

{{</details>}}

{{< plotly json="/plotly/evaluate-dual-mesh-wifi-connection/plotly_chart_6.json" >}}

## Bandwith to Distance relation

After we removed the outliers we can start with the evaluation. For this we'll plot the Bitrate over the Distance values in a scatterplot and a heatmap.

{{<details title="show code">}}

```python
# Create a mask where both columns are marked 'Normal'
mask_normal = (combined_df['Outlier_Bitrate'] == 'Normal') & (combined_df['Outlier_Latency'] == 'Normal')

# Overwrite the DataFrame, keeping only the rows that match the mask
combined_df = combined_df[mask_normal]
```

```python
# plottling

ROLLAVG_WINDOW_SIZE = int(len(combined_df)*0.05)

scatter_fig = px.scatter(
    combined_df,
    x='DISTANCE_CENTER',
    y='Bitrate',
    title='Bitrate vs. Distance to Center with Trendline',
    labels={'DISTANCE_CENTER': 'Distance to Center [m]', 'Bitrate': 'Bitrate [MBit/s]'},
    trendline='rolling',
    trendline_options=dict(window=ROLLAVG_WINDOW_SIZE)
)

histogram_fig = go.Figure(go.Histogram2dContour(
    x=combined_df['DISTANCE_CENTER'],
    y=combined_df['Bitrate'],
    colorscale='Viridis',
    colorbar=dict(title='Density'),
    contours=dict(coloring='heatmap'),
))

# Create subplots
fig = make_subplots(rows=1, cols=2, subplot_titles=('Bitrate vs. Distance to Center with Trendline', 'Spread of Bitrate vs. Distance to Center'))

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

{{</details>}}

{{< plotly json="/plotly/evaluate-dual-mesh-wifi-connection/plotly_chart_4.json" >}}

On the left side the scatterplot shows the datapoints in detail. To visualise the relation better, we plotted the rolling average within a windowsize of 5% of the total count of datapoints. We also plotted a threshold of 30Mbit/sec to discover at which distance from the center the car could stream its data to the infrastructure.

According to the rolling Average the WiFi-connection fulfills the requirements up to 120 meters. But unfortunatly there is also a bandwith-drop between 75 meters and 80 meters of distance. This could be caused by reflections and shielding by buildigs in the testing area as the test setup wasn't ideally placed and I had to drive near to some halls and offices.

On the right side the heatmap shows the density of the datapoints. The highest density is around 50 meters for values of 100 MBit/s which seems logic as each accesspoints was placed 50 meters from the center and the test-vehicle was driving from outside of the test area first into the environment of accesspoint-1, passing the center and then entered the environment of accesspoint-2. Datapoints between 0 meters and 20 meters distance show density hotspots at 20Mbit/s as well as at 80Mbit/s. This could be caused by the handshake-phase when the vehicle changes the communication from one accesspoint to another. Another reason could also be the shielding by near buildings.

## Bandwith to Position Relation

To discover certain blindspots or shielding issues by near buildings we'll plot the data on a map.

{{<details title="show code">}}

```python
center_lat = combined_df["Latitude"].mean()
center_lon = combined_df["Longitude"].mean()

fig = go.Figure()

fig.add_trace(go.Scattermap(
    lat=combined_df["Latitude"], 
    lon=combined_df["Longitude"],
    mode='markers',
    marker=go.scattermap.Marker(
        size=15,
        color=combined_df["Bitrate"],
        colorscale='viridis',
        colorbar=dict(title='Bitrate [MBit/s]', x=1.0)
    ),
    text=combined_df["Bitrate"].apply(lambda x: f'Bitrate: {x:.2f}'),
    name='Bitrate',
))

fig.update_layout(
    mapbox_style="carto-positron",
    map_center=dict(lat=center_lat, lon=center_lon),
    map_zoom=17,
    title_text='Bitrate Map', 
    showlegend=False,
)

fig.show()

```

{{</details>}}

{{< plotly json="/plotly/evaluate-dual-mesh-wifi-connection/plotly_chart_3.json" >}}

The scattermap shows spots where the bandwith values decrease clearly even if there are multiple traces independently. On the other hand there are also spots where high values and low values are measured.

One of these spots is next to the center of the testarea. The occurence of high and low values could indicate there handshake issues in some testraces when driving from one accesspoint to another. Another unclear spot is on the eastside of the map where also high and low values occure. Because we measured some tests from westside to eastside and others from eastside to westside the unclear values could relate to the driving direction.

The eastside was shielded by more buildings and though the process to establishm the WiFi connection could have last longer then on the westside. This would fit also to the feeling I had when I did the measurements.

## Latency to Distance Relation

As already done with the Bitrate Data we'll evaluate the latency of the WiFi connection from the vehicle to the destination host via scatterplot and a heatmap.

The next plot shows that the the latency doesn't really increase that much with increasing distance (as the trendline in the left plot is almost horizontal) but the spread in values seems to get higher with the distance. Even though if we consider that the maximum distance for an accurate Bitrate was 120 meters to the center of the testarea, then can assume latencies between 60 milliseconds and 90 milliseconds for the whole WiFi connection.

{{<details title="show code">}}

```python
## plottling

ROLLAVG_WINDOW_SIZE = int(len(combined_df)*0.1)

scatter_fig = px.scatter(
    combined_df,
    x='DISTANCE_CENTER',
    y='Latency',
    title='Latency vs. Distance to Center with Trendline',
    labels={'DISTANCE_CENTER': 'Distance to Center [m]', 'Latency': 'Latency [ms]'},
    trendline="expanding",
)

histogram_fig = go.Figure(go.Histogram2dContour(
    x=combined_df['DISTANCE_CENTER'],
    y=combined_df['Latency'],
    colorscale='Viridis',
    colorbar=dict(title='Density'),
    contours=dict(coloring='heatmap'),
))

# Create subplots
fig = make_subplots(rows=1, cols=2, subplot_titles=('Latency vs. Distance to Center with Trendline', 'Spread of Latency vs. Distance to Center'))

for trace in scatter_fig['data']:
    fig.add_trace(trace, row=1, col=1)

for trace in histogram_fig['data']:
     fig.add_trace(trace, row=1, col=2)


fig.update_layout(
    title_text='Latency Visualizations',
    template='none'
)

fig.update_xaxes(title_text='Distance to Center [m]', row=1, col=1)
fig.update_yaxes(title_text='Latency [ms]', row=1, col=1)
fig.update_xaxes(title_text='Distance to Center [m]', row=1, col=2)
fig.update_yaxes(title_text='Latency [ms]', row=1, col=2)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/evaluate-dual-mesh-wifi-connection/plotly_chart_2.json" >}}

## Latency to Position Relation
In order to check the latency-results in detail we'll also plot the latencies on a map like we did already with the bandwith results. Because we involved the latency measurement just in the second test session, we have to filter out first the _nan-values_ which will result into a slightly different map compared to the bandwith map above.

{{<details title="show code">}}

```python
# filter out traces with nan-values
combined_df = combined_df.dropna()

center_lat = combined_df["Latitude"].mean()
center_lon = combined_df["Longitude"].mean()

fig = go.Figure()

fig.add_trace(go.Scattermap(
    lat=combined_df["Latitude"], 
    lon=combined_df["Longitude"],
    mode='markers',
    marker=go.scattermap.Marker(
        size=15,
        color=combined_df["Latency"],
        reversescale=True,
        colorbar=dict(title='Latency [ms]', x=1.0)
    ),
    text=combined_df["Latency"].apply(lambda x: f'Latency: {x:.2f}'),
    name='Latency',
))

fig.update_layout(
    mapbox_style="carto-positron",
    map_center=dict(lat=center_lat, lon=center_lon),
    map_zoom=17,
    title_text='Latency Map', 
    showlegend=False,
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/evaluate-dual-mesh-wifi-connection/plotly_chart_1.json" >}}

Even though the critical and possibly by shielding effected spots are still visible in this plot, it seems like the latency isn't effected that much, as there is almost a smooth change in the values when increasing the distance from the accesspoints. This ofcourse fits to the calculated trendline in the first scatterplot. 

The latencies which were measured at eastside and westside seem to be the one with the highest spread when the vehicle was leaving the WiFi area. Unfortunatly we didn't record as many measurements including the latency-informations therefore we cannot make any conclusions about the spread in values. Moreover the latency measurement was just a single ping command which was synchronised with the logging of iperf3 and gpspipe.

## Conclusion

All in all we evaluated a bandwith of at least 30 MBit/s within an area of 120 meters radius. The latencies within this area were between 60ms and 90ms.
The tests were influenced by shieldings of nearer beuildings and also the test setup wasn't ideal to proof for example latency-stability as I dont know much about the way the ping-command is calculating the resulting latencies. Additionally it would have been better if I had recorded more measurements, but due to the fact that the results of this evaluations match my feelings when i did the tests, the two test sessions were good enough.