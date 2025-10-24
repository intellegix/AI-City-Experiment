import plotly.graph_objects as go
import plotly.express as px
import json
import numpy as np
import math

# Data for the network
data = {
  "nodes": [
    {"id": "agent", "label": "AI Citizen Agent", "group": "core", "size": 50},
    {"id": "llm", "label": "LLM Core", "group": "internal", "size": 35},
    {"id": "memory", "label": "Memory System", "group": "internal", "size": 35},
    {"id": "personality", "label": "Personality", "group": "internal", "size": 35},
    {"id": "needs", "label": "Needs Framework", "group": "internal", "size": 35},
    {"id": "decision", "label": "Decision Engine", "group": "internal", "size": 35},
    {"id": "environment", "label": "Environment", "group": "external", "size": 38},
    {"id": "other_agents", "label": "Other Agents", "group": "social", "size": 38},
    {"id": "network", "label": "Social Network", "group": "social", "size": 38},
    {"id": "economy", "label": "Economic System", "group": "external", "size": 38}
  ],
  "edges": [
    {"source": "agent", "target": "llm"},
    {"source": "agent", "target": "memory"},
    {"source": "agent", "target": "personality"},
    {"source": "agent", "target": "needs"},
    {"source": "agent", "target": "decision"},
    {"source": "agent", "target": "environment"},
    {"source": "agent", "target": "other_agents"},
    {"source": "agent", "target": "network"},
    {"source": "agent", "target": "economy"},
    {"source": "llm", "target": "decision"},
    {"source": "memory", "target": "decision"},
    {"source": "personality", "target": "decision"},
    {"source": "needs", "target": "decision"},
    {"source": "other_agents", "target": "network"},
    {"source": "environment", "target": "economy"}
  ]
}

# Create a mapping from node id to index
node_dict = {node['id']: i for i, node in enumerate(data['nodes'])}

# Position nodes with better balanced distribution
positions = {}
center_x, center_y = 0, 0

# Place central agent at center
positions['agent'] = (center_x, center_y)

# Group nodes by category
internal_nodes = [n for n in data['nodes'] if n['group'] == 'internal']
external_nodes = [n for n in data['nodes'] if n['group'] == 'external']
social_nodes = [n for n in data['nodes'] if n['group'] == 'social']

# Better radius for balanced layout
radius = 4.0

# Position internal nodes (blue) - distributed around upper portion
internal_angles = [math.pi/6, math.pi/2, 5*math.pi/6, 7*math.pi/6, 3*math.pi/2, 11*math.pi/6]
for i, node in enumerate(internal_nodes):
    angle = internal_angles[i]
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    positions[node['id']] = (x, y)

# Position external nodes (green) - left and bottom left
external_angles = [math.pi, 4*math.pi/3]
for i, node in enumerate(external_nodes):
    angle = external_angles[i]
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    positions[node['id']] = (x, y)

# Position social nodes (orange) - right side
social_angles = [0, -math.pi/3]
for i, node in enumerate(social_nodes):
    angle = social_angles[i]
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    positions[node['id']] = (x, y)

# Correct color mapping following instructions exactly
color_map = {
    'core': '#1FB8CD',      # Strong cyan for central agent
    'internal': '#5D878F',   # Blue tone for internal components  
    'external': '#2E8B57',   # Green tone for external systems
    'social': '#D2BA4C'      # Orange tone for social elements
}

# Create edge traces
edge_traces = []
for edge in data['edges']:
    source_pos = positions[edge['source']]
    target_pos = positions[edge['target']]
    
    edge_trace = go.Scatter(
        x=[source_pos[0], target_pos[0], None],
        y=[source_pos[1], target_pos[1], None],
        mode='lines',
        line=dict(width=3, color='rgba(120, 120, 120, 0.7)'),
        hoverinfo='none',
        showlegend=False
    )
    edge_traces.append(edge_trace)

# Create node traces by group with better text handling
node_traces = []
for group in ['core', 'internal', 'external', 'social']:
    group_nodes = [n for n in data['nodes'] if n['group'] == group]
    
    if not group_nodes:
        continue
        
    x_vals = [positions[node['id']][0] for node in group_nodes]
    y_vals = [positions[node['id']][1] for node in group_nodes]
    sizes = [node['size'] for node in group_nodes]
    labels = [node['label'] for node in group_nodes]
    
    # Group names for legend
    group_names = {
        'core': 'Core Agent',
        'internal': 'Internal (Blue)', 
        'external': 'External (Green)',
        'social': 'Social (Orange)'
    }
    
    # Better text sizing and positioning
    text_size = 13 if group == 'core' else 11
    
    node_trace = go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=color_map[group],
            line=dict(width=4, color='white'),
            opacity=0.9
        ),
        text=labels,
        textposition="middle center",
        textfont=dict(size=text_size, color='white', family='Arial Black'),
        name=group_names[group],
        hovertemplate='%{text}<extra></extra>',
        showlegend=True
    )
    node_traces.append(node_trace)

# Create the figure
fig = go.Figure(data=edge_traces + node_traces)

fig.update_layout(
    title="AI Society Infrastructure Network",
    showlegend=True,
    hovermode='closest',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-6, 6]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-5, 5]),
    plot_bgcolor='white',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Save the chart
fig.write_image("ai_society_network.png")
fig.write_image("ai_society_network.svg", format="svg")

fig.show()