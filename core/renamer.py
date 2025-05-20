import logging
import os
import re
import shutil
from pathlib import Path
from core.utils import sanitize_filename, extract_episode_number


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
    show_title = f"{show_details['name']} ({show_details['first_air_date'][:4]})"
    target_root = Path(target_dir) / sanitize_filename(show_title)

    source_path = Path(source_dir)
    matched_files = list(source_path.rglob(file_pattern or "*.mkv"))

    if not matched_files:
        logging.warning("No files matched in the source directory.")
        return

    for file in matched_files:
        episode_num = extract_episode_number(file.name)
        if episode_num is None:
            logging.warning(f"Skipping file (episode number not found): {file.name}")
            continue

        episode_info = episode_map.get(str(episode_num))
        if not episode_info:
            logging.warning(f"No TMDB info for episode {episode_num}")
            continue

        season_number = episode_info["season_number"]
        episode_title = episode_info["name"]
        season_name = episode_info.get("season_name", "")

        season_folder = (
            f"Season {season_number}- {sanitize_filename(season_name)}"
            if use_named_season
            else f"Season {season_number}"
        )
        episode_folder = f"Episode {episode_info['episode_number']:02d} - {sanitize_filename(episode_title)}"
        target_episode_path = target_root / season_folder / episode_folder
        target_episode_path.mkdir(parents=True, exist_ok=True)

        target_file_name = (
            f"S{season_number:02d}E{episode_info['episode_number']:02d}{file.suffix}"
        )
        target_file_path = target_episode_path / target_file_name

        logging.info(
            f"{'[DRY RUN] ' if dry_run else ''}{'Moving' if move_files else 'Copying'} {file} -> {target_file_path}"
        )

        if not dry_run:
            if move_files:
                shutil.move(str(file), str(target_file_path))
            else:
                shutil.copy2(str(file), str(target_file_path))
