import plotly.graph_objects as go

# Create a layered architecture diagram using Plotly
fig = go.Figure()

# Define the layers and their components
layers = [
    {
        'name': 'Layer 1 - Rendering',
        'y': 3,
        'components': ['Virtual DOM', 'Memoization', 'GPU Accel', 'RAF Schedule'],
        'color': '#B3E5EC'
    },
    {
        'name': 'Layer 2 - State', 
        'y': 2,
        'components': ['State Machines', 'Store (Redux)', 'Optimistic Up'],
        'color': '#FFCDD2'
    },
    {
        'name': 'Layer 3 - Memory',
        'y': 1, 
        'components': ['Object Pool', 'Asset Stream', 'GC Optimize'],
        'color': '#A5D6A7'
    },
    {
        'name': 'Layer 4 - Events',
        'y': 0,
        'components': ['Delegation', 'Throttling', 'Event Bus'],
        'color': '#FFEB8A'
    }
]

# Add layer rectangles and components
for layer in layers:
    y = layer['y']
    
    # Add layer background rectangle
    fig.add_shape(
        type="rect",
        x0=0,
        y0=y - 0.35,
        x1=6,
        y1=y + 0.35,
        fillcolor=layer['color'],
        line=dict(color="#333333", width=2),
        opacity=0.9
    )
    
    # Add layer title
    fig.add_annotation(
        x=0.2,
        y=y + 0.15,
        text=layer['name'],
        showarrow=False,
        font=dict(size=14, color="#13343B", family="Arial Black"),
        xanchor="left"
    )
    
    # Add components as text within the layer
    component_text = " • ".join(layer['components'])
    fig.add_annotation(
        x=0.2,
        y=y - 0.1,
        text=component_text,
        showarrow=False,
        font=dict(size=11, color="#13343B"),
        xanchor="left"
    )

# Add bidirectional arrows between adjacent layers
for i in range(len(layers) - 1):
    current_y = layers[i]['y']
    next_y = layers[i + 1]['y']
    
    # Downward arrow (left side)
    fig.add_annotation(
        x=6.2,
        y=next_y + 0.25,
        ax=6.2,
        ay=current_y - 0.25,
        arrowhead=3,
        arrowsize=1.5,
        arrowwidth=3,
        arrowcolor="#13343B",
        showarrow=True
    )
    
    # Upward arrow (right side) 
    fig.add_annotation(
        x=6.5,
        y=current_y - 0.25,
        ax=6.5,
        ay=next_y + 0.25,
        arrowhead=3,
        arrowsize=1.5,
        arrowwidth=3,
        arrowcolor="#13343B",
        showarrow=True
    )

# Add arrow labels
fig.add_annotation(
    x=6.8,
    y=1.5,
    text="Bidirectional<br>Data Flow",
    showarrow=False,
    font=dict(size=10, color="#13343B"),
    xanchor="left"
)

# Update layout
fig.update_layout(
    title="Layered Architecture",
    xaxis=dict(
        range=[-0.2, 8],
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    yaxis=dict(
        range=[-0.7, 3.7],
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    showlegend=False,
    plot_bgcolor="white"
)

# Save the chart
fig.write_image("layered_architecture.png")
fig.write_image("layered_architecture.svg", format="svg")

print("Updated layered architecture diagram with bidirectional arrows created successfully!")