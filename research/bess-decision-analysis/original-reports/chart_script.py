
import plotly.graph_objects as go
import pandas as pd

# Data
data = [
  {"Scenario": "With BESS (100 kWh)", "Component": "Initial CapEx", "Cost": 50000},
  {"Scenario": "With BESS (100 kWh)", "Component": "Operating Costs (10yr)", "Cost": 70000},
  {"Scenario": "With BESS (100 kWh)", "Component": "Battery Replacement", "Cost": 25000},
  {"Scenario": "Without BESS", "Component": "Engineering Development", "Cost": 100000},
  {"Scenario": "Without BESS", "Component": "Testing/Validation", "Cost": 25000},
  {"Scenario": "Without BESS", "Component": "Annual Risk Costs (10yr)", "Cost": 80000},
  {"Scenario": "Without BESS", "Component": "Operational Overhead (10yr)", "Cost": 35000}
]

df = pd.DataFrame(data)

# Calculate totals for each scenario
totals = df.groupby('Scenario')['Cost'].sum()

# Get unique scenarios and components
scenarios = ["With BESS (100 kWh)", "Without BESS"]

# Brand colors
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C', '#B4413C', '#964325']

# Create figure
fig = go.Figure()

# Get components for each scenario
with_bess_data = df[df['Scenario'] == "With BESS (100 kWh)"]
without_bess_data = df[df['Scenario'] == "Without BESS"]

# Add traces for With BESS components
for idx, row in with_bess_data.iterrows():
    fig.add_trace(go.Bar(
        name=row['Component'],
        x=["With BESS"],
        y=[row['Cost']],
        marker_color=colors[idx % len(colors)],
        hovertemplate='%{y:$,.0f}<extra></extra>',
        showlegend=True
    ))

# Add traces for Without BESS components
for idx, row in without_bess_data.iterrows():
    fig.add_trace(go.Bar(
        name=row['Component'],
        x=["Without BESS"],
        y=[row['Cost']],
        marker_color=colors[idx % len(colors)],
        hovertemplate='%{y:$,.0f}<extra></extra>',
        showlegend=True
    ))

# Update layout for stacked bars
fig.update_layout(
    barmode='stack',
    title='10-Year TCO Comparison',
    xaxis_title='Scenario',
    yaxis_title='Cost ($)',
    showlegend=True
)

# Add total annotations at the top of each bar
fig.add_annotation(
    x="With BESS",
    y=totals["With BESS (100 kWh)"],
    text="$145k",
    showarrow=False,
    yshift=10,
    font=dict(size=14, color='black')
)

fig.add_annotation(
    x="Without BESS",
    y=totals["Without BESS"],
    text="$240k",
    showarrow=False,
    yshift=10,
    font=dict(size=14, color='black')
)

# Format y-axis
fig.update_yaxes(tickformat='$,.0f')
fig.update_traces(cliponaxis=False)

# Save the chart
fig.write_image('tco_comparison.png')
fig.write_image('tco_comparison.svg', format='svg')
