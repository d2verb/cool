from datetime import datetime
from typing import Optional

from ctftools.api.ctftime import CTFtimeApi
from termcolor import colored


class CTFtime:
    def event(
        self, limit: int = 1, start: Optional[str] = None, finish: Optional[str] = None
    ) -> None:
        # convert --start from datetime string to unix timestamp
        try:
            start_timestamp = None
            if start is not None:
                start_timestamp = int(datetime.fromisoformat(start).timestamp())
        except ValueError:
            print(f"failed to parse --start: {start}")

        # convert --finish from datetime string to unix timestamp
        try:
            finish_timestamp = None
            if finish is not None:
                finish_timestamp = int(datetime.fromisoformat(finish).timestamp())
        except ValueError:
            print(f"failed to parse --finish: {finish}")

        # call events api
        events = CTFtimeApi.events(
            limit=limit, start=start_timestamp, finish=finish_timestamp
        )

        def headtxt(txt: str) -> str:
            return colored(txt, "green")

        print("========================")
        for event in events:
            print(f"{headtxt('title')}  : {event.title}")
            print(f"{headtxt('weight')} : {event.weight}")
            print(f"{headtxt('start')}  : {event.start}")
            print(f"{headtxt('finish')} : {event.finish}")
            print(f"{headtxt('format')} : {event.format}")
            print("========================")
