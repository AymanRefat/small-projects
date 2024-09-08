import json
from typing import List

file_name = "data.json"
indent = 4


def read_file() -> List[dict] | None:
    """read the file and return the data , return None if file is empty"""
    with open(file_name, "r") as file:
        content = file.read()
        if content:
            return json.loads(content)


def write_file(data: List[dict]) -> None:
    with open(file_name, "w") as file:
        json.dump(data, file, indent=indent, default=str)
