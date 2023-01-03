#!/mnt/g/my_git/garmin_repeater_import/venv/bin/python
import requests
from time import localtime
from repeaters import query_repeaters
from kml import createKML

if __name__ == "__main__":
    state = "georgia"
    url = f'https://www.repeaterbook.com/api/export.php?country=United%20States&state={state}'
    response = requests.get(url).json()

    filter = {'Use': 'PRIVATE', 'Operational Status': "Off-air"}
    require = {"EchoLink Node": ["", "0"], "FM Analog": "Yes", "IRLP Node": ["", "0"], "Wires Node": ""}
    rptrs = query_repeaters(response['results'][:-1], filter=filter, require=require)

    kml = createKML(rptrs)

    kml.save("repeaters" + "".join(map(str, localtime()[1:5])) + ".kml")
