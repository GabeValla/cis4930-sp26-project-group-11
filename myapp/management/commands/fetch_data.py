from django.core.management.base import BaseCommand
from django.db import transaction
import requests
from myapp.models import City, WeatherRecord
import datetime

class Command(BaseCommand):
    help = 'Fetch latest data from the Open-Meteo API'

    def handle(self, *args, **options):
        cities = [
            ("Tallahassee", 30.4383, -84.2807),
            ("Miami", 25.7617, -80.1918),
            ("Orlando", 28.5383, -81.3792)
        ]

        for city_name, lat, lon in cities:
            self.stdout.write(f'Fetching data for {city_name}...')
            try:
                params = {
                    "latitude": lat,
                    "longitude": lon,
                    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,precipitation_probability_max",
                    "timezone": "auto"
                }
                resp = requests.get(
                    'https://api.open-meteo.com/v1/forecast',
                    params=params,
                    timeout=10
                )
                resp.raise_for_status()
                data = resp.json()

                city, _ = City.objects.get_or_create(name=city_name)
                
                dates = data.get("daily", {}).get("time", [])
                temp_max = data.get("daily", {}).get("temperature_2m_max", [])
                temp_min = data.get("daily", {}).get("temperature_2m_min", [])
                precipitation = data.get("daily", {}).get("precipitation_sum", [])
                wind_speed_max = data.get("daily", {}).get("wind_speed_10m_max", [])
                precip_prob_max = data.get("daily", {}).get("precipitation_probability_max", [])

                with transaction.atomic():
                    for i, date_str in enumerate(dates):
                        # Convert date string to python date object
                        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                        
                        WeatherRecord.objects.update_or_create(
                            city=city,
                            date=date_obj,
                            defaults={
                                'temp_max': temp_max[i] if temp_max and i < len(temp_max) else None,
                                'temp_min': temp_min[i] if temp_min and i < len(temp_min) else None,
                                'precipitation': precipitation[i] if precipitation and i < len(precipitation) else None,
                                'wind_speed_max': wind_speed_max[i] if wind_speed_max and i < len(wind_speed_max) else None,
                                'precip_prob_max': precip_prob_max[i] if precip_prob_max and i < len(precip_prob_max) else None,
                                'source': 'api'
                            }
                        )
                self.stdout.write(self.style.SUCCESS(f'Successfully fetched and saved {len(dates)} records for {city_name}'))
            except requests.exceptions.RequestException as e:
                self.stderr.write(f'Error fetching {city_name}: {e}')
