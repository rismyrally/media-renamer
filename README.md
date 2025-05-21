# Media Renamer

A modular Python tool to rename and organize TV show and movie files using TMDb metadata.

## 🔧 Features

- Uses TMDB to fetch show, episode, and season details.
- Renames and organizes files into proper folder structure.
- Supports complex directory layouts with regex-based matching
- Organizes media into Kodi-friendly structure:
  `Show Name (Year)/Season X - Arc Name/Episode XX - Title/`
- Configurable for any TV show using simple JSON configs.
- Dry-run mode to preview changes safely
- Supports both move or copy operations

## 🧪 Requirements

- Python 3.7+
- A free [TMDB API key](https://www.themoviedb.org/settings/api)

## Setup

```sh
git clone https://github.com/rismyrally/media-renamer.git
cd media-rename
python -m venv .venv
source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# set your TMDB_API_KEY in .env
```

## ▶️ Usage

Run the script with your config file:

```sh
python main.py --config one_piece.json
```
### Optional Flags
- `--dry-run`
  Simulate the renaming process without actually moving or copying any files.

**Example:**
```sh
python main.py --config one_piece.json --dry-run
```

Configs are stored in the `configs/` folder.

## 📁 Config File Structure

```json
{
  "show_id": 37854,
  "source_dir": "D:/One Piece",
  "target_dir": "D:/",
  "file_pattern": "One Piece/Season (\\d+)/Episode (\\d+).*?/Episode (\\d+)",
  "use_named_season": true,
  "move_files": true
}
```
### Config Fields

| Field              | Description                                                |
| ------------------ | ---------------------------------------------------------- |
| `show_id`          | TMDB show ID                                               |
| `source_dir`       | Directory containing your existing media files             |
| `target_dir`       | Where to place renamed files (can be same as source)       |
| `file_pattern`     | Regex to extract season and episode numbers from full path |
| `use_named_season` | Add arc/season name to folder (e.g., `Season 6- Skypiea`)  |
| `move_files`       | `true` to move files, `false` to copy                      |


## 📂 Output Structure

Example output for One Piece:
```
One Piece (1999)/
├── Season 6- Skypiea/
│   └── Episode 144 - The Log is Taken! Salvage King, Masira!/
│       └── S06E144.mkv
...
```

## Notes

- File names must include a 4-digit episode number (e.g. `One Piece - 0144 - ...`).
- You can add more configs for other shows in `configs/`.
