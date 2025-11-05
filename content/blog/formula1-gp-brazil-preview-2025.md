---
title: 'formula1 gp brazil preview 2025'
date: '2025-11-05T23:32:52.431915+00:00'
author: 'Giancarlo Rizzo'
draft: true
plotly: true
categories: []
color: '#a09f93'
---

<a href="https://colab.research.google.com/github/protogia/formula1-evaluations/blob/main/formula1-gp-brazil-preview-2025.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## Prologue
It's 5 days before the GP Brazil is starting the next session of Formula1 season 2025 and I decided to evaluate the last 2024 race of this unique circuit with all its special characteristics to make a little preview.

Moreover this notebook is also a try to get some inspiration for a greater analysis of multiple seasons. I am planning to compare as good as possible historical data of choosen cirquits. Therefore I need to get a feeling what kind of analysis makes sense or not.

But for now let's focus on the preview of 2025. The GP Brazil will be held on the Interlagos Race Track. The drivers will complete 71 laps on the 4.309km long circuit and typically have to contend with harsh weather conditions as we will see in the further analysis.

## Preparing

In the next steps we'll install necessary packages, do some preconfigurations and load the data using _fastf1_.

### Install fastf1

{{<details title="Code and Output">}}

```python
%%capture
!pip install fastf1;

import fastf1
```

{{</details>}}

### Preconfiguration

{{<details title="Code and Output">}}

```python
# log-config
import warnings
warnings.filterwarnings('ignore')
```

```python
# layout-config
from IPython.core import display
display.display_html(display.HTML(""))
```

```python
# data-config
# fastf1.Cache.enable_cache('/content')
```

```python
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
```

{{</details>}}

### Loading and Preparing Data

{{<details title="Code and Output">}}

```python
race = fastf1.get_session(2024, "Brazil", identifier="R")
race.load(telemetry=True)
```

    Request for URL https://api.jolpi.ca/ergast/f1/2024/21/results.json failed; using cached response
    Traceback (most recent call last):
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/connectionpool.py", line 534, in _make_request
        response = conn.getresponse()
                   ^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/connection.py", line 565, in getresponse
        httplib_response = super().getresponse()
                           ^^^^^^^^^^^^^^^^^^^^^
      File "/usr/lib/python3.12/http/client.py", line 1428, in getresponse
        response.begin()
      File "/usr/lib/python3.12/http/client.py", line 331, in begin
        version, status, reason = self._read_status()
                                  ^^^^^^^^^^^^^^^^^^^
      File "/usr/lib/python3.12/http/client.py", line 292, in _read_status
        line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/usr/lib/python3.12/socket.py", line 707, in readinto
        return self._sock.recv_into(b)
               ^^^^^^^^^^^^^^^^^^^^^^^
      File "/usr/lib/python3.12/ssl.py", line 1252, in recv_into
        return self.read(nbytes, buffer)
               ^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/usr/lib/python3.12/ssl.py", line 1104, in read
        return self._sslobj.read(len, buffer)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    TimeoutError: The read operation timed out
    
    The above exception was the direct cause of the following exception:
    
    Traceback (most recent call last):
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/requests/adapters.py", line 644, in send
        resp = conn.urlopen(
               ^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/connectionpool.py", line 841, in urlopen
        retries = retries.increment(
                  ^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/util/retry.py", line 474, in increment
        raise reraise(type(error), error, _stacktrace)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/util/util.py", line 39, in reraise
        raise value
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/connectionpool.py", line 787, in urlopen
        response = self._make_request(
                   ^^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/connectionpool.py", line 536, in _make_request
        self._raise_timeout(err=e, url=url, timeout_value=read_timeout)
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/connectionpool.py", line 367, in _raise_timeout
        raise ReadTimeoutError(
    urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='api.jolpi.ca', port=443): Read timed out. (read timeout=5.0)
    
    During handling of the above exception, another exception occurred:
    
    Traceback (most recent call last):
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/requests_cache/session.py", line 286, in _resend
        response = self._send_and_cache(request, actions, cached_response, **kwargs)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/requests_cache/session.py", line 254, in _send_and_cache
        response = super().send(request, **kwargs)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/fastf1/req.py", line 136, in send
        return super().send(request, **kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/requests/sessions.py", line 703, in send
        r = adapter.send(request, **kwargs)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/requests/adapters.py", line 690, in send
        raise ReadTimeout(e, request=request)
    requests.exceptions.ReadTimeout: HTTPSConnectionPool(host='api.jolpi.ca', port=443): Read timed out. (read timeout=5.0)
    Request for URL https://api.jolpi.ca/ergast/f1/2024/21/laps/1.json failed; using cached response
    Traceback (most recent call last):
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/connectionpool.py", line 534, in _make_request
        response = conn.getresponse()
                   ^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/connection.py", line 565, in getresponse
        httplib_response = super().getresponse()
                           ^^^^^^^^^^^^^^^^^^^^^
      File "/usr/lib/python3.12/http/client.py", line 1428, in getresponse
        response.begin()
      File "/usr/lib/python3.12/http/client.py", line 331, in begin
        version, status, reason = self._read_status()
                                  ^^^^^^^^^^^^^^^^^^^
      File "/usr/lib/python3.12/http/client.py", line 292, in _read_status
        line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/usr/lib/python3.12/socket.py", line 707, in readinto
        return self._sock.recv_into(b)
               ^^^^^^^^^^^^^^^^^^^^^^^
      File "/usr/lib/python3.12/ssl.py", line 1252, in recv_into
        return self.read(nbytes, buffer)
               ^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/usr/lib/python3.12/ssl.py", line 1104, in read
        return self._sslobj.read(len, buffer)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    TimeoutError: The read operation timed out
    
    The above exception was the direct cause of the following exception:
    
    Traceback (most recent call last):
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/requests/adapters.py", line 644, in send
        resp = conn.urlopen(
               ^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/connectionpool.py", line 841, in urlopen
        retries = retries.increment(
                  ^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/util/retry.py", line 474, in increment
        raise reraise(type(error), error, _stacktrace)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/util/util.py", line 39, in reraise
        raise value
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/connectionpool.py", line 787, in urlopen
        response = self._make_request(
                   ^^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/connectionpool.py", line 536, in _make_request
        self._raise_timeout(err=e, url=url, timeout_value=read_timeout)
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/urllib3/connectionpool.py", line 367, in _raise_timeout
        raise ReadTimeoutError(
    urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='api.jolpi.ca', port=443): Read timed out. (read timeout=5.0)
    
    During handling of the above exception, another exception occurred:
    
    Traceback (most recent call last):
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/requests_cache/session.py", line 286, in _resend
        response = self._send_and_cache(request, actions, cached_response, **kwargs)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/requests_cache/session.py", line 254, in _send_and_cache
        response = super().send(request, **kwargs)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/fastf1/req.py", line 136, in send
        return super().send(request, **kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/requests/sessions.py", line 703, in send
        r = adapter.send(request, **kwargs)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/working/.cache/pypoetry/virtualenvs/formula1-evaluations-04DUQJVu-py3.12/lib/python3.12/site-packages/requests/adapters.py", line 690, in send
        raise ReadTimeout(e, request=request)
    requests.exceptions.ReadTimeout: HTTPSConnectionPool(host='api.jolpi.ca', port=443): Read timed out. (read timeout=5.0)

{{</details>}}

## Track Overview
As mentioned the circuit in Sao Paulo has a length of 4.309km seperated into 15 sectors/corners. It contains two highspeed sections as well as small corners with different radius.

As shown in the next chart especially the section from _corner 3_ up to _corner 7_ as well as _corner 8_ to _corner 12_ are characterized by small radiuses and at the same time by many changes of the gradient.

The long high speed sections are also different to each other. While the section from _corner 13_ to _corner 15_ changes the gradient four times, the second section (_sector 3_) has a negative steep hill downwards with a gradient up to -8.75% which makes it hard for the drivers to find the right brake point when entering _corner 4_.

{{<details title="Code and Output">}}

```python
position = race.laps.pick_fastest().get_pos_data()
circuit_info = race.get_circuit_info()
```

```python
def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)
```

```python
# Get an array of shape [n, 2] where n is the number of points and the second
# axis is x and y.
track = position.loc[:, ('X', 'Y')].to_numpy()

# Convert the rotation angle from degrees to radian.
track_angle = circuit_info.rotation / 180 * np.pi

rotated_track = rotate(track, angle=track_angle)
```

```python
reference_altitude = 800

# assuming the Z data is already in meters, we just need to add the reference altitude
altitude_meters = position['Z'].values + reference_altitude

# Calculate the gradient of the altitude
# Using numpy.gradient to calculate the gradient along the track points
# We need to calculate the gradient with respect to distance along the track, not just the index
# A simplified approach is to calculate the difference between consecutive altitude values
altitude_gradient = np.gradient(altitude_meters)


# scatter plot with color scale based on the altitude gradient
fig = go.Figure(data=go.Scatter(
    x=rotated_track[:, 0],
    y=rotated_track[:, 1],
    mode='lines+markers',
    marker=dict(
        size=5,
        color=altitude_gradient,
        colorscale='Plasma',
        colorbar=dict(title='Altitude Gradient'),
        opacity=0.8
    ),
    line=dict( # track
        color='grey',
        width=1
    ),
    hoverinfo='text',
    text=[f'Altitude Gradient: {grad:.2f}%' for grad in altitude_gradient]
))

# add corner information as annotations
track_angle = circuit_info.rotation / 180 * np.pi # track rotation angle

for _, corner in circuit_info.corners.iterrows():
    # Rotate the center of the corner equivalently to the rest of the track map
    txt = f"{corner['Number']}{corner['Letter']}"
    track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle)
    fig.add_annotation(
        x=track_x,
        y=track_y,
        text=txt,
        showarrow=False, # Do not show arrow
        bgcolor="grey",
        font=dict(
            color="white",
            size=10
        )
    )

fig.update_layout(
    title='Track Overview with Altitude Gradient and Corners',
    xaxis_title='X Coordinate',
    yaxis_title='Y Coordinate',
    yaxis=dict(scaleanchor="x", scaleratio=1), # Ensure aspect ratio is equal
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-preview-2025/plotly_chart_10.json" >}}

The following lineplot shows the altitude gradient over all corners to make this special point clearer. If we can trust the data there is a lot of changes in altitude even between the short sections between the corners.

{{<details title="Code and Output">}}

```python
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.colors as colors # Import plotly.colors

# Calculate the distance along the track
# Calculate the difference in X and Y between consecutive points
delta_x = position['X'].diff().fillna(0)
delta_y = position['Y'].diff().fillna(0)

# Calculate the distance between consecutive points
distances = np.sqrt(delta_x**2 + delta_y**2)

# Calculate the cumulative distance along the track
cumulative_distance = distances.cumsum()/10


# Create a color scale based on the altitude gradient values
colorscale = 'Plasma'
min_gradient, max_gradient = np.min(altitude_gradient), np.max(altitude_gradient)

# Get the colors from the colorscale
plasma_colors = colors.get_colorscale(colorscale)

# Create a list of segments with start and end points and their corresponding gradient and color
segments = []
for i in range(len(altitude_gradient) - 1):
    segment_gradient = (altitude_gradient[i] + altitude_gradient[i+1]) / 2 # Average gradient for the segment
    normalized_segment_gradient = (segment_gradient - min_gradient) / (max_gradient - min_gradient) if (max_gradient - min_gradient) != 0 else 0

    # Interpolate color from the colorscale
    segment_color = colors.sample_colorscale(plasma_colors, normalized_segment_gradient)[0]


    segment = {
        'x': [cumulative_distance.iloc[i], cumulative_distance.iloc[i+1]], # Use cumulative distance for x
        'y': [altitude_gradient[i], altitude_gradient[i+1]],
        'gradient': segment_gradient,
        'color': segment_color # Store the calculated color for the segment
    }
    segments.append(segment)

# Create the figure
fig = go.Figure()

# Add each segment as a separate Scatter trace with a colored line
for segment in segments:
    fig.add_trace(go.Scatter(
        x=segment['x'],
        y=segment['y'],
        mode='lines', # Only lines, no markers needed for this visualization
        line=dict(color=segment['color'], width=2), # Color the line by segment gradient
        hoverinfo='text',
        text=f'Altitude Gradient: {segment["gradient"]:.2f}',
        showlegend=False # Hide legend for individual segments
    ))

# Add a single Scatter trace for the colorbar. We use the original data for this.
fig.add_trace(go.Scatter(
    x=[None], # No x or y data
    y=[None],
    mode='markers', # Use markers mode to display the colorbar
    marker=dict(
        colorscale=colorscale,
        showscale=True,
        colorbar=dict(title='Altitude Gradient'),
        cmin=min_gradient,
        cmax=max_gradient,
        color=altitude_gradient # Use the full gradient data for the color mapping in the colorbar trace
    ),
    hoverinfo='none',
    showlegend=False
))


# Add vertical lines for corner information
for _, corner in circuit_info.corners.iterrows():
    # Find the cumulative distance at the corner's position
    # This requires finding the point in the cumulative_distance Series closest to the corner's X and Y coordinates.
    # We can approximate this by finding the index in the position data closest to the corner's position
    distances_to_corner = np.sqrt((position['X'] - corner['X'])**2 + (position['Y'] - corner['Y'])**2)
    closest_pos_index = distances_to_corner.idxmin()
    corner_cumulative_distance = cumulative_distance.iloc[closest_pos_index]


    # Add a vertical line at the closest cumulative distance
    fig.add_vline(
        x=corner_cumulative_distance,
        line_width=1,
        line_dash="dash",
        line_color="red",
        annotation_text=f"C-{corner['Number']}{corner['Letter']}",
        annotation_position="top right"
    )


fig.update_layout(
    title='Altitude Gradient Along the Track with Corners',
    xaxis_title='Distance along Track [m]', # Update x-axis title
    yaxis_title='Altitude Gradient [%]',
)

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-preview-2025/plotly_chart_9.json" >}}

As if the track weren't challenging enough, the GP Brazil is ​​also known for difficult weather conditions. Sao Paulo is characterized by subtropical climate conditions and november is typically the start of summer there. [This leads into an average amount of precipitation of 145l/m² or in simple words: It's raining a lot. Furthermore the average temperature lays between 15,6°C and 24,9°C in this period while the average relative humidity is around 73.7%](https://en.wikipedia.org/wiki/S%C3%A3o_Paulo#cite_ref-NCB-1931-1960_83-0).

The next chart shows the weather conditions for the GP Brazil 2024. Almost half of the race was driven while raining. The temperature was between 23°C at the beginning of the race and 20°C at the end, whereas the track temperature layed between 29,5°C at driest phase of the race and 23,3°C when it was raining.

{{<details title="Code and Output">}}

```python
from plotly.subplots import make_subplots

# Convert the Time column to a string format for plotting
weather_data_str_time = race.weather_data.copy()
weather_data_str_time['Time_str'] = weather_data_str_time['Time'].apply(lambda x: str(x).split(' ')[-1]) # Extract HH:MM:SS


# Create subplots with multiple y-axes
weather_fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces for each weather metric
weather_fig.add_trace(
    go.Scatter(x=weather_data_str_time['Time_str'], y=weather_data_str_time['AirTemp'], name='Air Temp'),
    secondary_y=False,
)

weather_fig.add_trace(
    go.Scatter(x=weather_data_str_time['Time_str'], y=weather_data_str_time['TrackTemp'], name='Track Temp'),
    secondary_y=False,
)

weather_fig.add_trace(
    go.Scatter(x=weather_data_str_time['Time_str'], y=weather_data_str_time['Humidity'], name='Humidity'),
    secondary_y=True,
)

weather_fig.add_trace(
    go.Scatter(x=weather_data_str_time['Time_str'], y=weather_data_str_time['Pressure'], name='Pressure'),
    secondary_y=True,
)

weather_fig.add_trace(
    go.Scatter(x=weather_data_str_time['Time_str'], y=weather_data_str_time['WindSpeed'], name='Wind Speed'),
    secondary_y=True,
)

# Update layout to ensure y-axis range is set
weather_fig.update_layout(
    title='Weather Data During the Race',
    xaxis_title='Time', # Keep Time as x-axis title
    legend_title='Metric'
)

weather_fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False)
weather_fig.update_yaxes(title_text="Value", secondary_y=True)

# Get the y-axis range after adding traces and updating layout
y_range_primary = weather_fig.layout.yaxis.range


# Add shading to indicate rain
# Find the start and end times of consecutive rain periods
rain_periods_str_time = weather_data_str_time[weather_data_str_time['Rainfall'] == True].copy()
if not rain_periods_str_time.empty:
    # Identify consecutive rain periods based on original Time difference
    rain_periods_str_time['rain_group'] = (rain_periods_str_time['Time'].diff() > pd.Timedelta(seconds=65)).cumsum()
    for group_id, group_df in rain_periods_str_time.groupby('rain_group'):
        start_time_str = group_df['Time_str'].min()
        end_time_str = group_df['Time_str'].max()

        # Use a default range if the actual range is still None
        y0_val = y_range_primary[0] if y_range_primary is not None else 0
        y1_val = y_range_primary[1] if y_range_primary is not None else 100 # Assuming a reasonable default max value


        weather_fig.add_shape(
            type="rect",
            x0=start_time_str,
            y0=y0_val,  # Start at the bottom of the primary y-axis
            x1=end_time_str,
            y1=y1_val,  # End at the top of the primary y-axis
            fillcolor="blue",
            opacity=0.2,
            layer="below",
            line_width=0,
        )
    # Add a single legend entry for "Rain"
    weather_fig.add_trace(go.Scatter(
        x=[None], y=[None], # Invisible trace
        mode='markers',
        marker=dict(size=10, color="blue", opacity=0.5),
        legendgroup='Rain',
        showlegend=True,
        name='Rain'
    ))


weather_fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-preview-2025/plotly_chart_8.json" >}}

## Analysing Tyre-Strategy by driver

In the next step we'll check out the tyre strategies which were choosen by the drivers and their teams. Even though these stongly depend on what happened within the race, I think it can be helpfull to make some basic guess.

{{<details title="Code and Output">}}

```python
drivers = race.laps['Driver'].unique()
```

```python
stints = race.laps[['Driver', 'Stint', 'Compound', 'LapNumber']]
stints = stints.groupby(['Driver', 'Stint', 'Compound']).count().reset_index()
stints = stints.rename(columns={'LapNumber': 'LapCount'})
```

```python
track_status_changes = race.track_status.copy()
```

```python
compound_colors = {
    'SOFT': 'red',
    'MEDIUM': 'yellow',
    'HARD': 'white',
    'INTERMEDIATE': 'green',
    'WET': 'blue'
}

fig = go.Figure()

# use set to avoid duplicate legend entries
added_compounds = set()

for driver in drivers:
    driver_stints = stints.loc[stints["Driver"] == driver].sort_values(by='Stint') # Sort by stint to ensure correct stacking

    previous_stint_end = 0
    for idx, row in driver_stints.iterrows():
        compound = row["Compound"]
        color = compound_colors.get(compound.upper(), 'gray') # Get color from dictionary, default to gray

        # determine whether to show the legend entry for this compound
        show_legend_entry = False
        if compound not in added_compounds:
            added_compounds.add(compound)
            show_legend_entry = True

        fig.add_trace(go.Bar(
            y=[driver],
            x=[row["LapCount"]],
            name=compound,
            orientation='h',
            marker=dict(
                color=color,
                line=dict(color='white', width=2)
            ),
            base=previous_stint_end,
            customdata=[compound], # compound name in customdata for hover
            hovertemplate='Driver: %{y}<br>Compound: %{customdata}<br>Laps: %{x}<extra></extra>', # Custom hover text
            showlegend=show_legend_entry
        ))

        previous_stint_end += row["LapCount"]

fig.update_layout(
    title='Tyre Strategy per Driver',
    xaxis_title='Lap Number',
    yaxis_title='Driver',
    barmode='stack',
    legend_title='Compound',
    yaxis=dict(autorange="reversed"), # Invert y-axis
    height=800 # Adjust height for better readability
)

###
# add vertical lines
track_status_colors = {
    "AllClear": "green",
    "Yellow": "yellow",
    "Red": "red",
    "SCDeployed": "purple",
    "VSCDeployed": "violet",
    "VSCEnding": "orange",
}

# filter race.track_status for relevant statuses
filtered_track_status_changes = race.track_status[
    race.track_status['Message'].isin(track_status_colors.keys())
].copy()

# add a 'Lap' column to filtered_track_status_changes by finding the lap number closest to the event time
filtered_track_status_changes['Lap'] = filtered_track_status_changes['Time'].apply(
    lambda event_time: race.laps.loc[race.laps['Time'] <= event_time, 'LapNumber'].max() if not race.laps.loc[race.laps['Time'] <= event_time].empty else None
)

# remove rows where Lap is None (no corresponding lap found)
filtered_track_status_changes.dropna(subset=['Lap'], inplace=True)

# convert Lap column to integer
filtered_track_status_changes['Lap'] = filtered_track_status_changes['Lap'].astype(int)


# Group by Lap to handle multiple events per lap
grouped_track_status = filtered_track_status_changes.groupby('Lap')


# add vertical lines for track status changes
for lap, lap_events in grouped_track_status:
    # Determine the color of the vertical line based on the first event in the lap
    line_color = track_status_colors.get(lap_events.iloc[0]['Message'], 'gray')

    # Add a single vertical line for the lap
    fig.add_vline(
        x=lap,
        line_width=2,
        line_dash="dash",
        line_color=line_color, # Use the determined color for the line
        layer="above", # ensure lines are above bars
    )

    # Add scatter markers for each event in the lap with vertical offset
    num_events = len(lap_events)
    # Create a small vertical offset for each marker in the same lap
    vertical_offsets = np.linspace(-0.2, 0.2, num_events) # Adjust the range and number of points as needed

    # Use the index of the first driver as a reference point for the vertical position of the markers
    # This assumes the y-axis categories are the driver names
    if drivers.size > 0:
        driver_y_index = fig.layout.yaxis.categoryarray.index(drivers[0]) if fig.layout.yaxis.categoryarray is not None else 0
    else:
        driver_y_index = 0 # Default to 0 if no drivers are found

    for i, (index, row) in enumerate(lap_events.iterrows()):
        event_color = track_status_colors.get(row['Message'], 'gray')

        fig.add_trace(go.Scatter(
            x=[row['Lap']],
            y=[driver_y_index + vertical_offsets[i]], # Use a consistent y-position with offset based on the first driver
            mode='markers',
            marker=dict(
                size=10,
                color=event_color,
                symbol='circle', # Or any other symbol
                line=dict(color='black', width=1)
            ),
            hoverinfo='text',
            text=f"Track Status: {row['Message']}, Lap {row['Lap']}",
            showlegend=False # Hide legend for individual markers
        ))

# Create a legend for the track status colors by adding invisible traces
for status, color in track_status_colors.items():
    fig.add_trace(go.Scatter(
        x=[None], # No data
        y=[None],
        mode='markers',
        marker=dict(size=10, color=color, symbol='circle'),
        legendgroup='Track Status',
        showlegend=True,
        name=status
    ))

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-preview-2025/plotly_chart_7.json" >}}

As you can see by hovering above the vertical dash-lines there were three situations that caused a red flag (lap 11,31, 43). All teams decided to take the red flag in lap 31 to make a pit stop and change tires. Because of the beginning rain in lap 26, 5 drivers took the decision to use the wet compound. This could have been the wrong decision as they could have lost time but because of the red flag in lap 31 all drivers had the chance to take the intermediate compund tyres again.

In the next plot we will try to compare the average laptime with the Intermediate Compound Tyres and the Wet Compound Tires and moreover evaluating the pit stop time of these drivers.

## Analysing Laptime Performence per Driver

{{<details title="Code and Output">}}

```python
# drivers that used wet compound
choosen_drivers = ['TSU', 'LAW', 'PER', 'ZHO', 'HUL']

for driver in choosen_drivers:
  data = race.laps[race.laps['Driver'] == driver]
```

```python
driver_laps_by_compound = {}

for driver in drivers:
    driver_laps = race.laps[race.laps['Driver'] == driver].copy()
    wet_intermediate_laps = driver_laps[driver_laps['Compound'].isin(['WET', 'INTERMEDIATE'])].copy()
    driver_laps_by_compound[f'{driver}_wet_intermediate_laps'] = wet_intermediate_laps

print(driver_laps_by_compound.keys())
```

    dict_keys(['VER_wet_intermediate_laps', 'GAS_wet_intermediate_laps', 'PER_wet_intermediate_laps', 'ALO_wet_intermediate_laps', 'LEC_wet_intermediate_laps', 'STR_wet_intermediate_laps', 'TSU_wet_intermediate_laps', 'ZHO_wet_intermediate_laps', 'HUL_wet_intermediate_laps', 'LAW_wet_intermediate_laps', 'OCO_wet_intermediate_laps', 'NOR_wet_intermediate_laps', 'COL_wet_intermediate_laps', 'HAM_wet_intermediate_laps', 'BEA_wet_intermediate_laps', 'SAI_wet_intermediate_laps', 'RUS_wet_intermediate_laps', 'BOT_wet_intermediate_laps', 'PIA_wet_intermediate_laps'])

```python
# Access race control messages
race_control_messages = race.race_control_messages

# Filter for relevant track status changes
track_status_changes = race_control_messages[
    race_control_messages['Category'].isin(['Track Status', 'SafetyCar', 'RedFlag', 'VSC'])
].copy()

# Get the session start time
session_start_time = race.session_start_time

# Convert race.laps['Time'] (timedelta from start) to datetime objects by adding session start time
race.laps['DateTime'] = session_start_time + race.laps['Time']

# Ensure 'Time' in track_status_changes is datetime
if not pd.api.types.is_datetime64_any_dtype(track_status_changes['Time']):
    track_status_changes['Time'] = pd.to_datetime(track_status_changes['Time'])

# Convert Time to lap number by finding the closest lap time
lap_numbers = []
for index, row in track_status_changes.iterrows():
    # Calculate absolute time differences between the track status change time and all lap datetimes
    # Ensure both are datetime before subtraction
    if pd.api.types.is_datetime64_any_dtype(race.laps['DateTime']) and pd.api.types.is_datetime64_any_dtype(row['Time']):
        time_diffs = np.abs(race.laps['DateTime'] - row['Time'])

        # Find the index of the minimum time difference
        closest_lap_index = time_diffs.idxmin()

        # Get the LapNumber corresponding to the closest time
        lap_numbers.append(race.laps.loc[closest_lap_index, 'LapNumber'])
    else:
        # If types are not compatible, append None
        lap_numbers.append(None)


# Add the determined lap numbers to the track_status_changes DataFrame
track_status_changes['LapNumber'] = lap_numbers

# Remove any rows where a corresponding lap number could not be found
track_status_changes = track_status_changes.dropna(subset=['LapNumber'])

# Convert the 'LapNumber' column to integer type
track_status_changes['LapNumber'] = track_status_changes['LapNumber'].astype(int)
```

```python
# Define track status colors if not already defined
track_status_colors = {
    "AllClear": "green",
    "Yellow": "yellow",
    "Red": "red",
    "SCDeployed": "purple",
    "VSCDeployed": "violet",
    "VSCEnding": "orange"
}

# Define compound colors if not already defined
compound_colors = {
    'SOFT': 'red',
    'MEDIUM': 'yellow',
    'HARD': 'white',
    'INTERMEDIATE': 'green',
    'WET': 'blue'
}

for driver in choosen_drivers:
    driver_df = driver_laps_by_compound.get(f'{driver}_wet_intermediate_laps')

    if driver_df is not None and not driver_df.empty:
        driver_df['LapTimeSeconds'] = driver_df['LapTime'].dt.total_seconds()

        # current driver's lap times
        fig = px.bar(driver_df,
                     x='LapNumber',
                     y='LapTimeSeconds',
                     color='Compound',
                     title=f'{driver} Lap Times by Compound',
                     labels={'LapTimeSeconds': 'Lap Time (seconds)'},
                     color_discrete_map=compound_colors) # Use the defined compound_colors

        fig.update_layout(
            xaxis_title='Lap Number',
            yaxis_title='Lap Time (seconds)',
            showlegend=True # Ensure legend is shown
        )

        # add vertical lines for track status changes
        for lap, lap_events in grouped_track_status:
            line_color = track_status_colors.get(lap_events.iloc[0]['Message'], 'gray')

            # add a single vertical line for the lap
            fig.add_vline(
                x=lap,
                line_width=2,
                line_dash="dash",
                line_color=line_color, # Use the determined color for the line
                layer="above", # ensure lines are above bars
            )

            # Add scatter markers for each event in the lap with vertical offset
            num_events = len(lap_events)
            # Create a small vertical offset for each marker in the same lap
            vertical_offsets = np.linspace(-2, 2, num_events) # Adjust the range and number of points as needed for lap time scale

            # Use a consistent y-position for the markers, adjusting for the vertical offset
            # A fixed y-position or a position relative to the plot's y-axis range could be used
            # Let's use a position relative to the bottom of the y-axis range
            y_position_base = fig.layout.yaxis.range[0] if fig.layout.yaxis.range else 0


            for i, (index, row) in enumerate(lap_events.iterrows()):
                event_color = track_status_colors.get(row['Message'], 'gray')

                fig.add_trace(go.Scatter(
                    x=[row['Lap']],
                    y=[y_position_base + vertical_offsets[i]], # Use a consistent y-position with offset
                    mode='markers',
                    marker=dict(
                        size=10,
                        color=event_color,
                        symbol='circle', # Or any other symbol
                        line=dict(color='black', width=1)
                    ),
                    hoverinfo='text',
                    text=f"Track Status: {row['Message']}, Lap {row['Lap']}",
                    showlegend=False # Hide legend for individual markers
                ))

        # legend for the track status colors by adding invisible traces
        for status, color in track_status_colors.items():
            fig.add_trace(go.Scatter(
                x=[None], # No data
                y=[None],
                mode='markers',
                marker=dict(size=10, color=color, symbol='circle'),
                legendgroup='Track Status',
                showlegend=True,
                name=status
            ))

        # plot for the current driver
        fig.show()
    else:
        print(f"No wet or intermediate laps found for driver {driver}")
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-preview-2025/plotly_chart_6.json" >}}

The driver specific charts for _Laptime by Compund_ are showing only the laptimes for the drivers that used the wet compound. At the first look it seems like the laptime is increasing when changing on the wet compound tyres but as indicated by thar dashed lines and scatters all laps with this tyres were driven when the Virtual Safety Car was deployed. Therefore the laps driven with the wet compound are not compareable to the others.

Also the pit stops were effected by the _deployment of the virtual safety car_ in lap 27 and the _red flag_ in lap 31 as you can see by the long pit stops in next chart.

{{<details title="Code and Output">}}

```python
# Calculate total pit stop time and individual pit stop times for each driver in choosen_drivers
pitstop_times = {}
individual_pitstop_durations = {}

for driver in choosen_drivers:
    driver_laps = race.laps.pick_driver(driver).reset_index(drop=True)

    # Filter for laps where the driver entered the pits
    pit_in_laps = driver_laps.loc[driver_laps['PitInTime'].notnull()]

    total_pitstop_duration = pd.Timedelta(seconds=0)
    driver_pitstop_list = []

    for index, pit_in_lap in pit_in_laps.iterrows():
        # Find the next lap where the driver exited the pits
        # We need to find the lap *after* the pit-in lap where PitOutTime is not null
        next_lap_index = pit_in_lap.name + 1
        if next_lap_index < len(driver_laps):
            pit_out_lap = driver_laps.loc[next_lap_index]
            if pd.notnull(pit_out_lap['PitOutTime']):
                # Calculate the duration from PitInTime of the current lap to PitOutTime of the next lap
                # Ensure both are Timedelta objects before subtraction
                if isinstance(pit_in_lap['PitInTime'], pd.Timedelta) and isinstance(pit_out_lap['PitOutTime'], pd.Timedelta):
                     pitstop_duration = pit_out_lap['PitOutTime'] - pit_in_lap['PitInTime']
                else:
                     # If not Timedelta, try converting and then calculate
                     try:
                         pitstop_duration = pd.to_timedelta(pit_out_lap['PitOutTime']) - pd.to_timedelta(pit_in_lap['PitInTime'])
                     except ValueError:
                         pitstop_duration = pd.Timedelta(seconds=0) # Handle cases where conversion fails


                total_pitstop_duration += pitstop_duration
                driver_pitstop_list.append({'LapNumber': pit_in_lap['LapNumber'], 'Duration': pitstop_duration})
            else:
                 # If PitOutTime is null in the next lap, the pit stop might span multiple laps or data is missing
                 # For simplicity, we'll skip this pit stop or handle it as an error for now
                 print(f"Warning: Could not find PitOutTime for pit stop starting on Lap {pit_in_lap['LapNumber']} for driver {driver}")


    pitstop_times[driver] = total_pitstop_duration
    individual_pitstop_durations[driver] = driver_pitstop_list
```

```python
# Convert the individual_pitstop_durations dictionary to a DataFrame
individual_pitstops_list = []
for driver, stops in individual_pitstop_durations.items():
    for stop in stops:
        individual_pitstops_list.append({'Driver': driver, 'LapNumber': stop['LapNumber'], 'PitStopDurationSeconds': stop['Duration'].total_seconds()})

individual_pitstops_df = pd.DataFrame(individual_pitstops_list)

# Create a bar plot for individual pit stops
fig = px.bar(individual_pitstops_df,
             x='LapNumber',
             y='PitStopDurationSeconds',
             color='Driver',
             title='Individual Pit Stop Durations per Driver',
             labels={'LapNumber': 'Lap Number', 'PitStopDurationSeconds': 'Pit Stop Duration (seconds)'},
             barmode='group' # Use barmode 'group' to show bars side by side for each lap
            )

fig.update_layout(xaxis_title='Lap Number', yaxis_title='Pit Stop Duration (seconds)')

# add vertical lines for track status changes
for lap, lap_events in grouped_track_status:
    if lap > 23 and lap < 35:
        line_color = track_status_colors.get(lap_events.iloc[0]['Message'], 'gray')

        # add a single vertical line for the lap
        fig.add_vline(
            x=lap,
            line_width=2,
            line_dash="dash",
            line_color=line_color, # Use the determined color for the line
            layer="above", # ensure lines are above bars
        )

        # Add scatter markers for each event in the lap with vertical offset
        num_events = len(lap_events)
        # Create a small vertical offset for each marker in the same lap
        vertical_offsets = np.linspace(0, fig.layout.yaxis.range[1] if fig.layout.yaxis.range else 50, num_events) # Adjust the range and number of points as needed

        for i, (index, row) in enumerate(lap_events.iterrows()):
            event_color = track_status_colors.get(row['Message'], 'gray')

            fig.add_trace(go.Scatter(
                x=[row['Lap']],
                y=[vertical_offsets[i]], # Use a consistent y-position with offset
                mode='markers',
                marker=dict(
                    size=10,
                    color=event_color,
                    symbol='circle', # Or any other symbol
                    line=dict(color='black', width=1)
                ),
                hoverinfo='text',
                text=f"Track Status: {row['Message']}, Lap {row['Lap']}",
                showlegend=False # Hide legend for individual markers
            ))

# legend for the track status colors by adding invisible traces
for status, color in track_status_colors.items():
    fig.add_trace(go.Scatter(
        x=[None], # No data
        y=[None],
        mode='markers',
        marker=dict(size=10, color=color, symbol='circle'),
        legendgroup='Track Status',
        showlegend=True,
        name=status
    ))

fig.show()
```

{{</details>}}

{{< plotly json="/plotly/formula1-gp-brazil-preview-2025/plotly_chart_1.json" >}}