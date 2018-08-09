# Response class that can have a number of codes

class Response(object):

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code

    def __init__(self):
        self._code = "NEW"
