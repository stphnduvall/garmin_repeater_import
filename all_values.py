#!/mnt/g/my_git/garmin_repeater_import/venv/bin/python
import requests
from sys import argv

def list_values(repeaters, key):
    values = []
    for repeater in repeaters:
        if key in repeater.keys():
            if repeater[key] not in values:
                values.append(repeater[key])
    return values

if __name__ == "__main__":
    state = 'georgia'
    response = requests.get(f'https://www.repeaterbook.com/api/export.php?country=United%20States&state={state}').json()
    repeaters = response['results'][:-1]

    if len(argv) > 1:
        for arg in argv[1:]:
            print(f'All values for the key: {arg}')
            print(*[f"\t{i}\n" for i in list_values(repeaters, arg)])