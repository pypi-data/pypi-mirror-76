class WhoisError(Exception):
    def message(self):
        return self.args[0]
