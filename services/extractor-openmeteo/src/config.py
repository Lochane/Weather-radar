import os
import json

POINTS = [
	("Paris", 48.85, 2.35),
	("Berlin", 52.52, 13.41),
	("Madrid", 40.42, -3.70),
	# ("Londre", 51.50, -0.12),
	# ("Bruxelles", 50.85, 4.35),
]

HOURLY_VARS = ["temperature_2m", "precipitation", "wind_speed_10m"]
BASE_URL    = "https://api.open-meteo.com/v1/forecast"
DATABASE_URL = os.environ["DATABASE_URL"]
FETCH_INTERVAL_SECONDS = 3600

def log_json(event, **kwargs):
	log = {"event": event, **kwargs}
	print(json.dumps(log))