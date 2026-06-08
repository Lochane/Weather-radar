import psycopg
import asyncio
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .config import BOTO_CLIENT, BUCKET_NAME, log_json

from .db import get_conn


def ensure_bucket():
	client = BOTO_CLIENT
	try:
		log_json("ensure_bucket.head_attempt", bucket=BUCKET_NAME)
		client.head_bucket(Bucket=BUCKET_NAME)
		log_json("ensure_bucket.exists", bucket=BUCKET_NAME)
		return
	except ClientError as exc:
		status = exc.response.get('ResponseMetadata', {}).get('HTTPStatusCode')
		if status == 404:
			try:
				log_json("ensure_bucket.create_attempt", bucket=BUCKET_NAME)
				client.create_bucket(Bucket=BUCKET_NAME)
				log_json("ensure_bucket.created", bucket=BUCKET_NAME)
				return
			except ClientError as exc2:
				log_json("ensure_bucket.create_failed", bucket=BUCKET_NAME, error=str(exc2))
				raise
		else:
			log_json("ensure_bucket.error", bucket=BUCKET_NAME, error=str(exc))
			raise


@asynccontextmanager
async def lifespan(app: FastAPI):
	log_json("lifespan.start")
	try:
		await asyncio.to_thread(ensure_bucket)
		log_json("lifespan.ensure_bucket_ok")
	except Exception as e:
		log_json("lifespan.ensure_bucket_failed", error=str(e))
		raise
	try:
		yield
	finally:
		log_json("lifespan.stop")

app = FastAPI(title="Radar API", version="0.1.0", lifespan=lifespan)

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