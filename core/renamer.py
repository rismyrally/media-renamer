import logging
import os
import re
import shutil


def sanitize(name):
    return re.sub(r'[\\\\/:*?"<>|]', "", name)


def rename_files(source_dir, episode_map, config):
    for filename in os.listdir(source_dir):
        if not filename.lower().endswith((".mkv", ".mp4", ".avi")):
            continue

        match = re.search(r"(\d{4})", filename)
        if not match:
            logging.warning(f"Skipped (no episode number): {filename}")
            continue

        episode_num = int(match.group(1))
        episode_info = episode_map.get(episode_num)

        if not episode_info:
            logging.warning(f"Skipped (not found in TMDB map): {filename}")
            continue

        season_name = sanitize(
            f"Season {episode_info['season_number']}- {episode_info['season_name']}"
        )
        episode_folder = sanitize(
            f"Episode {episode_num} - {episode_info['episode_name']}"
        )
        new_filename = (
            f"S{episode_info['season_number']:02d}E{episode_num:03d}"
            + os.path.splitext(filename)[1]
        )

        target_dir = os.path.join(source_dir, season_name, episode_folder)
        os.makedirs(target_dir, exist_ok=True)

        src_path = os.path.join(source_dir, filename)
        dst_path = os.path.join(target_dir, new_filename)

        try:
            shutil.move(src_path, dst_path)
            logging.info(f"Renamed: {filename} -> {dst_path}")
        except Exception as e:
            logging.error(f"Failed to move {filename}: {e}")
