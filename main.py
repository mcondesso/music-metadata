import os
from typing import Tuple

from tqdm import tqdm
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
from dotenv import load_dotenv

load_dotenv(".env")

SUPPORTED_FORMATS = {".mp3", ".mp4"}

METADATA_TAGS = {
    ".mp3": {
        "artist": "artist",
        "title": "title",
    },
    ".mp4": {
        "artist": "©ART",
        "title": "©nam",
    },
}

METADATA_CLASSES = {
    ".mp3": EasyID3,
    ".mp4": MP4,
}


def get_music_files(directory: str) -> Tuple[str, str]:
    for root, _, files in os.walk(directory):
        for filename in files:
            if os.path.splitext(filename)[1] in SUPPORTED_FORMATS:
                yield (root, filename)


def parse_filename(filename: str) -> dict:
    filename_no_extension, file_extension = os.path.splitext(filename)
    artist_tag = METADATA_TAGS[file_extension]["artist"]
    title_tag = METADATA_TAGS[file_extension]["title"]

    filename_no_extension = filename_no_extension.replace("–", "-")
    try:
        artists, title = filename_no_extension.split(" - ", maxsplit=1)
    except ValueError as error:
        raise ValueError(f'error parsing filename "{filename}"') from error
    else:
        return {
            artist_tag: artists.split("&"),
            title_tag: title,
        }


def set_file_tags(filepath: str, tags: dict):
    file_extension = os.path.splitext(filepath)[1]
    tag_handling_class = METADATA_CLASSES[file_extension]

    tag_dict = tag_handling_class(filepath)
    for key, value in tags.items():
        tag_dict[key] = value
    tag_dict.save()


if __name__ == "__main__":
    collection_path = os.getenv("COLLECTION_PATH")
    for folder, filename in tqdm(get_music_files(collection_path)):
        metadata = parse_filename(filename)
        set_file_tags(
            filepath=os.path.join(folder, filename),
            tags=metadata,
        )
