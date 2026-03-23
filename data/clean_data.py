import csv
import os

input_file = "data/raw/tops_crime_data_20260312_151016.csv"
output_file = "data/processed/tops_crime_data_cleaned.csv"

cols_to_remove = {"BEAT", "INCIDENT_TIME_ADJ", "LEGEND2", "OBJECTID", "REPORT_NUMBER"}

os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(input_file, "r", newline="", encoding="utf-8") as infile, open(
    output_file, "w", newline="", encoding="utf-8"
) as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    try:
        headers = next(reader)
        # Store index of columns to keep
        keep_indices = [i for i, h in enumerate(headers) if h not in cols_to_remove]

        # Write header
        writer.writerow([headers[i] for i in keep_indices])

        # Write data rows
        for row in reader:
            if row:
                writer.writerow([row[i] for i in keep_indices])
        print(f"Successfully cleaned data. Saved to {output_file}")
    except StopIteration:
        print("File is empty.")
