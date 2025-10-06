import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Setting up access to adam.env to load in the access token
load_dotenv(dotenv_path="adam.env")

# Genius API interaction class
class Genius:
    def __init__(self, access_token=None):
        '''
        Function to initialize the Genius API client.
        If no access_token is provided, it will look for ACCESS_CODE in environment variables.
        
        Parameters:
        access_token (str): The access token for the Genius API.
        
        Returns:
        None
        '''
        # Use token from env if not passed directly
        self.access_token = access_token or os.getenv("ACCESS_CODE")
        self.base_url = "https://api.genius.com"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def get_artist(self, search_term):
        '''
        Function to get a single artist's information from Genius API based on search term.
        
        Parameters:
        search_term (str): The name of the artist to search for.
        
        Returns:
        dict: The artist's information from the Genius API.
        '''
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
        '''
        Function to get multiple artists' information from Genius API based on a list of search terms.
        
        Parameters:
        search_terms (list): A list of artist names to search for.
        
        Returns:
        pd.DataFrame: A DataFrame containing artist information for each search term.
        '''
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