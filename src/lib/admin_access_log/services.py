from .constants import RequestMethod
from .models import AdminUrlAccessHistory


def is_unnecessary(url: str) -> bool:
    return url in ['/jsi18n/']


def add_log(staff_id: int, method: str, url: str) -> bool:
    if is_unnecessary(url):
        return False

    history = AdminUrlAccessHistory.create(staff_id, RequestMethod.convert(method), url)
    history.save()
    return True
