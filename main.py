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
    parser.add_argument(
        "--config", required=True, help="Path to config JSON file (inside configs/)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the renaming without making changes",
    )
    args = parser.parse_args()

    config_path = os.path.join("configs", args.config)
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception as e:
        logging.critical(f"Failed to load config {args.config}: {e}")
        return

    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        logging.critical("TMDB_API_KEY not set in .env file.")
        return

    tmdb_client = TMDBClient(api_key)
    show_details = tmdb_client.get_show_details(config["show_id"])
    episode_map = tmdb_client.build_episode_map(config["show_id"])

    rename_files(
        show_details=show_details,
        source_dir=config["source_dir"],
        target_dir=config["target_dir"],
        episode_map=episode_map,
        file_pattern=config.get("file_pattern", ""),
        use_named_season=config.get("use_named_season", False),
        move_files=config.get("move_files", True),
        dry_run=args.dry_run,
    )

if __name__ == "__main__":
    main()
