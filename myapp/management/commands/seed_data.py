import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from myapp.models import City, CrimeIncident

class Command(BaseCommand):
    help = 'Seed crime data from TOPS CSV into the database'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=10000, help='Limit number of rows to insert')

    def handle(self, *args, **options):
        limit = options['limit']
        file_path = 'data/raw/tops_crime_data_cleaned.csv'
        
        self.stdout.write(f'Reading CSV from {file_path}...')
        try:
            df = pd.read_csv(file_path)
            # Sample uniformly from the entire dataset so we get a good distribution of months
            if limit > 0 and len(df) > limit:
                df = df.sample(n=limit, random_state=42)
        except Exception as e:
            self.stderr.write(f'Error reading CSV: {e}')
            return
            
        # Ensure 'Tallahassee' City exists
        city, _ = City.objects.get_or_create(name='Tallahassee')

        # Clear existing to prevent duplicates if desired, or skip. 
        # The prompt says 'bulk insert', we'll just wipe CrimeIncident for this city 
        # to make it idempotent, or we can just append, but P1 is static data.
        self.stdout.write('Clearing existing crime data for Tallahassee to prevent duplicates...')
        CrimeIncident.objects.filter(city=city).delete()

        incidents_to_create = []

        self.stdout.write(f'Processing {len(df)} rows...')
        for _, row in df.iterrows():
            # CSV columns: CREATE_TIME_INCIDENT,DISPO_TEXT,LOCATION_TEXT,Latitude,Longitude
            date_time_val = row.get('CREATE_TIME_INCIDENT')
            reason_val = row.get('DISPO_TEXT')
            location_val = row.get('LOCATION_TEXT')
            lat_val = row.get('Latitude')
            lon_val = row.get('Longitude')

            # Handle NaN values
            if pd.isna(location_val):
                location_val = ''
            if pd.isna(lat_val):
                lat_val = None
            if pd.isna(lon_val):
                lon_val = None
                
            if not date_time_val or pd.isna(date_time_val):
                continue
                
            incidents_to_create.append(
                CrimeIncident(
                    city=city,
                    date_time=date_time_val,
                    reason=str(reason_val)[:200],  # truncate if needed
                    location=str(location_val)[:255] if location_val else '',
                    latitude=lat_val,
                    longitude=lon_val
                )
            )

        self.stdout.write('Bulk inserting incidents to the database...')
        # Bulk create in batches
        with transaction.atomic():
            CrimeIncident.objects.bulk_create(incidents_to_create, batch_size=2000)

        self.stdout.write(self.style.SUCCESS('Successfully seeded crime data!'))
