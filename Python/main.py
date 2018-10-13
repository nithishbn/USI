from Spectrum import Spectrum
from UniversalSpectrumIdentifier import UniversalSpectrumIdentifier

# USI created
usi = UniversalSpectrumIdentifier("asdf:PXD000561::Adult_Frontalcortex_bRP_Elite_85_f09:scan:17555:VLHPLEGAVVIIFK/2")
# usi = UniversalSpectrumIdentifier("mzspec:PXD002437:00261_A06_P001564_B00E_A00_R1:scan:10951:PEPT[Phospho]IDELVISK/2")
# usi = UniversalSpectrumIdentifier("mzspec:PXD005712::20152002_RG_150218_Saita_Ctrl_3XXXXX:scan:5748:AVAAVAATGPASAPGPGGGR/2")
usi.parse(verbose=False)
# if the USI is okay then create a spectrum class to fetch from the online database
if usi.valid:
    # spectrum class just takes in a USI
    spectrum = Spectrum(usi)
    # fetches the USI from the PeptideAtlas database or whatever database is specified
    resp = spectrum.fetch('PeptideAtlas')
    print(resp.code)
    if resp.code == 'OK':
        spectrum.show()
    

        
