import argparse
import json
import logging
import os
from dotenv import load_dotenv

from core.renamer import rename_files
from core.tmdb_client import TMDBClient

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",  # ISO 8601 without timezone
)

def main():
    parser = argparse.ArgumentParser(description="Media Renamer Script")
    parser.add_argument("--config", required=True, help="Path to config JSON file")
    args = parser.parse_args()

    try:
        with open(args.config, "r") as f:
            config = json.load(f)
    except Exception as e:
        logging.critical(f"Failed to load config: {e}")
        return

    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        logging.critical("TMDB_API_KEY not set in .env file.")
        return

    tmdb_client = TMDBClient(api_key)
    episode_map = tmdb_client.build_episode_map(config["show_id"])
    rename_files(episode_map, config)

if __name__ == "__main__":
    main()
