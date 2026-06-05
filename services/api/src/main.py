import psycopg
from datetime import datetime
from fastapi import FastAPI

from .db import get_conn

app = FastAPI(title="Radar API", version="0.1.0")


@app.get("/")
async def root():
	return {"status": "ok", "service": "radar-api", "docs": "/docs"}


@app.get("/health")
async def health():
	return {"status": "ok", "service": "radar-api"}


@app.get("/weather/point")
async def weather_point(latitude: float, longitude: float, time: datetime | None = None):
	conn = get_conn()
	cur = conn.cursor()
	try:
		query = """
			SELECT *
			FROM raw.openmeteo_measurements
			WHERE latitude = %s
			AND longitude = %s
		"""
		params = [latitude, longitude]

		if time is not None:
			query += " AND measured_at = %s"
			params.append(time)

		cur.execute(query, params)
		rows = cur.fetchall()
		return [dict(row) for row in rows]
	except psycopg.Error as e:
		print("Error executing SELECT statement:", e)
		return {"error": "database query failed"}
	finally:
		cur.close()
		conn.close()