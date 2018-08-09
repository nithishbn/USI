from Python.Response import Response
import requests


class Spectrum(object):

    # directly takes an USI
    def __init__(self, usi):
        self.usi = usi.usi
        self.r = Response()
        self.results = None

    # fetches spectra information from specified source
    def fetch(self, source: str) -> Response:
        res = requests.get(
            "https://db.systemsbiology.net/dev2/sbeams/cgi/{source}/Spectrum?usi={usi}".format(source=source,
                                                                                               usi=self.usi))

        if res.status_code == 200:
            data = res.json()
            self.results = data["results"]
            self.r.code = "OK"
        else:
            self.r.code("ERROR")

        return self.r

    def show(self):
        print(self.results[0])
        for i in self.results[0]["Spectrum"]["PeakList"]:
            print(i)
