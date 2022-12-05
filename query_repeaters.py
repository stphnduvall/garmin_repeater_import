#!/mnt/g/my_git/garmin_repeater_import/venv/bin/python
from sys import argv
import requests


def filter_repeaters(repeaters, filter={}, require={}):
    keys = [*repeaters[0].keys()]
    dumb_keys = [ 'Country', 'Nearest City', 'Landmark', 'County', 'State', 'Precise', 'AllStar Node', 'EchoLink Node',
        'NXDN', 'APCO P-25', 'P-25 NAC', 'Tetra', 'Tetra MCC', 'Tetra MNC', 'System Fusion', 'YSF DG ID Uplink',
        'YSF DG IS Downlink', 'YSF DSC'
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
        i = 0
        for key in require.keys():
            i += 1
            if type(require[key]) == list:
                if repeater[key] not in require[key]:
                    required = False
                    continue
            elif repeater[key] != require[key]:
                required = False

        # Gets rid of the shit keys I don't want.
        for dumb_key in dumb_keys:
            repeater.pop(dumb_key)
        if (required and not filtered): filtered_repeaters.append(repeater)
    return filtered_repeaters


if __name__ == "__main__":
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
        print(repeater)
