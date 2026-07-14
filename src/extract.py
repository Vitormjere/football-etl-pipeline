import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "https://api.football-data.org/v4"
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

def get_standings(competition_code, season=None):
    url = f"{BASE_URL}/competitions/{competition_code}/standings"
    headers = {"X-Auth-Token": API_KEY}
    params = {}

    if season:
        params["season"] = season

    response = requests.get(url, headers=headers, params=params)

    return response.json()

def get_matches(competition_code, status=None, season=None):
    url = f"{BASE_URL}/competitions/{competition_code}/matches"
    headers = {"X-Auth-Token": API_KEY}
    params = {}

    if status:
        params["status"] = status
    if season:
        params["season"] = season

    response = requests.get(url, headers=headers, params=params)

    return response.json()

if __name__ == "__main__":
    dados = get_matches("PL", status="FINISHED", season="2025")
    print(dados)