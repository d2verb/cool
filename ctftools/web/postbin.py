from typing import Callable, NamedTuple
from urllib.parse import urljoin

import requests


class PostBinApiException(Exception):
    def __init__(self, status, data):
        super().__init__()
        self.__status = status
        self.__data = data

    @property
    def status(self):
        return self.__status

    @property
    def data(self):
        return self.__data

    def __str__(self):
        return f"{self.status} {self.data}"


class PostBinRequestNotFound(Exception):
    pass


class PostBinRequestFetchingFailed(Exception):
    pass


class PostBinCreationFailed(Exception):
    pass


class PostBinReceivedRequest(NamedTuple):
    method: str
    path: str
    headers: dict
    query: dict
    body: dict
    ip: str
    inserted: int


class PostBin:
    """
    This is a static class for accessing the PostBin API.
    """

    API_BASE = "https://postb.in/api/"

    @classmethod
    def create_bin(cls):
        """
        Create a new bin.

        :calls: `POST /bin`
        :return str: The id of the created bin.
        """
        status, data = cls.__api("bin", requests.post)

        if status != 201:
            raise PostBinCreationFailed(status, data["msg"])

        return data["binId"]

    @classmethod
    def delete_bin(cls, binid: str):
        """
        Delete the bin with the given binid.

        :calls: `DELETE /bin/:binid`
        """
        cls.__api(f"bin/{binid}", requests.delete)

    @classmethod
    def fetch_request(cls, binid: str):
        """
        Fetch a request arrived at the bin with the given binid.

        :calls: `GET /bin/:binid/req/shift`
        :return PostBinReceivedRequest: The request information sent to the bin with the given binid.
        """
        status, data = cls.__api(f"bin/{binid}/req/shift", requests.get)

        if status == 200:
            return PostBinReceivedRequest(
                method=data["method"],
                path=data["path"],
                headers=data["headers"],
                query=data["query"],
                body=data["body"],
                ip=data["ip"],
                inserted=data["inserted"],
            )

        if status == 404 and data["msg"] == "No requests in this bin":
            raise PostBinRequestNotFound(status, data["msg"])
        else:
            raise PostBinRequestFetchingFailed(status, data["msg"])

    @classmethod
    def __api(cls, path: str, method: Callable, **kwargs):
        """
        The basic function for calling PostBin API.
        """
        url = urljoin(cls.API_BASE, path)
        response = method(url, **kwargs)
        return response.status_code, response.json()
