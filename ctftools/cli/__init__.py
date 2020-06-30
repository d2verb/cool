from ctftools.cli.ctftime import CTFtime
from ctftools.cli.postbin import postbin


class Pipeline:
    def __init__(self):
        self.ctftime = CTFtime()
        self.postbin = postbin
