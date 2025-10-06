import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from adam.env
load_dotenv(dotenv_path="adam.env")

class Genius:
    def __init__(self, access_token=None):
        # Use token from env if not passed directly
        self.access_token = access_token or os.getenv("ACCESS_CODE")
        self.base_url = "https://api.genius.com"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def get_artist(self, search_term):
        # Step 1: Search for the artist
        search_url = f"{self.base_url}/search"
        params = {"q": search_term}
        response = requests.get(search_url, headers=self.headers, params=params)
        data = response.json()

        # Step 2: Extract the primary artist ID from the first hit
        first_hit = data["response"]["hits"][0]
        artist_id = first_hit["result"]["primary_artist"]["id"]

        # Step 3: Use the artist ID to get artist info
        artist_url = f"{self.base_url}/artists/{artist_id}"
        artist_response = requests.get(artist_url, headers=self.headers)
        artist_data = artist_response.json()

        return artist_data

    def get_artists(self, search_terms):
        results = []

        for term in search_terms:
            try:
                artist_data = self.get_artist(term)
                artist_info = artist_data["response"]["artist"]

                results.append({
                    "search_term": term,
                    "artist_name": artist_info.get("name"),
                    "artist_id": artist_info.get("id"),
                    "followers_count": artist_info.get("followers_count")
                })
            except Exception:
                results.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })

        return pd.DataFrame(results)