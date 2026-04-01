# Automated Weather Data Pipeline
Group 11

### Group Members
- Liam Kandel
- Gabe Valla
- Olivia Anderson
- Gabe Rivera

## Real-World Context
This project implements an automated Python pipeline to track daily weather forecasts for three major Florida cities: Tallahassee, Miami, and Orlando. By continually pulling and aggregating max/min temperatures, precipitation totals, maximum wind speeds, and peak precipitation probabilities, we can build a historical dataset useful for local planning, event scheduling, and analyzing seasonal weather trends.

## API Documentation
This project uses the free, no-authentication **Open-Meteo API**:
- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)
- **Constraints/Why we chose it**: Open-Meteo is highly reliable, does not require API keys or auth tokens, and allows us to test easily without worrying about daily quota limits on a free tier. We rely on their `daily` forecast endpoint to grab the specific 5 physical measurements we need.

## Data Pipeline Goals
1. **Fetch daily weather metrics** for multiple cities (Tallahassee, Miami, Orlando) in a single run.
2. **Handle network failures gracefully** through robust `try/except` blocks and timeout configurations.
3. **Parse and extract 5 meaningful fields** (max temp, min temp, precipitation sum, max wind speed, max precipitation probability) from the nested JSON response.
4. **Persist the data** into a single structured CSV file (`data/processed/weather_data.csv`), ensuring new pipeline runs cleanly append data without silently overwriting historical records.

## Example Run
To execute the data pipeline, run the following command from the root of the project:

```bash
python -m src.pipeline
```

**Example Console Output:**
```text
Fetching data for Tallahassee...
Fetching data for Miami...
Fetching data for Orlando...
Saved data to data/processed/weather_data.csv

Pipeline complete. 21 rows processed.
```

## Data Analysis (Extra Credit)
To satisfy the optional stretch goal, we included a Jupyter Notebook (`analysis.ipynb`) that runs an Exploratory Data Analysis (EDA) on the `weather_data.csv` file. 
The notebook:
- Checks out the dataset using `pandas`.
- Drops duplicates that inherently appear when re-running the automated pipeline to ensure data integrity during graphing.
- Generates a chronological line graph tracking the **Maximum Temperature Over Time** for the 3 Florida cities.
- Generates a dashed chronological line graph mapping out **Daily Precipitation**.

## Automation Hook
To schedule this pipeline to run automatically every day at 8:00 AM, you could add the following cron job to your system (macOS/Linux):

```bash
# Run the pipeline every day at 8:00 AM
0 8 * * * cd /path/to/automated-data-pipeline && /usr/bin/python3 -m src.pipeline >> data/processed/pipeline.log 2>&1
```
