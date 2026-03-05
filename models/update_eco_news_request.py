from dataclasses import dataclass, field, asdict
from typing import List
import json

from enums.language import Language
from enums.news_tag import EcoNewsTag


@dataclass
class UpdateEcoNewsRequest:
    """ Data Transfer Object (DTO) for updating EcoNews via API. """
    id: int
    title: str
    content: str
    short_info: str
    tags: List[str] = field(default_factory=list)
    source: str = ""

    def get_tags_en(self) -> List[str]:
        """ Map tags to English locale. """
        return EcoNewsTag.map_strings_to_locale(self.tags, Language.EN)

    def get_tags_uk(self) -> List[str]:
        """ Map tags to Ukrainian locale. """
        return EcoNewsTag.map_strings_to_locale(self.tags, Language.UK)

    def to_json(self) -> str:
        """ Convert DTO to JSON string. """
        return json.dumps(asdict(self), ensure_ascii=False)
