#!/mnt/g/my_git/garmin_repeater_import/venv/bin/python
from sys import argv
import requests
import simplekml
import query_repeaters
from time import localtime


if __name__ == "__main__":
    kml = simplekml.Kml()

    state = "georgia"
    response = requests.get(f'https://www.repeaterbook.com/api/export.php?country=United%20States&state={state}').json()
    repeaters = response['results'][:-1]

    filter = {'Use': 'PRIVATE', 'Operational Status': "Off-air"}
    require = {"EchoLink Node": ["", "0"], "FM Analog": "Yes", "IRLP Node": ["", "0"], "Wires Node": ""}
    for repeater in query_repeaters.filter_repeaters(repeaters, filter=filter, require=require):
        if repeater.band not in ['2m', '70cm']:
            continue
        point = kml.newpoint(name=repeater.name())
        point.coords = [repeater.get_coords()]

        point.description = repeater.description()
        point.extendeddata.newdata('state', 'Georgia')

    kml.save("repeaters" + "".join(map(str, localtime()[1:5])) + ".kml")
