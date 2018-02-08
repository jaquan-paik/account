import logging

from infra.configure.config import FilterConfig


class NotFoundFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record, 'request') and hasattr(record, 'status_code'):
            if self._include_ignore_url(record.request.path) and record.status_code == 404:
                return False
        return True

    def _include_ignore_url(self, path):
        ignores = FilterConfig.ignore_404_filter_url()
        for ignore in ignores:
            if ignore.search(path):
                return True
        return False
