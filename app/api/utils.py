import json
import os
import random
import string

from typing import Union

from flask import current_app


class ImageHandler:
    def __init__(self, file):
        self.file = file

    def generate_filename(self) -> str:
        try:
            file_extension = "." + self.file.filename.split(".")[-1]
            filename = self.generate_random_string(10)
            return filename + file_extension
        except Exception:
            return None

    def save_file(self, filename: str) -> Union[str, None]:
        error = None
        try:
            if not os.path.exists(current_app.config["IMG_DIR"]):
                os.mkdir(current_app.config["IMG_DIR"])

            file_path = os.path.join(current_app.config["IMG_DIR"], filename)
            self.file.save(file_path)
        except Exception as e:
            error = getattr(e, "message", str(e))
        return error

    @staticmethod
    def generate_random_string(length: int = None) -> str:
        length = 10 if length is None else length
        letters = string.ascii_lowercase
        rand_string = "".join(random.choice(letters) for i in range(length))
        return rand_string


def response_bad(error, status: int):
    return (
        json.dumps({"error": getattr(error, "message", str(error))}),
        status,
        {"Content-Type": "application/json"},
    )


def response_ok(response: dict, status: int) -> tuple:
    return (
        json.dumps(response),
        status,
        {"Content-Type": "application/json"},
    )


def response_error(message: str, status: int) -> tuple:
    return (
        json.dumps({"error": message}),
        status,
        {"Content-Type": "application/json"},
    )
