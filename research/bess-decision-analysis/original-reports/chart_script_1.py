import plotly.graph_objects as go

# Create figure
fig = go.Figure()

# Define node positions (x, y)
positions = {
    'start': (0.5, 1.0),
    'q1': (0.5, 0.85),
    'deploy1': (0.15, 0.70),
    'q2': (0.5, 0.70),
    'deploy2': (0.15, 0.55),
    'q3': (0.5, 0.55),
    'deploy3': (0.15, 0.40),
    'q4': (0.5, 0.40),
    'no_bess1': (0.15, 0.25),
    'q5': (0.5, 0.25),
    'no_bess2': (0.25, 0.10),
    'deploy4': (0.75, 0.10)
}

# Define shapes and annotations
shapes = []
annotations = []

# Start node (rounded rectangle)
shapes.append(dict(type="rect", x0=0.42, y0=0.97, x1=0.58, y1=1.03,
                   fillcolor="#B3E5EC", line=dict(color="#21808d", width=2),
                   layer="below"))
annotations.append(dict(x=0.5, y=1.0, text="BESS Decision", showarrow=False,
                       font=dict(size=12, color="#13343b"), xanchor="center"))

# Decision nodes (diamonds approximated with rotated squares)
decision_nodes = [
    (0.5, 0.85, "Regulatory<br>Requirement?"),
    (0.5, 0.70, "In-house Gen.<br>Control Exp.?"),
    (0.5, 0.55, "Risk<br>Tolerance?"),
    (0.5, 0.40, "Budget<br>Constraints<br>Severe?"),
    (0.5, 0.25, "Deployment<br>Duration?")
]

for x, y, label in decision_nodes:
    shapes.append(dict(type="rect", x0=x-0.08, y0=y-0.05, x1=x+0.08, y1=y+0.05,
                       fillcolor="#FFEB8A", line=dict(color="#21808d", width=2),
                       layer="below"))
    annotations.append(dict(x=x, y=y, text=label, showarrow=False,
                           font=dict(size=10, color="#13343b"), xanchor="center"))

# Deploy BESS nodes (rounded rectangles)
deploy_nodes = [
    (0.15, 0.70, "Deploy BESS"),
    (0.15, 0.55, "Deploy BESS"),
    (0.15, 0.40, "Deploy BESS"),
    (0.75, 0.10, "Deploy BESS<br>(Recommended)")
]

for x, y, label in deploy_nodes:
    shapes.append(dict(type="rect", x0=x-0.06, y0=y-0.03, x1=x+0.06, y1=y+0.03,
                       fillcolor="#A5D6A7", line=dict(color="#21808d", width=2),
                       layer="below"))
    annotations.append(dict(x=x, y=y, text=label, showarrow=False,
                           font=dict(size=10, color="#13343b"), xanchor="center"))

# No BESS nodes
no_bess_nodes = [
    (0.15, 0.25, "No BESS"),
    (0.25, 0.10, "No BESS")
]

for x, y, label in no_bess_nodes:
    shapes.append(dict(type="rect", x0=x-0.06, y0=y-0.03, x1=x+0.06, y1=y+0.03,
                       fillcolor="#FFCDD2", line=dict(color="#21808d", width=2),
                       layer="below"))
    annotations.append(dict(x=x, y=y, text=label, showarrow=False,
                           font=dict(size=10, color="#13343b"), xanchor="center"))

# Add arrows and edge labels
arrows = [
    # Start to Q1
    (0.5, 0.97, 0.5, 0.90, ""),
    # Q1 to Deploy1 (Yes)
    (0.42, 0.85, 0.21, 0.70, "Yes"),
    # Q1 to Q2 (No)
    (0.5, 0.80, 0.5, 0.75, "No"),
    # Q2 to Deploy2 (No)
    (0.42, 0.70, 0.21, 0.55, "No"),
    # Q2 to Q3 (Yes)
    (0.5, 0.65, 0.5, 0.60, "Yes"),
    # Q3 to Deploy3 (Low)
    (0.42, 0.55, 0.21, 0.40, "Low"),
    # Q3 to Q4 (High)
    (0.5, 0.50, 0.5, 0.45, "High"),
    # Q4 to No BESS1 (Yes <$100K)
    (0.42, 0.40, 0.21, 0.25, "Yes <$100K"),
    # Q4 to Q5 (No)
    (0.5, 0.35, 0.5, 0.30, "No"),
    # Q5 to No BESS2 (Temp. <1yr)
    (0.42, 0.25, 0.31, 0.10, "Temp.<1yr"),
    # Q5 to Deploy4 (Long-term)
    (0.58, 0.25, 0.69, 0.10, "Long-term")
]

for x0, y0, x1, y1, label in arrows:
    fig.add_annotation(
        x=x1, y=y1, ax=x0, ay=y0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#21808d"
    )
    if label:
        mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
        annotations.append(dict(
            x=mid_x, y=mid_y, text=label,
            showarrow=False,
            font=dict(size=9, color="#13343b"),
            bgcolor="#F3F3EE",
            xanchor="center"
        ))

# Update layout
fig.update_layout(
    title="BESS Deployment Decision Tree",
    shapes=shapes,
    annotations=annotations,
    xaxis=dict(range=[0, 1], showgrid=False, zeroline=False, visible=False),
    yaxis=dict(range=[0, 1.1], showgrid=False, zeroline=False, visible=False),
    plot_bgcolor="#F3F3EE",
    paper_bgcolor="#F3F3EE",
    showlegend=False
)

# Save the figure
fig.write_image('bess_flowchart.png')
fig.write_image('bess_flowchart.svg', format='svg')
