import datetime

class Utils(object):
    @staticmethod
    def timestamp():
        return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
