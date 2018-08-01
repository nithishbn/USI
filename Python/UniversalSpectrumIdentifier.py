#!/usr/bin/python3

import os
import sys
import json

class UniversalSpectrumIdentifier:

  #### Constructor
  def __init__(self):
    pass

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

  #### Define attribute usi
  @property
  def usi(self) -> str:
    return self._usi

  @usi.setter
  def usi(self, usi: str):
    self._usi = usi

  #### Define attribute datasetIdentifier
  @property
  def datasetIdentifier(self) -> str:
    return self._datasetIdentifier

  @datasetIdentifier.setter
  def datasetIdentifier(self, datasetIdentifier: str):
    self._datasetIdentifier = datasetIdentifier


  #### Define attribute datasetSubfolder
  @property
  def datasetSubfolder(self) -> str:
    return self._datasetSubfolder

  @datasetSubfolder.setter
  def datasetSubfolder(self, datasetSubfolder: str):
    self._datasetSubfolder = datasetSubfolder

# .... other attributes ...





  #### parser a usi string
  def parse(self,usi):
    print("INFO: Parsing USI string '"+usi+"'")





#### If this class is run from the command line, perform a short little test to see if it is working correctly
def main():

  testUSIs = [
    ["valid","mzspec:PXD002437:00261_A06_P001564_B00E_A00_R1:scan:10951"],
    ["valid","mzspec:PXD002437::00261_A06_P001564_B00E_A00_R1:scan:10951"],
    ["invalid","PXD002437::00261_A06_P001564_B00E_A00_R1:scan:10951"],
    ["valid","mzspec:PXD002437::00261_A06_P001564_B00E_A00_R1:scan:10951:PEPT[Phospho]IDELVISK/2"],
    ["invalid","mzspec:PASS002437::00261_A06_P001564_B00E_A00_R1:scan:10951:PEPT[Phospho]IDELVISK/2"],
    ["invalid","mzspec"],
    ["invalid","mzspec:"],
    ["invalid","mzspec:PXD001234"],
    ["invalid","mzspec:PXD001234:00261_A06_P001564_B00E_A00_R1:scan"],
    ["invalid","mzspec:PXD001234:00261_A06_P001564_B00E_A00_R1:index:10951"],
    ["valid","mzspec:PXD002437:00261_A06_P001564_B00E_A00_R1:scan:10951:PEPT[Phospho]IDELVISK/2"],
    ["valid","mzspec:PXD002437:00261_A06_P001564_B00E_A00_R1:scan:10951:PEPT[+79]IDELVISK/2"],
    ["valid","mzspec:PXD001234:Dilution1:4:scan:10951"],
    ["valid","mzspec:PXD002437::00261_A06_P001564_B00E_A00_R1:test1:scan:10951:PEPT[Phospho]IDELVISK/2"],
    ["valid","mzspec:PXD002437::00261_A06_P001564_B00E_A00_R1\\:test1:scan:10951:PEPT[Phospho]IDELVISK/2"],
  ]


  #### Loop over each test USI, parse it, and determine if it is valid or not, and print the index number
  print("Testing example USIs:")
  for usiSet in testUSIs:
    expectedStatus = usiSet[0]
    usiStr = usiSet[1]

    #### Create a new UniversalSpectrumIdentifier object
     usi = UniversalSpectrumIdentifier()
     response = usi.parse(usiStr)
     if response.status == "OK":
       print("Found index '"+usi.index'"+ from USI "+usiStr)
     else:
       print("ERROR: Invalid USI "+usiStr)

if __name__ == "__main__": main()
