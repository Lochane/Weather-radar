import boto3
import os
import json
# does not work that way, need parameters (set in gibs.fetch_point()) see https://nasa-gibs.github.io/gibs-api-docs/access-basics/ - OGC Web Map Tile Service (WMTS) for more information
BASE_URL = "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/"

BOTO_CLIENT = boto3.client('s3',
					endpoint_url=os.environ['MINIO_ENDPOINT'],
					aws_access_key_id=os.environ['MINIO_ROOT_USER'],
					aws_secret_access_key=os.environ['MINIO_ROOT_PASSWORD'],
					region_name="eu-west"
					)

BUCKET_NAME='gibs-tiles'

def log_json(event, **kwargs):
	log = {"event": event, **kwargs}
	print(json.dumps(log), flush=True)