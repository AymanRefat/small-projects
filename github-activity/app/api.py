import requests


def get_events(username:str)->list[dict]:
	"""get the events for a given user"""
	url = f"https://api.github.com/users/{username}/events"
	response = requests.get(url)
	if response.status_code != 200:
		raise Exception(f"Error: {response.status_code}")
	return response.json()