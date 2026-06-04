import datetime as dt
# from dateutil.parser import isoparse

def to_rows(payload: dict) -> list[dict]:
	latitude = payload["latitude"]
	longitude = payload["longitude"]
	hourly = payload["hourly"]
	times = hourly["time"]
	temperatures = hourly["temperature_2m"]
	precipitations = hourly["precipitation"]
	wind_speed_10m = hourly["wind_speed_10m"]

	rows = []
	for time, temp, preci, wind in zip(times, temperatures, precipitations, wind_speed_10m):
		rows.append({'latitude': latitude, 'longitude': longitude, 'measured_at': dt.datetime.fromisoformat(time).replace(tzinfo=dt.timezone.utc), 'temperature_2m': temp, 'precipitation': preci, 'wind_speed_10m': wind})
	return rows