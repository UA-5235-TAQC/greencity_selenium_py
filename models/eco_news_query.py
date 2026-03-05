from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class EcoNewsQuery:
    """ Data Transfer Object for querying EcoNews via API. """
    author_id: Optional[int] = None
    favorite: Optional[bool] = None
    page: Optional[int] = None
    size: Optional[int] = None

    def to_params(self) -> Dict[str, Any]:
        """ Convert the query object to a dictionary suitable for HTTP GET parameters. """
        params = {
            "author-id": self.author_id,
            "favorite": self.favorite,
            "page": self.page,
            "size": self.size,
        }
        return {k: v for k, v in params.items() if v is not None}
