import sqlite3

from common import conf
from common.dispatcher import Service


class MatchServices(Service):
    def __init__(self, host, sid = conf.MATCH_SERVICES):
        super(MatchServices, self).__init__(sid)
        self.host = host