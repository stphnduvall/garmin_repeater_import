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
    for rptr in query_repeaters.filter_repeaters(repeaters, filter=filter, require=require):
        repeater = query_repeaters.Repeater(rptr)
        point = kml.newpoint(name=repeater.callsign)
        point.coords = [repeater.get_coords()]

        rx = repeater.frequency
        tx = repeater.input_frequency
        uplink = repeater.pl
        mode = repeater.mode
        last_update = repeater.last_update

        point.description = f"rx: {rx}, tx: {tx}, {uplink}, {mode}, {last_update}"

    print(kml.allfeatures)

    kml.save("test.kml")

# {'State ID': '13', 'Rptr ID': '77', 'Frequency': '147.19500', 'Input Freq': '147.79500', 'PL': '141.3', 'TSQ': '141.3',
# 'Lat': '30.70019640', 'Long': '-83.98794630', 'Callsign': 'W4UCJ', 'Use': 'OPEN', 'Operational Status':
# 'On-air', 'ARES': 'No', 'RACES': 'No', 'SKYWARN': 'No', 'CANWARN': 'No', 'IRLP Node': '0', 'Wires Node': '',
# 'FM Analog': 'Yes', 'DMR': 'No', 'DMR Color Code': '', 'DMR ID': '', 'D-Star': 'No', 'Last Update': '2022-10-14'}