from urllib.parse import parse_qsl, urlparse
from typing import Callable, Optional

from pydantic import BaseModel, HttpUrl


class _Config(BaseModel):
    verify_ssl: Optional[bool] = False


class ConfigMixin(BaseModel):
    config: _Config


class ResultSet(BaseModel):
    _endpoint: Optional[Callable] = None
    _more: Optional[Callable] = None

    count: Optional[int] = None
    previous: Optional[HttpUrl] = None
    next: Optional[HttpUrl] = None

    def _parse_params(self, url):
        return dict(url.query_params())

    def has_previous(self):
        return self.previous is not None

    def has_next(self):
        return self.next is not None

    def get_next(self):
        if not self.has_next() or not hasattr(self, "_more"):
            return
        params = self._parse_params(self.next)
        return self._more(**params)

    def get_previous(self):
        if not self.has_previous() or not hasattr(self, "_more"):
            return
        params = self._parse_params(self.previous)
        return self._more(**params)

    def iter_pages(self):
        next_page = self
        while next_page.has_next():
            next_page = next_page.get_next()
            yield next_page

    def iter_items(self):
        return iter(self.results)

    def iter_all(self):
        for item in self.iter_items():
            yield item
        for page in self.iter_pages():
            for item in page.iter_items():
                yield item

    def __iter__(self):
        return self.iter_items()
