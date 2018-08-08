class Response(object):


    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code
