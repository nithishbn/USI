
import requests
import Response 


class Spectrum(object):

    # directly takes an USI
    def __init__(self, usi):
        self.usi = usi.usi
        self.r = Response.Response()
        self.results = None
        self.name = None
        self.precursorMZ = None
        self.numPeaks = None
        self.peakList = None

    # fetches spectra information from specified source
    def fetch(self, source: str) -> Response:
        res = requests.get(
            "https://db.systemsbiology.net/dev2/sbeams/cgi/{source}/Spectrum?usi={usi}".format(source=source,
                                                                                               usi=self.usi))

        if res.status_code == 200:
            data = res.json()
            # spectrum json tag
            if(data["nErrors"]>0):
                print(data["message"])
                self.r.code = "ERROR"
            else:
                self.results = data["results"][0]["Spectrum"]

                # individual attributes from spectrum information
                self.name = self.results["Name"]
                self.precursorMZ = self.results["PrecursorMZ"]
                self.numPeaks = self.results["NumPeaks"]
                self.peakList = self.results["PeakList"]
                self.r.code = "OK"
        else:
            self.r.code = "ERROR"

        return self.r

    # prints out attributes
    def show(self):
        print("Name: {}".format(self.name))
        print("PrecursorMZ: {}".format(self.precursorMZ))
        print("USI: {}".format(self.usi))
        print("NumPeaks: {}".format(self.numPeaks))
        # for peak in self.peakList:
        #     for val in peak:
        #         print(val, end=" ")
        #     print()
