import csv
import json
from datetime import datetime, timedelta
import pytz

def data_preprocessor(input_file, output_file):
    """
    Processes a CSV file containing taxi trip data, converting raw polyline
    and timestamp data into enriched output including:
        - WKT formatted polyline
        - Timestamp array
        - Start and end local times
        - Travel duration
        - Hour of the day
        - Number of recorded points

    Parameters:
        input_file (str): Path to the input CSV file with raw taxi data.
        output_file (str): Path to the output CSV file to save processed data.
    """
    lisbon_tz = pytz.timezone('Europe/Lisbon')

    input_count = 0
    output_count = 0

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = [
            'trip_id', 'call_type', 'origin_call', 'origin_stand',
            'taxi_id', 'day_type', 'missing_data',
            'polyline', 'timestamps', 'total_travel_time',
            'start_local_time', 'end_local_time', 'hour_of_day', 'point_count'
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            input_count += 1

            try:
                poly_raw = row['POLYLINE']
                # Skip entries with no valid polyline
                if poly_raw in ('[]', '""', ''):
                    continue

                polyline = json.loads(poly_raw)
                # Skip entries with fewer than 2 points
                if len(polyline) < 2:
                    continue

                # Construct WKT-formatted LINESTRING from polyline
                linestring = 'LINESTRING(' + ', '.join(f'{lon} {lat}' for lon, lat in polyline) + ')'

                # Compute UTC start time from UNIX timestamp
                ts = int(row['TIMESTAMP'])
                start_utc = datetime.utcfromtimestamp(ts)

                # Each point is recorded every 15 seconds; compute trip duration
                total_seconds = (len(polyline) - 1) * 15
                end_utc = start_utc + timedelta(seconds=total_seconds)

                # Generate PostgreSQL-compatible timestamp array
                timestamp_array = ['"' + (start_utc + timedelta(seconds=15 * i)).strftime('%Y-%m-%dT%H:%M:%SZ') + '"'
                                   for i in range(len(polyline))]
                timestamp_pg_array = '{' + ','.join(timestamp_array) + '}'

                # Convert start and end time to local time
                start_time = lisbon_tz.normalize(start_utc.replace(tzinfo=pytz.utc).astimezone(lisbon_tz))
                end_time = lisbon_tz.normalize(end_utc.replace(tzinfo=pytz.utc).astimezone(lisbon_tz))

                # Write processed data to output CSV
                writer.writerow({
                    'trip_id': row['TRIP_ID'],
                    'call_type': row['CALL_TYPE'],
                    'origin_call': row['ORIGIN_CALL'],
                    'origin_stand': row['ORIGIN_STAND'],
                    'taxi_id': row['TAXI_ID'],
                    'day_type': row['DAY_TYPE'],
                    'missing_data': row['MISSING_DATA'],
                    'polyline': linestring,
                    'timestamps': timestamp_pg_array,
                    'total_travel_time': total_seconds,
                    'start_local_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'end_local_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'hour_of_day': start_time.hour,
                    'point_count': len(polyline)
                })

                output_count += 1
                
            except Exception as e:
                print(f"[Error] Trip {row.get('TRIP_ID', 'UNKNOWN')} - {e}")

    print(f"Input rows: {input_count}")
    print(f"Output rows: {output_count}")

print("Processing train.csv...")
data_preprocessor('train.csv', 'train_preprocessed.csv')
print("Processing complete.")
