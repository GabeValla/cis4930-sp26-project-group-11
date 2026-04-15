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
- **Analytics Dashboard (`/analytics/`)**: Uses Chart.js to map both the most common incident types visually via a pie chart, and the frequency of calls over time chronologically via a line trend. It answers the initial Project 1 core research questions using Pandas aggregations.

## Setup Instructions

Ensure your machine has Python 3.9+ installed. Follow these steps sequentially to setup and run the application locally.

1. **Clone the Repository:**
```bash
git clone https://github.com/YourGitHubUsername/cis4930-sp26-django-project-group-XX.git
cd cis4930-sp26-django-project-group-XX
```

2. **Set up a Virtual Environment & Install Dependencies:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure Environment Variables:**
Copy the example environment securely.
```bash
cp .env.example .env
```
> *Note: By default, Django will load `.env` variables via `python-decouple`. Populate `SECRET_KEY` and set `DEBUG=True` for normal usage.*

4. **Apply Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Seed the Local Database:**
This retrieves exactly 10,000 rows from the 160K+ local processed file to ensure fast functionality. You can optionally modify `--limit 10000` to inject more or less.
```bash
python manage.py seed_data --limit 10000
python manage.py fetch_data
```

6. **Run the Application Locally:**
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your web browser.

---

## Output of `manage.py check --deploy`

```text
(venv) $ export DJANGO_SETTINGS_MODULE=config.settings.prod 
(venv) $ export SECRET_KEY="long-random-secret-key-1234567890-qwertyuiop-asdfghjkl"
(venv) $ python3 manage.py check --deploy

System check identified no issues (0 silenced).
```

---

## Screenshots

*(See artifacts folder dynamically attached to this repository for visual examples of our homepage, list view, and analytics dashboard running live).*
