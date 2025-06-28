import argparse
import json
import os
from dotenv import load_dotenv

from core.logger import get_logger
from core.tmdb_client import TMDBClient
from core.renamer import rename_files
from core.legacy_renamer import rename_legacy_structure

load_dotenv()

logger = get_logger(__name__)

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
    parser.add_argument("--legacy", action="store_true", help="Use legacy renaming")
    args = parser.parse_args()

    config_path = os.path.join("configs", args.config)
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception as e:
        logger.critical(f"Failed to load config {args.config}: {e}")
        return

    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        logger.critical("TMDB_API_KEY not set in .env file.")
        return

    tmdb_client = TMDBClient(api_key)
    show_details = tmdb_client.get_show_details(config["show_id"])

    if args.legacy:
        logger.info("Using legacy renamer")
        rename_legacy_structure(
            show_details=show_details,
            base_dir=config["source_dir"],
            dry_run=args.dry_run,
        )
    else:
        episode_map = tmdb_client.build_episode_map(config["show_id"])

        try:
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
        except Exception as e:
            logger.critical(f"💥 fatal error: {e}")

if __name__ == "__main__":
    main()
