# Media Renamer

A modular Python tool to rename and organize TV show and movie files using TMDb metadata.

## Features

- Uses TMDB to fetch show, episode, and season details.
- Renames and organizes files into proper folder structure.
- Configurable for any TV show using simple JSON configs.

## Requirements

- Python 3.7+
- TMDB account + API key

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

## Usage

```sh
python main.py --config one_piece.json
```
Configs are stored in the `configs/` folder.

## Config Structure (`configs/one_piece.json`)

```json
{
  "show_id": 37854,
  "source_dir": "D:/One Piece (1999)"
}
```

## Output Structure

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
