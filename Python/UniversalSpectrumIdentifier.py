import re
import Response
class UniversalSpectrumIdentifier(object):

    # usi object takes usiStr an automatically parses it and stores attributes
    # usi objects can still exist even if the usi str is incorrect.
    # it will simply show where the error in the string is
    def __init__(self, usi):
        # is there a better way to do this oh god

        self.valid = False
        self.usi = usi
        self.datasetIdentifier = None
        self.datasetSubfolder = None
        self.msRunName = None
        self.indexFlag = None
        self.index = None
        self.interpretation = None
        self.peptidoform = None
        self.charge = None
        self.provenanceIdentifier = None
        self.error = 0
        
        # parse out usi and store response
        
        

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

    # parses USI string
    def parse(self, verbose):
        r = Response.Response()
        print()
        verboseprint = print if verbose else lambda *a, **k: None
        verboseprint("\nINFO: Parsing USI string '" + self.usi + "'")
        elementOffset = 0
        offset = 0
        if self.usi.startswith("mzspec:"):
            self.usiMzspec = self.usi[len("mzspec:"):]
        else:
            self.error += 1
            verboseprint("ERROR: USI does not begin with prefix 'mszpec:'")
            r.code = "ERROR"
            return r

        # creates list of potential usi attributes
        elements = self.usiMzspec.split(":")
        nElements = len(elements)
        # print(elements)
        # print(nElements)

        # checks if usi has at least 4 colon-separated fields
        if nElements < 4:
            verboseprint("ERROR: USI does not have the minimum required 4 colon-separated fields after mzspec")
            self.error += 1
            r.code = "ERROR"
            return r
        offset = elementOffset

        # datasetIdentifier field
        self.datasetIdentifier = elements[offset]
        if self.datasetIdentifier is None:
            verboseprint("Dataset identifier is empty. Not permitted.")
            self.error += 1

        # this is the way it has been implemented now, but it can easily be changed to regex for other types of datasets
        elif self.datasetIdentifier.startswith("PXD"):
            self.datasetIdentifier = elements[offset]
            verboseprint("Dataset identifier is PXD compliant. Allowed.")
        else:
            verboseprint("Dataset identifier unknown. Not permitted.")
            self.error += 1
        elementOffset += 1
        offset = elementOffset
        nextField = elements[offset]
        offsetShift = 0
        # empty datasetsubfolder
        if nextField == '':
            verboseprint("old style. empty is ok. Empty datasetsubfolder probably.")
            offsetShift = 1

        offset = elementOffset + offsetShift
        self.msRunName = elements[offset]

        if self.msRunName:
            verboseprint("MS run equals " + self.msRunName)
        else:
            verboseprint("MS Run identifier empty. Not permitted.")
            self.error += 1

        elementOffset += 1
        offset = elementOffset + offsetShift
        self.indexFlag = elements[offset]
        # print("check " + self.indexFlag)
        # does indexFlag exist?
        if self.indexFlag:
            # is it scan or mgfi
            if self.indexFlag == "scan" or self.indexFlag == "mgfi":
                verboseprint("indexFlag is OK.")
            # is there potentially some weird colon escaping in the msRun name?
            else:
                potentialOffsetShift = offsetShift
                appendStr = ""
                repaired = False

                # fix colon escaping if it exists
                while elementOffset + potentialOffsetShift < nElements:
                    # go until program finds 'scan' or 'mgfi' index flag types
                    if elements[elementOffset + potentialOffsetShift].startswith("scan") or elements[
                        elementOffset + potentialOffsetShift].startswith(
                        "mgfi"):
                        self.indexFlag = elements[elementOffset + potentialOffsetShift]
                        self.msRunName += appendStr
                        offsetShift = potentialOffsetShift
                        repaired = True
                        break
                    appendStr += ":" + elements[elementOffset + potentialOffsetShift]

                    potentialOffsetShift += 1

                # colon escape fixed and msRun field updated
                if repaired:
                    verboseprint("Unescaped colon in msRun name. Hopefully taken care of. Please fix this")
                    verboseprint("msRun name revised to '{}'".format(self.msRunName))

                # no 'scan' or 'mgfi' fields found later. assume broken index flag
                else:
                    self.error += 1
                    verboseprint("Index type invalid. Must be 'scan' or 'mgfi'")
                    self.indexFlag = "ERROR"
                    r.code = "ERROR"
                    return r

        # no index flag
        else:
            self.error += 1
            verboseprint("Index flag empty! Not permitted.")
            self.indexFlag = "ERROR"
            r.code = "ERROR"
            return r
        elementOffset += 1
        offset = offsetShift + elementOffset

        # index for index flag if flag is valid. useless if index flag is invalid
        self.index = elements[offset]
        if self.index:
            verboseprint("Index is " + self.index)
        else:
            verboseprint("Index field empty. Not permitted.")
            self.error += 1

        elementOffset += 1
        offset = elementOffset + offsetShift

        # if statement check to see if the USI even has an interpretation field
        if offset < nElements:
            self.interpretation = elements[offset]
            self.peptidoform = ''
            self.charge = ''
            if self.interpretation and self.interpretation != '':
                find = re.match("^\s*(.+)\/(\d+)\s*$", self.interpretation)
                # match
                if find:
                    # subfields of interpretation
                    self.peptidoform = find.group(1)
                    self.charge = find.group(2)
                    verboseprint("Interpreted peptidoform = {}, charge = {}".format(self.peptidoform, self.charge))
                else:
                    verboseprint("Unable to parse interpretation {} as peptidoform/charge".format(self.interpretation))
            else:
                verboseprint("Interpretation field not provided. OK.")

        # provenance identifier
        if offset < nElements:
            self.provenanceIdentifier = elements[offset]
            print("Provenance Identifier = ".format(self.provenanceIdentifier))
        # returns count of errors found in usi. useful for checking if the entire identifier is valid.

        if self.error > 0:
            r.code = "ERROR"
        else:
            r.code = "OK"
        # no errors
        if r.code == "OK":
            print()
            print("Found index '" + self.index
                + "' from USI " + self.usi + "\n")
            # self.show()
            self.valid = True
        # errors found in usi
        else:
            print("Number of errors: " + str(self.error))
            self.valid = False
            print("ERROR: Invalid USI " + self.usi)
        print()

    # prints out USI attributes
    def show(self):
        print("USI: " + self.usi)
        print("Dataset Identifier: " + str(self.datasetIdentifier))
        print("Dataset Subfolder: " + str(self.datasetSubfolder))
        print("MS run name: " + str(self.msRunName))
        print("Index flag: " + str(self.indexFlag))
        print("Index: " + str(self.index))
        print("Peptido form: " + str(self.peptidoform))
        print("Charge: " + str(self.charge))


# If this class is run from the command line, perform a short little test to see if it is working correctly
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
    testUSIsValid = []
    # Loop over each test USI, parse it, and determine if it is valid or not, and print the index number
    print("Testing example USIs:")
    for usiSet in testUSIs:
        expectedStatus = usiSet[0]
        usiStr = usiSet[1]

        # Create a new UniversalSpectrumIdentifier object
        # made the USI object itself take a string so that parse does not need to be called explicitly
        usi = UniversalSpectrumIdentifier(usiStr)
        response = usi.valid
        testUSIsValid.append(response)
    # check to see if parsing is correct
    print(testUSIsValid)


# if __name__ == "__main__": main()
# inp = input("usi: ")
# usi = UniversalSpectrumIdentifier(inp)

# usi.parse(verbose=False)
# usi.show()
