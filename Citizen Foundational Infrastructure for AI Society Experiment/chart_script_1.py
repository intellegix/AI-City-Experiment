import plotly.graph_objects as go
import plotly.io as pio

# Data from all demographic categories
categories = (
    # Income Tier
    ["Lower Income", "Middle Income", "Upper Income"] +
    # Age Bracket  
    ["Age 18-24", "Age 25-34", "Age 35-44", "Age 45-54", "Age 55-64", "Age 65+"] +
    # Location Type
    ["Urban Core", "Urban Periph", "Suburban", "Small Town", "Rural"] +
    # Education Level
    ["Secondary", "Bachelor", "Graduate", "Vocational"]
)

percentages = (
    # Income Tier
    [30.5, 53.7, 15.8] +
    # Age Bracket
    [12.0, 16.4, 17.3, 14.8, 16.0, 23.5] +
    # Location Type  
    [18.6, 21.0, 18.7, 22.1, 19.6] +
    # Education Level
    [38.0, 35.0, 15.0, 12.0]
)

# Colors for each group
colors = (
    # Income Tier (3 items)
    ['#1FB8CD', '#DB4545', '#2E8B57'] +
    # Age Bracket (6 items)
    ['#5D878F', '#D2BA4C', '#B4413C', '#964325', '#944454', '#13343B'] +
    # Location Type (5 items)
    ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C'] +
    # Education Level (4 items)
    ['#B4413C', '#964325', '#944454', '#13343B']
)

# Create horizontal bar chart
fig = go.Figure(data=go.Bar(
    y=categories,
    x=percentages,
    orientation='h',
    text=[f'{p}%' for p in percentages],
    textposition='inside',
    textfont=dict(color='white', size=12),
    marker=dict(color=colors)
))

# Update layout
fig.update_layout(
    title="AI Society Pop Demographics (N=1000)",
    xaxis_title="Percentage",
    yaxis_title="Demo Categories"
)

# Update traces for better appearance
fig.update_traces(cliponaxis=False)

# Reverse y-axis to show categories in original order
fig.update_yaxes(autorange="reversed")

# Save as PNG and SVG
fig.write_image("demographics_chart.png")
fig.write_image("demographics_chart.svg", format="svg")

fig.show()