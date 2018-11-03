# import json

from xmltodict import parse
import requests
from json import dumps, loads

id = input("ID: ")
response = requests.get(
    "http://proteomecentral.proteomexchange.org/cgi/GetDataset?ID={id}&outputMode=XML".format(id=id))
if response.status_code == 200:
    data = parse(response.text)
    jsonData = dumps(data)
    print(dumps(loads(jsonData), indent=4, sort_keys=True))
print("Done")
