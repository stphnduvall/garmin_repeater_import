#!/mnt/g/my_git/garmin_repeater_import/venv/bin/python
from sys import argv
import requests
import simplekml
import query_repeaters


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

    kml.save("test.kml")

# {'State ID': '13', 'Rptr ID': '77', 'Frequency': '147.19500', 'Input Freq': '147.79500', 'PL': '141.3', 'TSQ': '141.3',
# 'Lat': '30.70019640', 'Long': '-83.98794630', 'Callsign': 'W4UCJ', 'Use': 'OPEN', 'Operational Status':
# 'On-air', 'ARES': 'No', 'RACES': 'No', 'SKYWARN': 'No', 'CANWARN': 'No', 'IRLP Node': '0', 'Wires Node': '',
# 'FM Analog': 'Yes', 'DMR': 'No', 'DMR Color Code': '', 'DMR ID': '', 'D-Star': 'No', 'Last Update': '2022-10-14'}