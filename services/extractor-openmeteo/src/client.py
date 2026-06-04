import httpx
from .config import BASE_URL

def fetch_point(latitude, longitude, hourly_vars) -> dict:
	params = {
		"latitude": latitude,
		"longitude": longitude,
		"hourly": ",".join(hourly_vars),
	}
	try:
		response = httpx.get(BASE_URL, params=params)
		response.raise_for_status()
		return response.json()
	except httpx.HTTPError as exc:
		print(f"Error while requesting {exc.request.url!r}.")
		raise #! maybe exit need to see later