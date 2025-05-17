import logging
import requests


class TMDBClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.session = requests.Session()
        self.base_url = "https://api.themoviedb.org/3"

    def build_episode_map(self, show_id):
        episode_map = {}

        try:
            response = self.session.get(
                f"{self.base_url}/tv/{show_id}", params={"api_key": self.api_key}
            )
            response.raise_for_status()
            show_data = response.json()

            for season in show_data.get("seasons", []):
                season_number = season["season_number"]
                season_details = self.get_season_details(show_id, season_number)
                season_name = season.get("name")

                for ep in season_details.get("episodes", []):
                    episode_map[ep["episode_number"]] = {
                        "season_number": season_number,
                        "season_name": season_name,
                        "episode_name": ep["name"],
                    }

        except Exception as e:
            logging.error(f"Error building episode map: {e}")

        return episode_map

    def get_season_details(self, show_id, season_number):
        try:
            response = self.session.get(
                f"{self.base_url}/tv/{show_id}/season/{season_number}",
                params={"api_key": self.api_key},
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            logging.error(f"Failed to get season {season_number} details: {e}")
            return {}
