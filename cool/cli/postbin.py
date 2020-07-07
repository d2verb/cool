import time

from cool.api.postbin import PostBinApi, PostBinRequestNotFoundError
from termcolor import colored


def receive_request_loop(binid: str) -> None:
    def headtxt(txt: str) -> str:
        return colored(txt, "green")

    idx = 1
    print("========================")
    while True:
        try:
            req = PostBinApi.shift_request(binid)

            print(f"{headtxt('no')}      : {idx}")
            print(f"{headtxt('method')}  : {req.method}")
            print(f"{headtxt('path')}    : {req.path}")
            print(f"{headtxt('headers')} : {req.headers}")
            print(f"{headtxt('query')}   : {req.query}")
            print(f"{headtxt('body')}    : {req.body}")
            print(f"{headtxt('ip')}      : {req.ip}")
            print("========================")

            # don't abuse api
            time.sleep(4)

            idx += 1
        except PostBinRequestNotFoundError:
            pass
        except Exception:
            print("something wrong...")
            break


def postbin() -> None:
    try:
        binid = PostBinApi.create()
        print(f"{colored('Bin URL', 'green')}: {PostBinApi.url(binid)}")

        receive_request_loop(binid)
    except KeyboardInterrupt:
        print(f"deleting bin({binid})...")
        PostBinApi.delete(binid)
