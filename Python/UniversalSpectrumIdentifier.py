#!/usr/bin/python3

import os
import sys
import json


class UniversalSpectrumIdentifier:

    #### Constructor
    def __init__(self):
        # is there a better way to do this oh god
        self.usi = None
        self.datasetIdentifier = None
        self.datasetSubfolder = None
        self.msRunName = None
        self.indexFlag = None
        self.index = None
        self.interpretation = None
        self.peptidoform = None
        self.charge = None

    #### Destructor
    def __del__(self):
        pass

    # Attributes:
    #   usi
    #   datasetIdentifier
    #   datasetSubfolder
    #   msRunName
    #   indexFlag
    #   index
    #   interpretation
    #   peptidoform
    #   charge

    #### parser a usi string
    def parse(self, usi):
        print("INFO: Parsing USI string '" + usi + "'")
        elementOffset = 0
        offset = 0
        if usi:
            self.usi(usi)
        else:
            print("ERROR: No USI provided")
            return "error"
        if usi.startswith("mzspec:"):
            self.usi(usi[len("mzspec")])
        elements = self.usi.split(":")
        nElements = len(elements)
        print(elements)
        print(nElements)
        if nElements < 4:
            print("ERROR: USI does not have the minimum required 4 colon-separated fields after mzspec")
            return "error"
        if elements[offset] is None:
            print("Dataset identifier is empty. Not permitted.")
        elif elements[offset].startswith("PXD"):
            self.datasetIdentifier = elements[offset]
            print("Dataset identifier is PXD compliant. Allowed.")
        else:
            print("Dataset identifier unknown. Not permitted.")
        offset += 1
        offsetShift = 0
        if elements[offset] == '':
            print("old style. empty is ok.")
            offsetShift = 1
        offset += offsetShift
        if elements[offset]:
            self.msRunName = elements[offset]
            print("MS run equals " + self.msRunName)

        offset += 1
        if elements[offset] == "scan" or "mgfi":
            print("indexFlag is OK.")
            self.indexFlag = elements[offset]
        else:
            potentialOffsetShift = 1
            appendStr = "";
            repaired = False
            while offset + offsetShift <= nElements:
                if elements[offset + offsetShift].startsWith("scan" or "mgfi"):
                    self.indexFlag = elements[offset + offsetShift]
                    self.msRunName += appendStr
                    repaired = True
                appendStr += ":" + elements[offset + offsetShift];
                offsetShift += 1
        return "OK"


#### If this class is run from the command line, perform a short little test to see if it is working correctly
def main():
    testUSIs = [
        ["valid", "mzspec:PXD002437:00261_A06_P001564_B00E_A00_R1:scan:10951"],
        ["valid", "mzspec:PXD002437::00261_A06_P001564_B00E_A00_R1:scan:10951"],
        ["invalid", "PXD002437::00261_A06_P001564_B00E_A00_R1:scan:10951"],
        ["valid", "mzspec:PXD002437::00261_A06_P001564_B00E_A00_R1:scan:10951:PEPT[Phospho]IDELVISK/2"],
        ["invalid", "mzspec:PASS002437::00261_A06_P001564_B00E_A00_R1:scan:10951:PEPT[Phospho]IDELVISK/2"],
        ["invalid", "mzspec"],
        ["invalid", "mzspec:"],
        ["invalid", "mzspec:PXD001234"],
        ["invalid", "mzspec:PXD001234:00261_A06_P001564_B00E_A00_R1:scan"],
        ["invalid", "mzspec:PXD001234:00261_A06_P001564_B00E_A00_R1:index:10951"],
        ["valid", "mzspec:PXD002437:00261_A06_P001564_B00E_A00_R1:scan:10951:PEPT[Phospho]IDELVISK/2"],
        ["valid", "mzspec:PXD002437:00261_A06_P001564_B00E_A00_R1:scan:10951:PEPT[+79]IDELVISK/2"],
        ["valid", "mzspec:PXD001234:Dilution1:4:scan:10951"],
        ["valid", "mzspec:PXD002437::00261_A06_P001564_B00E_A00_R1:test1:scan:10951:PEPT[Phospho]IDELVISK/2"],
        ["valid", "mzspec:PXD002437::00261_A06_P001564_B00E_A00_R1\\:test1:scan:10951:PEPT[Phospho]IDELVISK/2"],
    ]

    #### Loop over each test USI, parse it, and determine if it is valid or not, and print the index number
    print("Testing example USIs:")
    for usiSet in testUSIs:
        expectedStatus = usiSet[0]
        usiStr = usiSet[1]

        #### Create a new UniversalSpectrumIdentifier object
        usi = UniversalSpectrumIdentifier()
        response = usi.parse(usiStr)
        if response == "OK":
            print("Found index '" + usi.index
                  + "' from USI " + usiStr)
        else:
            print("ERROR: Invalid USI " + usiStr)


if __name__ == "__main__": main()
