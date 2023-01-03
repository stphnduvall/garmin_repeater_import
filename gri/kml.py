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


def create_rect_kml(rectangles, name=None):
    kml = simplekml.Kml()
    for rectangle in rectangles:
        rect = kml.newpolygon(name=name)
        rect.outerboundaryis = rectangle.corners()
        rect.polystyle.color = simplekml.Color.rgb(255, 255, 255, 128)

    kml.save(f'{name}.kml')


def create_track(points: list, name=None, description=None):
    kml = simplekml.Kml()
    kml.newlinestring(name=name, description=description, coords=points)
    kml.save(f"{name}.kml")


if __name__ == "__main__":
    from time import localtime
    import requests
    import repeaters

    state = "georgia"
    url = f'https://www.repeaterbook.com/api/export.php?country=United%20States&state={state}'
    response = requests.get(url).json()

    filter = {'Use': 'PRIVATE', 'Operational Status': "Off-air"}
    require = {"EchoLink Node": ["", "0"], "FM Analog": "Yes", "IRLP Node": ["", "0"], "Wires Node": ""}
    rptrs = repeaters.query_repeaters(response['results'][:-1], filter=filter, require=require)

    kml = createKML(rptrs)
    kml.save("repeaters" + "".join(map(str, localtime()[1:5])) + ".kml")
