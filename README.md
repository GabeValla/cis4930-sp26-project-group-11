# TallyStats: Crime & Weather Analytics Dashboard

**Group 11**
* Gabriel Rivera
* Gabriel Valladares-Ruiz
* Olivia Anderson
* Liam Kandel

## Project Title & Real-World Context

**TallyStats: Crime and Weather Analytics**

This project integrates two disparate real-world datasets into a single, comprehensive public safety dashboard for the City of Tallahassee. By combining historical 911 dispatch records with live, ongoing weather tracking for major Florida cities, the application allows residents and city planners to visually survey incident hotspots, track types of crime, and explore potential correlations between changing weather conditions and public safety call volumes. The same TOPS dataset utilized in Project 1 serves as the backbone here, alongside the Open-Meteo API integrated during Project 2.

## Datasets and APIs Used
* **TOPS Crime Data (Project 1)**: [Tallahassee Online Police Statistics](https://www.talgov.com/gis/tops/)
* **Weather API (Project 2)**: [Open-Meteo Free API](https://open-meteo.com/en/docs)

## Application Features

The Django application implements the following pages and features:
- **Homepage (`/`)**: A dynamic entry page outlining project goals and displaying high-level statistical context.
- **Records List View (`/records/`)**: A paginated database of all individual 911 incidents within the city.
- **Record Detail View (`/records/<pk>/`)**: Specific time and location coordinates for an individual incident.
- **Record Create View (`/records/add/`)**: A validated Form interface to report a new incident to the database.
- **Record Update View (`/records/<pk>/edit/`)**: Interface to alter information about an existing record.
- **Record Delete View (`/records/<pk>/delete/`)**: A safety confirmation screen prior to permanent database record deletion.
- **Analytics Dashboard (`/analytics/`)**: Uses Chart.js to map both the most common incident types visually via a doughnut chart, and employs `leaflet.js` with `leaflet-heat` to dynamically map geographical incident coordinates across the city for a given month. It answers the initial Project 1 core research questions using Pandas aggregations.
- **Secure API Webhook (`/api/trigger-fetch/`)**: A hidden endpoint locked behind an environment variable validation token (`CRON_FETCH_TOKEN`). When pinged securely by an external cron service, it runs `fetch_data` autonomously in a background thread to continually bypass Render hibernation and sync fresh weather items.

## Render URL
https://cis4930-sp26-project-group-11.onrender.com/
