import json
from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any, List, Optional


@dataclass
class EcoNewsQuery:
    """ Data Transfer Object for querying EcoNews via API. """
    author_id: Optional[int] = None
    favorite: Optional[bool] = None
    page: Optional[int] = None
    size: Optional[int] = None
    title: Optional[str] = None
    sort: Optional[str] = None
    tags: Optional[list[str]] = None

    def to_params(self) -> Dict[str, Any]:
        """ Convert the query object to a dictionary suitable for HTTP GET parameters. """
        params = {
            "author-id": self.author_id,
            "favorite": self.favorite,
            "page": self.page,
            "size": self.size,
        }
        return {k: v for k, v in params.items() if v is not None}

    def to_json(self) -> str:
        """ Convert the DTO into a JSON string. """
        data = asdict(self)
        data["authorId"] = data.pop("author_id")
        return json.dumps(data, ensure_ascii=False)


@dataclass
class CommentQuery:
    """ Data Transfer Object for querying comments via API. """
    page: Optional[int] = None
    size: Optional[int] = None
    sort: List[str] = field(default_factory=list)
