import httpx
from time import sleep
from .config import BASE_URL

def is_retryable(exc) -> bool:
	if isinstance(exc, httpx.RequestError):
		return True
	if isinstance(exc, httpx.HTTPStatusError):
		return exc.response.status_code >= 500
	return False


def fetch_point(latitude, longitude, hourly_vars, max_retries) -> dict:
	params = {
		"latitude": latitude,
		"longitude": longitude,
		"hourly": ",".join(hourly_vars),
	}

	for tentative in range(max_retries):
		try:
			response = httpx.get(BASE_URL, params=params)
			response.raise_for_status()
			out = response.json()
			out['latitude'] = latitude
			out['longitude'] = longitude
			return out
		except (httpx.HTTPStatusError, httpx.RequestError) as exc:
			if not is_retryable(exc) or tentative == max_retries:
				print(f"Error while requesting {exc.request.url!r}.")
				raise
			sleep(1.0 * 2 ** tentative)