#!/mnt/g/my_git/garmin_repeater_import/venv/bin/python

class Repeater():
    def __init__(self, rptr):
        self.state_id = rptr['State ID']
        self.rptr_id = rptr['Rptr ID']
        self.frequency = float(rptr['Frequency'])
        self.input_frequency = float(rptr['Input Freq'])
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
        self.band = ''
        self.get_mode()

    def get_mode(self):
        mode = []
        if self.fm_analog == "Yes":
            mode.append("FM")
            if self.frequency > 144 and self.frequency < 148:
                self.band = "2m"
            elif self.frequency > 440 and self.frequency < 447:
                self.band = "70cm"
        if self.dmr == "Yes":
            mode.append("DMR")
        if self.d_star == "Yes":
            mode.append("D*")
        if self.system_fusion == "Yes":
            mode.append("YSF")
        self.mode = "/".join(mode)

    def get_coords(self):
        return (self.long, self.lat)

    def name(self):
        name = self.callsign + " " + (self.band if self.mode == 'FM' else self.mode)
        return name

    def description(self):
        desc = f"rx:{self.frequency}, tx:{self.input_frequency}, {self.pl}, {self.mode}\n{self.last_update}"
        return desc


def filter_repeaters(repeaters, filter={}, require={}):
    keys = [*repeaters[0].keys()]
    dumb_keys = [ 'Country', 'Nearest City', 'Landmark', 'County', 'State', 'Precise', 'AllStar Node', 'EchoLink Node',
        'NXDN', 'APCO P-25', 'P-25 NAC', 'Tetra', 'Tetra MCC', 'Tetra MNC', 'YSF DG ID Uplink',
        'YSF DG IS Downlink', 'YSF DSC', 'Use'
    ]

    filtered_repeaters = []
    for repeater in repeaters:
        required = True
        filtered = False
        for key in filter.keys():
            if type(filter[key]) == list:
                if repeater[key] in filter[key]:
                    filtered = True
            elif repeater[key] == filter[key]:
                filtered = True
        for key in require.keys():
            if type(require[key]) == list:
                if repeater[key] not in require[key]:
                    required = False
                    continue
            elif repeater[key] != require[key]:
                required = False

        # Gets rid of the shit keys I don't want.
        for dumb_key in dumb_keys:
            repeater.pop(dumb_key)
        if (required and not filtered): filtered_repeaters.append(Repeater(repeater))
    return filtered_repeaters


if __name__ == "__main__":
    from sys import argv
    import requests

    if len(argv) == 1:
        state = 'georgia'
    else:
        state = argv[1]

    response = requests.get(f'https://www.repeaterbook.com/api/export.php?country=United%20States&state={state}').json()
    repeaters = response['results'][:-1]

    # filter removes data with corresponding values
    filter = {'Use': 'PRIVATE', 'Operational Status': "Off-air"}
    # require ensures data has corresponding values
    require = {"EchoLink Node": ["", "0"], "FM Analog": "Yes", "IRLP Node": ["", "0"], "Wires Node": ""}
    for repeater in filter_repeaters(repeaters, filter=filter, require=require):
        print(repeater.callsign)
