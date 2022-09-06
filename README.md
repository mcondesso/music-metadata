# Music Metadata

This script adds metadata to music files by parsing the filename.

It assumes the following format: `<artist_name> - <song_title>.<file_extension>`
* the separator between `artist_name` and `song_title` is the first occurrence of " - "
* multiple artists can be separated by `&`

## Setup and Run
A virtual environment needs to be set:
* `python -m venv env`
* `source env/bin/activate`
* `pip install -r requirements.txt`

And a `.env` file should be provided containing:
```
COLLECTION_PATH=<path_to_the_mp3_file_collection>
```

After that, simply run `python main.py`