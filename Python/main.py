from Python.Spectrum import Spectrum
from Python.UniversalSpectrumIdentifier import UniversalSpectrumIdentifier

usi = UniversalSpectrumIdentifier()

response = usi.parse("mzspec:PXD000561::Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555:VLHPLEGAVVIIFK/2")

if response.code == 'OK':

    spectrum = Spectrum()

    spectrum.USI = usi

    resp = spectrum.fetch('PeptideAtlas')

    if resp.code == 'OK':

        spectrum.show()

    else:
        response.show()
