# Response class that can have a number of codes

class Response(object):

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code

    @property
    def message(self):
        return self._message
    @message.setter
    def message(self, message):
        self._message = message

    def __init__(self):
        self._code = "NEW"
        self._message = None
    
