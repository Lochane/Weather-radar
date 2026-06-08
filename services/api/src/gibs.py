import httpx
from .config import BASE_URL

def fetch_point(time:str, row:str, col:str) -> bytes:
	url = BASE_URL
	url +=  "/".join((time , "250m", "6.1", row, col))
	url += ".jpg"

	try:
		response = httpx.get(url)
		response.raise_for_status()
		return response.content
	
	except (httpx.HTTPStatusError, httpx.RequestError) as exc:
		print(f"Error while requesting {exc.request.url!r}: {exc.response}")
		return