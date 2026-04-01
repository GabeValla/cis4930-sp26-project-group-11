from src.api_client import fetch_weather
from src.storage import save_to_csv
import pandas as pd

def main():
    # Define cities with their latitude and longitude
    cities = [
        ("Tallahassee", 30.4383, -84.2807),
        ("Miami", 25.7617, -80.1918),
        ("Orlando", 28.5383, -81.3792)
    ]

    all_rows = []

    # Fetch weather data for each city and prepare rows for the DataFrame
    for city_name, lat, lon in cities:
        print(f"Fetching data for {city_name}...")
        result = fetch_weather(city_name, lat, lon)

        # If the API call was successful, process the data
        if result:
            dates = result["dates"]
            temp_max = result["temp_max"]
            temp_min = result["temp_min"]
            precipitation = result["precipitation"]
            wind_speed_max = result["wind_speed_max"]
            precip_prob_max = result["precip_prob_max"]

            # Create a row for each date in the API response
            for i in range(len(dates)):
                row = {
                    "city": city_name,
                    "date": dates[i],
                    "temp_max": temp_max[i],
                    "temp_min": temp_min[i],
                    "precipitation": precipitation[i],
                    "wind_speed_max": wind_speed_max[i],
                    "precip_prob_max": precip_prob_max[i]
                }
                all_rows.append(row)

    # Convert the list of rows into a DataFrame
    df = pd.DataFrame(all_rows)

    # Save the DataFrame to a CSV file
    output_path = "data/processed/weather_data.csv"
    save_to_csv(df, output_path)

    # Print summary of the pipeline execution
    print(f"\nPipeline complete. {len(df)} rows processed.")

if __name__ == "__main__":
    main()