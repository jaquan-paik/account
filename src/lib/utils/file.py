import os

from lib.secret.secret import ImproperlyConfigured


class FileHandler:
    def __init__(self):
        self._set_root_path()

    def _set_root_path(self) -> None:
        self.root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    def get_file_path(self, file_name: str) -> str:
        return os.path.join(self.root_path, file_name)

    def save_file(self, file_name: str, content: str) -> None:
        file_path = self.get_file_path(file_name)
        with open(file_path, 'w') as file:
            file.write(content)

    def load(self, file_name: str) -> str:
        file_path = self.get_file_path(file_name)
        try:
            with open(file_path) as file:
                return file.read()
        except (OSError, IOError):
            raise ImproperlyConfigured('There is no setting file %s' % file_path)
