# COVID-19 Vaccination Explorer

A comprehensive interactive dashboard for visualizing and analyzing global COVID-19 vaccination data.

- **Deployed Project**: [Dashboard Preview](https://covid-vaccination-explorer-0yu1fvmc.preswald.app/)

## 📊 About the Project

This COVID-19 Vaccination Explorer provides an intuitive, single-page interface for exploring vaccination trends and statistics worldwide. Built with Preswald, it offers interactive visualizations and in-depth analysis tools to understand vaccination progress across different countries and regions.

## 🌍 Data Source

This application uses the **Our World in Data COVID-19 Vaccination Dataset**, which provides comprehensive, up-to-date vaccination data for countries around the world.

- **Source**: [Our World in Data COVID-19 Vaccination Dataset](https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations)
- **Dataset Features**: Country-level data on vaccination doses, population coverage percentages, daily rates, and vaccine types
- **Update Frequency**: The dataset is regularly updated, reflecting the latest available vaccination statistics

## ✨ Features

- **Interactive Global Map**: Color-coded choropleth visualization of vaccination rates worldwide
- **Country-Specific Analysis**: Detailed vaccination statistics and trends for individual countries
- **Comparative Analysis**: Tools to compare vaccination progress across different countries
- **Time-Based Visualization**: Track vaccination progress over customizable time periods
- **Correlation Analysis**: Explore relationships between population size and vaccination rates
- **Global Statistics**: Summary metrics for worldwide vaccination progress

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Preswald framework

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/covid-vaccination-explorer.git
   cd covid-vaccination-explorer
   ```

2. Install Preswald if you haven't already:
   ```bash
   pip install preswald
   ```

3. Download the dataset:
   ```bash
   mkdir -p data
   curl -o data/covid_vaccinations.csv https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv
   ```

4. Make sure your `preswald.toml` file is set up with the correct data source:
   ```toml
   [data.covid_vaccinations]
   type = "csv"
   path = "data/covid_vaccinations.csv"
   ```

### Running the App

Run the application locally with:

```bash
preswald run hello.py
```

This will start the Preswald server and open the application in your default web browser (typically at http://localhost:8501).

## 🌐 Deployment

### Local Network Deployment

To deploy the app so it's accessible on your local network:

```bash
preswald deploy hello.py --target local
```

### Cloud Deployment (Optional)

To deploy to a cloud provider:

1. Google Cloud Run:
   ```bash
   preswald deploy hello.py --target gcp
   ```

2. Structured Cloud (Preswald's managed service):
   ```bash
   preswald deploy hello.py --target structured
   ```

## 📝 Usage Guide

1. **Global Map**: The main map shows worldwide vaccination rates. Select different metrics using the dropdown above the map.

2. **Country Selection**: Click on a country in the map or use the dropdown to select a specific country for detailed analysis.

3. **Time Range**: Use the time period selector to view data over different time spans.

4. **Comparative Analysis**: The vaccination leaders section shows countries with the highest vaccination rates.

5. **Population Analysis**: The scatter plot at the bottom compares vaccination rates with population sizes.

## 📋 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Our World in Data](https://ourworldindata.org/) for providing the COVID-19 vaccination dataset
- [Preswald](https://github.com/shubhayan935/preswald) framework for interactive data visualization
- [Plotly](https://plotly.com/) for the underlying chart library