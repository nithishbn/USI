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

            self.results = data["results"][0]["Spectrum"]
            self.r.code = "OK"
        else:
            self.r.code = "ERROR"

        return self.r

    def show(self):
        print("Name: {}".format(self.results["Name"]))
        print("PrecursorMZ: {}".format(self.results["PrecursorMZ"]))
        print("USI: {}".format(self.results["USI"]))
        print("NumPeaks: {}".format(self.results["NumPeaks"]))
        for peak in self.results["PeakList"]:
            for val in peak:
                print(val, end=" ")
            print()

