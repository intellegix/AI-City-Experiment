import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Create a comprehensive architecture diagram using Plotly
fig = go.Figure()

# Define positions for different components
# Orchestrator at the top
orchestrator_x, orchestrator_y = 0.5, 0.9

# Specialized agents in parallel below orchestrator
agents_y = 0.75
fe_x, be_x, po_x, ap_x = 0.15, 0.35, 0.65, 0.85

# Memory systems below agents
memory_y = 0.55
stm_x, wm_x, ltm_x = 0.25, 0.5, 0.75

# Tool integrations on the right
tool_y_base = 0.7
ti_x = 0.95
mcp_x, fc_x, va_x = 0.95, 0.95, 0.95
mcp_y, fc_y, va_y = 0.6, 0.5, 0.4

# Communication patterns on the left
comm_y_base = 0.7
cp_x = 0.05
ed_x, pl_x, ow_x = 0.05, 0.05, 0.05
ed_y, pl_y, ow_y = 0.6, 0.5, 0.4

# UI Performance at the bottom
perf_y_base = 0.25
upa_x = 0.5
rl_x, mm_x, es_x, uc_x = 0.2, 0.4, 0.6, 0.8
rl_y, mm_y, es_y, uc_y = 0.15, 0.15, 0.15, 0.15

# Colors based on instructions
blue = '#4A90E2'  # Orchestrator
green = '#7ED321'  # Specialized Agents
purple = '#9013FE'  # Memory Systems
orange = '#FF9500'  # Tool Integrations
cyan = '#1FB8CD'  # Communication Patterns
red = '#DB4545'  # Performance Architecture

# Add rectangles for each component
components = [
    # Orchestrator
    {'x': orchestrator_x, 'y': orchestrator_y, 'text': 'Orchestrator Agent<br>Claude Opus 4', 'color': blue, 'width': 0.15, 'height': 0.08},
    
    # Specialized Agents
    {'x': fe_x, 'y': agents_y, 'text': 'Frontend/UI<br>Sonnet 4', 'color': green, 'width': 0.12, 'height': 0.06},
    {'x': be_x, 'y': agents_y, 'text': 'Backend/API<br>Sonnet 4', 'color': green, 'width': 0.12, 'height': 0.06},
    {'x': po_x, 'y': agents_y, 'text': 'Performance Opt<br>Sonnet 4', 'color': green, 'width': 0.12, 'height': 0.06},
    {'x': ap_x, 'y': agents_y, 'text': 'Architecture Plan<br>Sonnet 4', 'color': green, 'width': 0.12, 'height': 0.06},
    
    # Memory Systems
    {'x': stm_x, 'y': memory_y, 'text': 'Short-term Memory<br>Context Window', 'color': purple, 'width': 0.12, 'height': 0.06},
    {'x': wm_x, 'y': memory_y, 'text': 'Working Memory<br>Shared State', 'color': purple, 'width': 0.12, 'height': 0.06},
    {'x': ltm_x, 'y': memory_y, 'text': 'Long-term Memory<br>Vector Store', 'color': purple, 'width': 0.12, 'height': 0.06},
    
    # Tool Integrations
    {'x': ti_x, 'y': tool_y_base, 'text': 'Tool Integrations', 'color': orange, 'width': 0.1, 'height': 0.05},
    {'x': mcp_x, 'y': mcp_y, 'text': 'MCP Servers', 'color': orange, 'width': 0.08, 'height': 0.04},
    {'x': fc_x, 'y': fc_y, 'text': 'Function Calling', 'color': orange, 'width': 0.08, 'height': 0.04},
    {'x': va_x, 'y': va_y, 'text': 'Vision API', 'color': orange, 'width': 0.08, 'height': 0.04},
    
    # Communication Patterns
    {'x': cp_x, 'y': comm_y_base, 'text': 'Communication<br>Patterns', 'color': cyan, 'width': 0.1, 'height': 0.05},
    {'x': ed_x, 'y': ed_y, 'text': 'Event-Driven', 'color': cyan, 'width': 0.08, 'height': 0.04},
    {'x': pl_x, 'y': pl_y, 'text': 'Pipeline', 'color': cyan, 'width': 0.08, 'height': 0.04},
    {'x': ow_x, 'y': ow_y, 'text': 'Orchestrator-Worker', 'color': cyan, 'width': 0.08, 'height': 0.04},
    
    # UI Performance Architecture
    {'x': upa_x, 'y': perf_y_base, 'text': 'UI Performance<br>Architecture', 'color': red, 'width': 0.15, 'height': 0.06},
    {'x': rl_x, 'y': rl_y, 'text': 'Rendering Layer', 'color': red, 'width': 0.1, 'height': 0.04},
    {'x': mm_x, 'y': mm_y, 'text': 'Memory Mgmt', 'color': red, 'width': 0.1, 'height': 0.04},
    {'x': es_x, 'y': es_y, 'text': 'Event System', 'color': red, 'width': 0.1, 'height': 0.04},
    {'x': uc_x, 'y': uc_y, 'text': 'Update Cycles', 'color': red, 'width': 0.1, 'height': 0.04},
]

# Add rectangles and text for each component
for comp in components:
    # Add rectangle
    fig.add_shape(
        type="rect",
        x0=comp['x'] - comp['width']/2,
        y0=comp['y'] - comp['height']/2,
        x1=comp['x'] + comp['width']/2,
        y1=comp['y'] + comp['height']/2,
        fillcolor=comp['color'],
        line=dict(color="white", width=2),
        opacity=0.8
    )
    
    # Add text
    fig.add_annotation(
        x=comp['x'],
        y=comp['y'],
        text=comp['text'],
        showarrow=False,
        font=dict(color="white", size=10, family="Arial Black"),
        align="center"
    )

# Define connections
connections = [
    # Orchestrator to agents (bidirectional)
    (orchestrator_x, orchestrator_y, fe_x, agents_y),
    (orchestrator_x, orchestrator_y, be_x, agents_y),
    (orchestrator_x, orchestrator_y, po_x, agents_y),
    (orchestrator_x, orchestrator_y, ap_x, agents_y),
    
    # Agents to memory
    (fe_x, agents_y, stm_x, memory_y),
    (be_x, agents_y, stm_x, memory_y),
    (po_x, agents_y, wm_x, memory_y),
    (ap_x, agents_y, ltm_x, memory_y),
    
    # Memory flow
    (stm_x, memory_y, wm_x, memory_y),
    (wm_x, memory_y, ltm_x, memory_y),
    
    # Tool integrations
    (ti_x, tool_y_base, mcp_x, mcp_y),
    (ti_x, tool_y_base, fc_x, fc_y),
    (ti_x, tool_y_base, va_x, va_y),
    
    # Communication patterns
    (cp_x, comm_y_base, ed_x, ed_y),
    (cp_x, comm_y_base, pl_x, pl_y),
    (cp_x, comm_y_base, ow_x, ow_y),
    
    # UI Performance
    (upa_x, perf_y_base, rl_x, rl_y),
    (upa_x, perf_y_base, mm_x, mm_y),
    (upa_x, perf_y_base, es_x, es_y),
    (upa_x, perf_y_base, uc_x, uc_y),
    
    # Cross connections
    (orchestrator_x, orchestrator_y, ti_x, tool_y_base),
    (orchestrator_x, orchestrator_y, cp_x, comm_y_base),
    (fe_x, agents_y, upa_x, perf_y_base),
    (po_x, agents_y, upa_x, perf_y_base),
    (wm_x, memory_y, ti_x, tool_y_base),
    (cp_x, comm_y_base, orchestrator_x, orchestrator_y),
]

# Add arrows for connections
for x1, y1, x2, y2 in connections:
    fig.add_annotation(
        x=x2, y=y2,
        ax=x1, ay=y1,
        xref="x", yref="y",
        axref="x", ayref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="gray",
        opacity=0.7
    )

# Configure layout
fig.update_layout(
    title="Claude Multimodal Agent Structure",
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-0.05, 1.05]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[0, 1]
    ),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# Save as PNG and SVG
fig.write_image("claude_agent_architecture.png")
fig.write_image("claude_agent_architecture.svg", format="svg")

print("Architecture diagram saved successfully as PNG and SVG")