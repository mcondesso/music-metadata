import os
from typing import Tuple

from tqdm import tqdm
from mutagen.easyid3 import EasyID3
from dotenv import load_dotenv

load_dotenv(".env")


def get_mp3_files(directory: str) -> Tuple[str, str]:
    for root, dirs, files in os.walk(directory):
        for filename in files:
            yield (root, filename)


def parse_filename(filename: str) -> dict:
    without_extension = os.path.splitext(filename)[0]
    try:
        artists, title = without_extension.split(" - ", maxsplit=1)
    except ValueError as error:
        raise ValueError(f'error parsing filename "{filename}"')
    else:
        return {
            "artist": artists.split("&"),
            "title": title,
        }


def set_file_tags(filepath: str, tags: dict):
    tag_dict = EasyID3(filepath)
    for key, value in tags.items():
        tag_dict[key] = value
    tag_dict.save()


if __name__ == "__main__":
    collection_path = os.getenv("COLLECTION_PATH")
    for folder, filename in tqdm(get_mp3_files(collection_path)):
        metadata = parse_filename(filename)
        set_file_tags(
            filepath=os.path.join(folder, filename),
            tags=metadata,
        )
