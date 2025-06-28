import os
import re
import traceback

from core.logger import get_logger
from core.utils import is_video_file

logger = get_logger(__name__)

# === regex patterns ===
season_pattern = re.compile(r"Season\s*(\d+)", re.IGNORECASE)
episode_pattern = re.compile(r"Episode\s*(\d+)", re.IGNORECASE)


def fetch_show_metadata(show_details):
    try:
        return show_details["name"], show_details["first_air_date"][:4]
    except Exception as e:
        logger.error(f"💥 failed to fetch show metadata: {e}")
        raise


def rename_episodes_in_season(season_path: str, season_number: int, dry_run: bool):
    for dirpath, _, filenames in os.walk(season_path):
        for filename in filenames:
            if not is_video_file(filename):
                continue

            try:
                match = episode_pattern.search(dirpath)
                if not match:
                    logger.warning(f"⚠️ skipping (no episode number found): {dirpath}")
                    continue

                episode_num = int(match.group(1))

                ext = os.path.splitext(filename)[1]
                new_filename = f"S{season_number:02d}E{episode_num:02d}{ext}"

                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, new_filename)

                if os.path.exists(new_path):
                    logger.warning(f"❌ skipping (already exists): {new_path}")
                    continue

                logger.info(
                    f"🔄 {'[DRY RUN] ' if dry_run else ''}renaming: {old_path} → {new_path}"
                )

                if not dry_run:
                    os.rename(old_path, new_path)

            except Exception:
                logger.error(f"💥 error renaming file in: {dirpath}")
                logger.debug(traceback.format_exc())


def rename_base_directory(old_path: str, show_name: str, year: str, dry_run: bool):
    parent_dir = os.path.dirname(os.path.abspath(old_path))
    new_dir_name = f"{show_name} ({year})"
    new_path = os.path.join(parent_dir, new_dir_name)

    try:
        logger.info(
            f"🏷️ {'[DRY RUN] ' if dry_run else ''}renaming base directory: {old_path} → {new_path}"
        )
        if not dry_run:
            os.rename(old_path, new_path)
    except Exception:
        logger.error(f"💥 failed to rename base directory: {old_path}")
        logger.debug(traceback.format_exc())


def rename_legacy_structure(show_details, base_dir, dry_run):
    try:
        logger.info("🔍 fetching metadata")
        show_title, show_year = fetch_show_metadata(show_details)
        logger.info(f"🎬 fetched metadata for: {show_title} [{show_year}]")

        logger.info(f"📁 renaming episodes in: {base_dir}")
        for season_dir in os.listdir(base_dir):
            try:
                season_match = season_pattern.match(season_dir)
                if not season_match:
                    continue

                season_number = int(season_match.group(1))

                season_path = os.path.join(base_dir, season_dir)

                if not os.path.isdir(season_path):
                    logger.warning(f"⚠️ skipping non-directory: {season_path}")
                    continue

                logger.info(f"📁 processing {season_dir} (Season {season_number})")
                rename_episodes_in_season(season_path, season_number, dry_run)

            except Exception:
                logger.error(f"💥 error processing season folder: {season_dir}")
                logger.debug(traceback.format_exc())

        rename_base_directory(base_dir, show_title, show_year, dry_run)

    except Exception as e:
        logger.critical(f"💥 fatal error: {e}")
