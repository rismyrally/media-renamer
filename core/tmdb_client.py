import tmdbsimple as tmdb
import logging


class TMDBClient:

    def __init__(self, api_key: str):
        tmdb.API_KEY = api_key
        self.logger = logging.getLogger(__name__)

    def get_show_details(self, show_id: int):
        try:
            show = tmdb.TV(show_id)
            return show.info()
        except Exception as e:
            self.logger.error(f"Error fetching show details for ID {show_id}: {e}")
            return None

    def build_episode_map(self, show_id: int):
        try:
            show_data = self.get_show_details(show_id)
            if not show_data:
                return {}

            episode_map = {}
            for season in show_data.get("seasons", []):
                season_number = season["season_number"]
                season_details = tmdb.TV_Seasons(show_id, season_number).info()
                if not season_details:
                    continue

                for episode in season_details.get("episodes", []):
                    episode_number = episode["episode_number"]
                    episode_map[(season_number, episode_number)] = {
                        "season_number": season_number,
                        "episode_number": episode_number,
                        "name": episode["name"],
                        "season_name": season.get("name", f"Season {season_number}"),
                    }
            return episode_map
        except Exception as e:
            self.logger.error(f"Error building episode map for show ID {show_id}: {e}")
            return {}
