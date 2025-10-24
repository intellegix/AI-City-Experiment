import plotly.graph_objects as go
import json

# Load the data
data = {
  "phases": [
    {
      "phase": "Phase 1: Initialization",
      "duration": "Day 0",
      "activities": ["Load 1000 citizen profiles", "Initialize memory systems", "Establish baseline"]
    },
    {
      "phase": "Phase 2: Stabilization",
      "duration": "Days 1-30",
      "activities": ["Agents explore environment", "Form initial relationships", "Establish routines"]
    },
    {
      "phase": "Phase 3: Emergence",
      "duration": "Days 31-180",
      "activities": ["Social structures form", "Norms emerge", "Economic patterns develop"]
    },
    {
      "phase": "Phase 4: Maturation",
      "duration": "Days 181-365",
      "activities": ["Society functions", "Complex interactions", "Innovation & adaptation"]
    },
    {
      "phase": "Phase 5: Analysis",
      "duration": "Post-simulation",
      "activities": ["Data analysis", "Compare to human society", "Extract insights"]
    }
  ]
}

# Create figure
fig = go.Figure()

# Colors gradient from blue to green
colors = ['#4A90E2', '#5BA3F5', '#1FB8CD', '#2E8B57', '#228B22']

# Box dimensions and positions - larger boxes for better readability
box_width = 5
box_height = 2.2
start_y = 9
y_spacing = 3.5

# Create boxes and text for each phase
for i, phase_data in enumerate(data['phases']):
    y_pos = start_y - (i * y_spacing)
    
    # Create box
    fig.add_shape(
        type="rect",
        x0=-box_width/2, y0=y_pos - box_height/2,
        x1=box_width/2, y1=y_pos + box_height/2,
        fillcolor=colors[i],
        line=dict(color="black", width=2),
        opacity=0.9
    )
    
    # Add phase title
    fig.add_annotation(
        x=0, y=y_pos + 0.6,
        text=f"<b>{phase_data['phase']}</b>",
        showarrow=False,
        font=dict(size=16, color="white"),
        align="center"
    )
    
    # Add duration
    fig.add_annotation(
        x=0, y=y_pos + 0.2,
        text=phase_data['duration'],
        showarrow=False,
        font=dict(size=14, color="white"),
        align="center"
    )
    
    # Add activities with better spacing
    activities_text = "• " + "<br>• ".join(phase_data['activities'])
    fig.add_annotation(
        x=0, y=y_pos - 0.4,
        text=activities_text,
        showarrow=False,
        font=dict(size=12, color="white"),
        align="center"
    )
    
    # Add arrow to next phase (except for last phase)
    if i < len(data['phases']) - 1:
        arrow_y_start = y_pos - box_height/2
        arrow_y_end = y_pos - y_spacing + box_height/2
        
        fig.add_annotation(
            x=0, y=(arrow_y_start + arrow_y_end) / 2,
            ax=0, ay=arrow_y_start - 0.2,
            arrowhead=2,
            arrowsize=2,
            arrowwidth=4,
            arrowcolor="black",
            showarrow=True,
            text=""
        )

# Update layout with better spacing
fig.update_layout(
    title="AI Society Experiment Phases",
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-3, 3]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-7, 11]
    ),
    plot_bgcolor="white",
    font=dict(family="Arial, sans-serif")
)

# Save the chart
fig.write_image("ai_society_experiment_phases.png")
fig.write_image("ai_society_experiment_phases.svg", format="svg")
print("Improved flowchart saved successfully!")