from pyteomics.mass import Unimod

modTest = Unimod(source="http://www.unimod.org/xml/unimod.xml")
print(modTest.by_title("Phospho"))
