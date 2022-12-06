import gpxpy
import gpxpy.gpx
import query_repeaters


def create_gpx(repeaters):
    gpx = gpxpy.gpx.GPX()
    for repeater in repeaters:
        if repeater.band not in ['2m', '70cm']:
            continue

        waypoint = gpxpy.gpx.GPXWaypoint(repeater.lat, repeater.long)
        waypoint.name = repeater.name()
        waypoint.description = repeater.description()
        waypoint.symbol = 'Custom 1'

        gpx.waypoints.append(waypoint)

    return gpx


if __name__ == "__main__":
    import requests
    state = "georgia"
    response = requests.get(f'https://www.repeaterbook.com/api/export.php?country=United%20States&state={state}').json()

    filter = {'Use': 'PRIVATE', 'Operational Status': "Off-air"}
    require = {"EchoLink Node": ["", "0"], "FM Analog": "Yes", "IRLP Node": ["", "0"], "Wires Node": ""}
    repeater_data = query_repeaters.filter_repeaters(response['results'][:-1], filter=filter, require=require)

    gpx = create_gpx(repeater_data)
    print(gpx.to_xml())
