# Contribution.md

## CIS 4930 Spring 2026 Group 11

### Project: TallyStats: Crime & Weather Analytics Dashboard

---

## Team Members & Contributions

### Gabriel Rivera

- **Weather Page**: Built the weather page for the Django application
- **Data Analysis (Extra Credit)**: Created the `analysis.ipynb` Jupyter Notebook for exploratory data analysis. Loaded and cleaned `weather_data.csv` with pandas, generated matplotlib visualizations (Max Temperature Over Time, Daily Precipitation) per city
- **Weather Data Pipeline (with Liam Kandel)**: Collaborated on extending the pipeline from 3 to 5 weather metrics by adding `wind_speed_10m_max` and `precipitation_probability_max` to the API client and pipeline
- **README & Documentation**: Co-authored README sections including project context, API documentation, data analysis writeup, and embedded graph images
- **Figures**: Generated and added chart PNGs (`max_temp_over_time.png`, `daily_precipitation.png`) to the repository

### Liam Kandel

- **Weather Data Pipeline (with Gabriel Rivera)**: Collaborated on extending the Open-Meteo API integration and data pipeline, adding max wind speed and precipitation probability metrics
- **Git Workflow & Version Control**: Managed commits, branching (`extra-credit` branch), and pull request merges on behalf of the pair
- **README & Documentation**: Co-authored README content including run instructions and project documentation
- **Notebook Updates**: Updated `analysis.ipynb` with saved execution outputs and kernel/venv configuration

### Gabriel Valladares-Ruiz

- **Django Application**: Developed the core Django project structure (`myapp/`, `manage.py`, settings, URL routing)
- **Crime Data Integration (Project 1)**: Integrated the TOPS 911 dispatch dataset into the application database
- **CRUD Views**: Implemented Records List, Detail, Create, Update, and Delete views
- **Deployment**: Configured Render deployment (`Procfile`, `build.sh`, `runtime.txt`, `requirements.txt`)

### Olivia Anderson

- **Analytics Dashboard**: Built the `/analytics/` page with Chart.js doughnut chart for incident types and Leaflet.js heatmap for geographic incident mapping
- **Homepage**: Developed the dynamic homepage with project goals and high-level statistics
- **HTML Templates**: Created and styled the Django templates
- **API Webhook**: Implemented the secure `/api/trigger-fetch/` endpoint for automated weather data syncing

---

## Notes

- Gabriel Rivera and Liam Kandel collaborated closely on the weather data pipeline and extra credit work. Liam handled the Git commits for their shared contributions, which is why the commit history reflects a single committer for jointly authored work.
- Gabriel Valladares-Ruiz and Olivia Anderson focused on the Django application, crime data integration, analytics dashboard, and deployment infrastructure.
