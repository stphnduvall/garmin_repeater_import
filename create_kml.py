#!/mnt/g/my_git/garmin_repeater_import/venv/bin/python
import simplekml


def createKML(repeaters):
    kml = simplekml.Kml()
    for repeater in repeaters:
        if repeater.band not in ['2m', '70cm']:
            continue
        point = kml.newpoint(name=repeater.name())
        point.coords = [repeater.get_coords()]

        point.description = repeater.description()
        point.extendeddata.newdata('state', 'Georgia')
    return kml


if __name__ == "__main__":
    from time import localtime
    import requests
    import query_repeaters

    state = "georgia"
    url = f'https://www.repeaterbook.com/api/export.php?country=United%20States&state={state}'
    response = requests.get(url).json()

    filter = {'Use': 'PRIVATE', 'Operational Status': "Off-air"}
    require = {"EchoLink Node": ["", "0"], "FM Analog": "Yes", "IRLP Node": ["", "0"], "Wires Node": ""}
    repeaters = query_repeaters.filter_repeaters(response['results'][:-1], filter=filter, require=require)

    kml = createKML(repeaters)
    kml.save("repeaters" + "".join(map(str, localtime()[1:5])) + ".kml")
