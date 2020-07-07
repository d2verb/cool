import dataclasses
from typing import Callable, Tuple
from urllib.parse import urljoin

import requests

from .common import ApiException


class PostBinRequestNotFoundError(ApiException):
    pass


class PostBinFatalError(ApiException):
    pass


@dataclasses.dataclass(frozen=True)
class PostBinRequest:
    method: str
    path: str
    headers: dict
    query: dict
    body: dict
    ip: str
    inserted: int


class PostBinApi:
    """
    This is a static class for accessing the PostBin API.
    """

    API_BASE: str = "https://postb.in/api/"

    @classmethod
    def url(cls, binid: str) -> str:
        return f"https://postb.in/{binid}"

    @classmethod
    def create(cls) -> str:
        """
        Create a new bin.

        :calls: `POST /bin`
        :return str: The id of the created bin.
        """
        status, data = cls.__api("bin", requests.post)

        if status != 201:
            raise PostBinFatalError(status, data["msg"])

        return data["binId"]

    @classmethod
    def delete(cls, binid: str) -> None:
        """
        Delete the bin with the given binid.

        :calls: `DELETE /bin/:binid`
        """
        cls.__api(f"bin/{binid}", requests.delete)

    @classmethod
    def shift_request(cls, binid: str) -> PostBinRequest:
        """
        Fetch a request arrived at the bin with the given binid.

        :calls: `GET /bin/:binid/req/shift`
        """
        status, data = cls.__api(f"bin/{binid}/req/shift", requests.get)

        if status == 200:
            return PostBinRequest(
                method=data["method"],
                path=data["path"],
                headers=data["headers"],
                query=data["query"],
                body=data["body"],
                ip=data["ip"],
                inserted=data["inserted"],
            )

        if status == 404 and data["msg"] == "No requests in this bin":
            raise PostBinRequestNotFoundError(status, data["msg"])
        else:
            raise PostBinFatalError(status, data["msg"])

    @classmethod
    def __api(cls, path: str, method: Callable, **kwargs) -> Tuple[int, dict]:
        """
        The basic function for calling PostBin API.
        """
        url = urljoin(cls.API_BASE, path)
        response = method(url, **kwargs)
        return response.status_code, response.json()
