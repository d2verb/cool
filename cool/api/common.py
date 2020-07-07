class ApiException(Exception):
    def __init__(self, status: int, data: str) -> None:
        super().__init__()
        self.__status = status
        self.__data = data

    @property
    def status(self) -> int:
        return self.__status

    @property
    def data(self) -> str:
        return self.__data

    def __str__(self) -> str:
        return f"{self.status} {self.data}"
