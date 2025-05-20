import logging
import requests


class TMDBClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"

    def _get(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        params = {"api_key": self.api_key}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Failed to fetch {endpoint}: {e}")
            return None

    def get_show_details(self, show_id):
        return self._get(f"/tv/{show_id}")

    def build_episode_map(self, show_id):
        show_data = self.get_show_details(show_id)
        if not show_data:
            return {}

        episode_map = {}
        for season in show_data.get("seasons", []):
            season_number = season["season_number"]
            season_details = self._get(f"/tv/{show_id}/season/{season_number}")
            if not season_details:
                continue

            for episode in season_details.get("episodes", []):
                episode_number = episode["episode_number"]
                key = str(episode["episode_number"] + (season_number - 1) * 100)
                episode_map[key] = {
                    "season_number": season_number,
                    "episode_number": episode_number,
                    "name": episode["name"],
                    "season_name": season.get("name", f"Season {season_number}"),
                }
        return episode_map
