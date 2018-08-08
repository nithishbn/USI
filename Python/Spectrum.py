from Python.Response import Response
import requests

class Spectrum(object):

    def __init__(self, usi):
        self.usi = usi

    def fetch(self, source: str) -> Response:
        requests.get()
        return Response()

    def show(self):
        pass
