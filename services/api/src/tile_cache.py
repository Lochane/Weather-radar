from botocore.exceptions import ClientError
from .config import BOTO_CLIENT, BUCKET_NAME

def store_object(content:bytes, key:str) -> None:
	client = BOTO_CLIENT
	try:
		client.put_object(Body=content, Bucket=BUCKET_NAME, Key=key)
	except ClientError as exc:
		# print(f"{exc}")
		raise
	
def get_object(key:str) -> bytes:
	client = BOTO_CLIENT
	try:
		object = client.get_object(Bucket=BUCKET_NAME, Key=key)
		return object
	except ClientError as exc:
		# print(f"{exc}")
		raise