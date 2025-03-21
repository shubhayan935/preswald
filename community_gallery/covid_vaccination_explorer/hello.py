from preswald import text, table, plotly, connect, get_df, selectbox, slider, checkbox, separator
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# Connect to data
connect()
df = get_df('covid_vaccinations')

# Data preprocessing
df['date'] = pd.to_datetime(df['date'])
# Replace NaN values in important columns with 0
df['total_vaccinations'] = df['total_vaccinations'].fillna(0)
df['people_vaccinated'] = df['people_vaccinated'].fillna(0)
df['people_fully_vaccinated'] = df['people_fully_vaccinated'].fillna(0)

# Get the most recent date for each country
latest_by_country = df.sort_values('date').groupby('location').tail(1)
latest_by_country = latest_by_country.sort_values('people_fully_vaccinated', ascending=False)

# Identify continent data - create this column manually since it doesn't exist
continent_list = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania', 'World']
# Create these as new columns
df['is_continent'] = df['location'].isin(continent_list)
df['is_world'] = df['location'] == 'World'
latest_by_country['is_continent'] = latest_by_country['location'].isin(continent_list)
latest_by_country['is_world'] = latest_by_country['location'] == 'World'

# Title and Introduction
text("# 🌍 COVID-19 Vaccination Explorer Dashboard")

# Instead of divs with inline styles (which might not be supported),
# use Preswald's natural layout capabilities with components with size parameters

# Start main content
separator()

# --------------------------------
# SECTION 1: World Map (Main Element)
# --------------------------------
text("## 🗺️ Global Vaccination Map - Hover over each country to view data", size=1.0)

# Prepare data for the map
map_data = latest_by_country.copy()
selected_metric = selectbox(
    "Select map metric:", 
    [
        "people_fully_vaccinated_per_hundred",
        "people_vaccinated_per_hundred",
        "total_vaccinations_per_hundred"
    ],
    default="people_fully_vaccinated_per_hundred"
)

# Create readable metric names
metric_names = {
    "people_fully_vaccinated_per_hundred": "% Fully Vaccinated",
    "people_vaccinated_per_hundred": "% With At Least One Dose",
    "total_vaccinations_per_hundred": "Total Doses per 100 People"
}

# Filter out rows with missing iso_code values
map_data = map_data.dropna(subset=['iso_code'])

# Prepare hover data dictionary with only available columns
hover_data = {"iso_code": False}
if selected_metric in map_data.columns:
    hover_data[selected_metric] = True
if "people_vaccinated_per_hundred" in map_data.columns:
    hover_data["people_vaccinated_per_hundred"] = True
if "people_fully_vaccinated_per_hundred" in map_data.columns:
    hover_data["people_fully_vaccinated_per_hundred"] = True
if "date" in map_data.columns:
    hover_data["date"] = True

# Prepare labels dictionary
labels = {
    "date": "Last Updated"
}
for metric in metric_names:
    if metric in map_data.columns:
      labels[metric] = metric_names.get(metric, metric)

# Create the choropleth map
try:
    fig_map = px.choropleth(
        map_data, 
        locations="iso_code",
        color=selected_metric,
        hover_name="location",
        hover_data=hover_data,
        color_continuous_scale="Viridis",
        labels=labels,
        projection="natural earth"
    )
except Exception as e:
    # Fallback to a simple world map if choropleth fails
    text(f"Error creating map: {str(e)}")
    fig_map = go.Figure(go.Choropleth(
        locations=["USA", "CAN", "MEX"],  # Minimal fallback data
        z=[0, 0, 0],
        colorscale="Viridis",
        showscale=False
    ))
    fig_map.update_layout(title="Map could not be generated with the current data")

# Improve the map layout
fig_map.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    coloraxis_colorbar={
        'title': metric_names.get(selected_metric, selected_metric)
    },
    height=500,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular'
    )
)

# Add map click events through custom data
fig_map.update_traces(
    customdata=map_data[["location", "people_fully_vaccinated_per_hundred", "people_vaccinated_per_hundred"]]
)

plotly(fig_map)

# Detail view for clicked country (initially hidden)
country_view_div_id = "country-detail-view"

# --------------------------------
# SECTION 2: Top Stats Cards
# --------------------------------
text("## 📊 Global Statistics", size=1.0)
separator()

# Get world data for summary stats
world_data = latest_by_country[latest_by_country['location'] == 'World']
if not world_data.empty:
    world_latest = world_data.iloc[0]
    
    # Create a stats table instead of styled divs
    stat_rows = []
    
    # Total Global Doses
    if 'total_vaccinations' in world_latest and pd.notna(world_latest['total_vaccinations']):
        stat_rows.append({
            "Metric": "Total Vaccine Doses Globally",
            "Value": f"{world_latest['total_vaccinations']:,.0f}"
        })
    
    # People with at least one dose
    if 'people_vaccinated' in world_latest and pd.notna(world_latest['people_vaccinated']):
        stat_rows.append({
            "Metric": "People With At Least One Dose",
            "Value": f"{world_latest['people_vaccinated']:,.0f}"
        })
    
    # People fully vaccinated
    if 'people_fully_vaccinated' in world_latest and pd.notna(world_latest['people_fully_vaccinated']):
        stat_rows.append({
            "Metric": "People Fully Vaccinated",
            "Value": f"{world_latest['people_fully_vaccinated']:,.0f}"
        })
    
    # % of World Population Fully Vaccinated
    if 'people_fully_vaccinated_per_hundred' in world_latest and pd.notna(world_latest['people_fully_vaccinated_per_hundred']):
        stat_rows.append({
            "Metric": "% of World Population Fully Vaccinated",
            "Value": f"{world_latest['people_fully_vaccinated_per_hundred']:.2f}%"
        })
    
    # Display stats as a table
    if stat_rows:
        table(pd.DataFrame(stat_rows), title="Global Vaccination Statistics")

# --------------------------------
# SECTION 3: Country Comparison Chart
# --------------------------------
separator()
text("## 📊 Vaccination Leaders", size=0.5)

# Get top countries by fully vaccinated rate
top_n = slider("Number of countries to display:", min_val=5, max_val=15, default=10, step=5)

# Get data for comparison - filter out continents
comparison_data = latest_by_country[~latest_by_country['is_continent']].dropna(subset=['people_fully_vaccinated_per_hundred']).head(top_n)

if not comparison_data.empty:
    # Create horizontal bar chart
    fig_comparison = px.bar(
        comparison_data, 
        y='location', 
        x='people_fully_vaccinated_per_hundred',
        title='Countries with Highest Vaccination Rates',
        labels={
            'people_fully_vaccinated_per_hundred': '% of Population Fully Vaccinated',
            'location': 'Country'
        },
        orientation='h',
        color='people_fully_vaccinated_per_hundred',
        color_continuous_scale='Viridis',
        text='people_fully_vaccinated_per_hundred'
    )
    
    fig_comparison.update_traces(
        texttemplate='%{text:.1f}%', 
        textposition='outside'
    )
    
    fig_comparison.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title='% Fully Vaccinated',
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        coloraxis_showscale=False
    )
    
    plotly(fig_comparison)
# --------------------------------

# Footer
text("""
---
**Data Source:** [Our World in Data](https://ourworldindata.org/covid-vaccinations) | Last updated with the dates shown for each country
""")