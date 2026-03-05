from dataclasses import dataclass, asdict, field
from typing import List
import json


@dataclass
class EcoNewsRequest:
    """ Data Transfer Object (DTO) for creating or updating EcoNews via API. """
    title: str
    text: str
    source: str
    short_info: str
    tags: List[str] = field(default_factory=list)

    def to_json(self) -> str:
        """ Convert the DTO into a JSON string. """
        return json.dumps(asdict(self), ensure_ascii=False)
