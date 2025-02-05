import dataclasses
from typing import Iterable


@dataclasses.dataclass
class URLComponents:
    scheme: str
    netloc: str
    url: str
    path: str
    query: str
    fragment: str

    def __iter__(self) -> Iterable:
        return iter([getattr(self, field.name) for field in dataclasses.fields(self)])
