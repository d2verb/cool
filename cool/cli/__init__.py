from cool.cli.ctftime import CTFtime
from cool.cli.postbin import postbin


class Pipeline:
    def __init__(self):
        self.ctftime = CTFtime()
        self.postbin = postbin
