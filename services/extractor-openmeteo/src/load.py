import psycopg
from .config import DATABASE_URL

def upsert_rows(rows: list[dict], run_id):

	with psycopg.connect(DATABASE_URL) as conn:
		with conn.cursor() as cur:
			for row in rows:
				cur.execute("""
				INSERT INTO raw.openmeteo_measurements(latitude, longitude, measured_at, temperature_2m, precipitation, wind_speed_10m, run_id) VALUES (%s, %s, %s, %s, %s, %s, %s)
				ON CONFLICT (latitude, longitude, measured_at) DO UPDATE SET temperature_2m = excluded.temperature_2m, precipitation = excluded.precipitation, wind_speed_10m= excluded.wind_speed_10m
				""", (row['latitude'], row['longitude'], row['measured_at'], row['temperature'], row['precipitation'], row['wind_speed_10m'], run_id))
		conn.commit()