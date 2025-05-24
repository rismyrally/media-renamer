import os
import re
import shutil
from pathlib import Path

from core.logger import get_logger
from core.utils import sanitize_filename, extract_episode_number

logger = get_logger(__name__)

def sanitize(name):
    return re.sub(r'[\\\\/:*?"<>|]', "", name)


def rename_files(
    show_details,
    source_dir,
    target_dir,
    episode_map,
    file_pattern,
    use_named_season,
    move_files,
    dry_run,
):
    show_title = f"{sanitize_filename(show_details['name'])} ({show_details['first_air_date'][:4]})"

    for root, _, files in os.walk(source_dir):
        for file in files:
            if not file.lower().endswith((".mkv", ".mp4", ".avi")):
                continue

            full_source_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_source_path, source_dir)
            episode_key = extract_episode_number(rel_path, file_pattern)

            if episode_key not in episode_map:
                logger.warning(f"Skipping unmatched file: {rel_path}")
                continue

            episode_info = episode_map[episode_key]
            season_folder = f"Season {episode_info['season_number']}"
            if use_named_season:
                season_folder += f"- {sanitize_filename(episode_info['season_name'])}"

            episode_folder = f"Episode {episode_info['episode_number']:02d} - {sanitize_filename(episode_info['episode_name'])}"
            episode_filename = f"S{episode_info['season_number']:02d}E{episode_info['episode_number']:02d}{os.path.splitext(file)[1]}"

            final_dir = os.path.join(
                target_dir, show_title, season_folder, episode_folder
            )
            final_path = os.path.join(final_dir, episode_filename)

            logger.info(
                f"{'[DRY RUN] ' if dry_run else ''}{'Moving' if move_files else 'Copying'} {file} -> {final_path}"
            )

            if not dry_run:
                os.makedirs(final_dir, exist_ok=True)
                if move_files:
                    shutil.move(full_source_path, final_path)
                else:
                    shutil.copy2(full_source_path, final_path)
