import dataclasses
from datetime import datetime
from typing import Callable, List, Optional
from urllib.parse import urljoin

import requests

from cool.api.common import ApiException


class CTFtimeFatalError(ApiException):
    pass


@dataclasses.dataclass(frozen=True)
class CTFEvent:
    organizers: List[str]
    onsite: bool
    title: str
    url: str
    start: datetime
    finish: datetime
    weight: float
    format: str


class CTFtimeApi:
    """
    This is a static class for accessing the CTFTime API.
    """

    API_BASE = "https://ctftime.org/api/v1/"

    @classmethod
    def events(
        cls, limit: int = 1, start: Optional[int] = None, finish: Optional[int] = None
    ) -> List[CTFEvent]:
        """
        Get ctf events.

        :calls: `POST /events/`
        :return: list of ctf events
        """

        params = {"limit": limit}

        if start is not None:
            params["start"] = start
        if finish is not None:
            params["finish"] = finish

        status, data = cls.__api("events/", requests.get, params=params)

        if status != 200:
            raise CTFtimeFatalError(status, "Failed to get event information")

        events = []
        for event_info in data:
            event = CTFEvent(
                organizers=[org["name"] for org in event_info["organizers"]],
                onsite=event_info["onsite"],
                title=event_info["title"],
                url=event_info["onsite"],
                start=datetime.fromisoformat(event_info["start"]),
                finish=datetime.fromisoformat(event_info["finish"]),
                weight=event_info["weight"],
                format=event_info["format"],
            )
            events.append(event)

        return events

    @classmethod
    def __api(cls, path: str, method: Callable, **kwargs):
        """
        The basic function for calling CTFtime API.
        """
        url = urljoin(cls.API_BASE, path)

        # fake user agent
        ua = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        )

        kwargs["headers"] = {"User-Agent": ua}

        response = method(url, **kwargs)
        return response.status_code, response.json()
