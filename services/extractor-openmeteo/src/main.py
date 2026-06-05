import uuid
from . import client, load, transform, config

def main():
	run_id = uuid.uuid4()
	config.log_json("START", run_id=str(run_id), n_points=len(config.POINTS))
	for point in config.POINTS:
		try:
			payload = client.fetch_point(point[1], point[2], ["temperature_2m", "precipitation", "wind_speed_10m"], 5)
			rows = transform.to_rows(payload)
			load.upsert_rows(rows, run_id)
			config.log_json("OK", run_id=str(run_id), point=point, n_rows=(len(rows)))
		except Exception as e:
			config.log_json("ERROR", run_id=str(run_id), point=point, error=str(e))
	config.log_json("END", run_id=str(run_id))
	return 0


if __name__ == "__main__":
	main()