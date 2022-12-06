#!/mnt/g/my_git/garmin_repeater_import/venv/bin/python
from sys import argv
import requests
import simplekml
import query_repeaters


class Repeater():
    def __init__(self, rptr):
        self.state_id = rptr['State ID']
        self.rptr_id = rptr['Rptr ID']
        self.frequency = rptr['Frequency']
        self.input_frequency = rptr['Input Freq']
        self.pl = rptr['PL']
        self.tsq = rptr['TSQ']
        self.lat = rptr['Lat']
        self.long = rptr['Long']
        self.callsign = rptr['Callsign']
        self.operational_status = rptr['Operational Status']
        self.ares = rptr['ARES']
        self.races = rptr['RACES']
        self.skywarn = rptr['SKYWARN']
        self.canwarn = rptr['CANWARN']
        self.irlp_node = rptr['IRLP Node']
        self.wires_node = rptr['Wires Node']
        self.fm_analog = rptr['FM Analog']
        self.dmr = rptr['DMR']
        self.dmr_color_code = rptr['DMR Color Code']
        self.dmr_id = rptr['DMR ID']
        self.d_star = rptr['D-Star']
        self.system_fusion = rptr['System Fusion']
        self.last_update = rptr['Last Update']
        self.get_mode()

    def get_mode(self):
        mode = []
        if self.fm_analog == "Yes":
            mode.append("FM")
        if self.dmr == "Yes":
            mode.append("DMR")
        if self.d_star == "Yes":
            mode.append("D*")
        if self.system_fusion == "Yes":
            mode.append("YSF")
        self.mode = "/".join(mode)

    def get_coords(self):
        return (self.long, self.lat)
    # {'State ID': '13', 'Rptr ID': '13942', 'Frequency': '53.05000', 'Input Freq': '52.05000', 'PL': '100.0', 'TSQ': '',
    #  'Lat': '34.52992280', 'Long': '-84.33909230', 'Callsign': 'KC4JNN', 'Use': 'OPEN', 'Operational Status': 'On-air', 'ARES': 'No',
    #  'RACES': 'No', 'SKYWARN': 'No', 'CANWARN': 'No', 'IRLP Node': '0', 'Wires Node': '', 'FM Analog': 'Yes',
    #  'DMR': 'No', 'DMR Color Code': '', 'DMR ID': '', 'D-Star': 'No', 'System Fusion': 'No', 'Last Update': '2022-10-11'}

    # 'FM Analog': 'Yes', 'DMR': 'No', 'DMR Color Code': '', 'DMR ID': '', 'D-Star': 'No', 'System Fusion': 'No',



if __name__ == "__main__":
    kml = simplekml.Kml()

    state = "georgia"
    response = requests.get(f'https://www.repeaterbook.com/api/export.php?country=United%20States&state={state}').json()
    repeaters = response['results'][:-1]

    filter = {'Use': 'PRIVATE', 'Operational Status': "Off-air"}
    require = {"EchoLink Node": ["", "0"], "FM Analog": "Yes", "IRLP Node": ["", "0"], "Wires Node": ""}
    for rptr in query_repeaters.filter_repeaters(repeaters, filter=filter, require=require):
        repeater = Repeater(rptr)
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