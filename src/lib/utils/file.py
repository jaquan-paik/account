import os

from django.conf import settings

from lib.base.exceptions import MsgException


class FileHandler:
    def __init__(self, relative_file_path: str):
        self.relative_file_path = relative_file_path

    def get_absolute_file_path(self) -> str:
        return os.path.join(settings.BASE_DIR, self.relative_file_path)

    def load(self) -> str:
        try:
            with open(self.get_absolute_file_path()) as file:
                return file.read()
        except (OSError, IOError):
            raise MsgException('존재하지 않는 파일입니다.')
