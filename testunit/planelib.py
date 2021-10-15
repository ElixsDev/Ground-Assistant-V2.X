class Library:
    def __init__(self):
        from datetime import datetime
        from .models import New
        self.datetime = datetime
        self.new = New
        self.index = {}

    def add(self, beacon):
        if not beacon["address"] in self.index.keys():
            self.index[beacon["address"]] = self.new(beacon, coordinates)
        else:
            self.index[beacon["address"]].update(beacon)
        return True

    def clean(self, age = 5):
        for key in self.index:
            delta = (self.datetime.utcnow() - index[key].timestamps["timestamp"]).seconds
            if delta > int(age) * 60:
                self.index[key].close()
                del self.index[key]
        return True

    def output(self, request = ["alt", "away"]):
        ret = []
        for key in self.index:
            if self.index[key].categorys["alt"] = request[1]:
                ret.append(self.index[key])
        return ret

    def close(self):
        for key in self.index:
            self.index[key].close()
        return True
