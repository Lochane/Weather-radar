import uuid
import json
from .config import POINTS
from . import client, load, transform

def log_json(event, **kwargs):
	log = {"event": event, **kwargs}
	print(json.dumps(log))

def main():
	run_id = uuid.uuid4()
	log_json("START", run_id=str(run_id), n_points=len(POINTS))
	for point in POINTS:
		try:
			payload = client.fetch_point(point[1], point[2], ["temperature_2m", "precipitation", "wind_speed_10m"])
			rows = transform.to_rows(payload)
			load.upsert_rows(rows, run_id)
			log_json("OK", run_id=str(run_id), point=point, n_rows=(len(rows)))
		except Exception as e:
			log_json("ERROR", run_id=str(run_id), point=point, error=str(e))
	log_json("END", run_id=str(run_id))
	return 0


if __name__ == "__main__":
	main()