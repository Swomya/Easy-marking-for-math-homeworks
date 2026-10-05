import os
import uuid

from app.service.ports import FileStorage

_EXT = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}


class LocalFileStorage(FileStorage):
    def __init__(self, folder: str):
        self._folder = folder
        os.makedirs(folder, exist_ok=True)

    def save(self, data: bytes, mime_type: str) -> str:
        path = os.path.join(self._folder, uuid.uuid4().hex + _EXT.get(mime_type, ".bin"))
        with open(path, "wb") as f:
            f.write(data)
        return path

    def delete(self, path: str) -> None:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
