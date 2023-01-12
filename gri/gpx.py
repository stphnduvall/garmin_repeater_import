from math import sin, cos, sqrt, asin, acos, atan2
import gpxpy
import gpxpy.gpx
from geopy.distance import lonlat, distance, Distance
from geopy.units import rad, degrees
from geopy import Point

from kml import create_track, create_tracks, Line


def n_mile_divisions(segment: gpxpy.gpx.GPXTrackSegment, n_miles=1):
    total_distance = 0.0
    current_distance = 0.0
    n_mile_markers = []

    for i in range(0, len(segment.points) - 1):
        p1 = (segment.points[i].latitude, segment.points[i].longitude)
        p2 = (segment.points[i+1].latitude, segment.points[i+1].longitude)
        pt_distance = distance(p1, p2).miles
        current_distance += pt_distance
        total_distance += pt_distance

        if current_distance > n_miles:
            n_mile_markers.append(segment.points[i+1])
            current_distance = 0.0
    return n_mile_markers


def calculate_midpoint(point1, point2):
    """
    Parameters:
    point1 (gpxpy.gpx.GPXTrackPoint)
    point2 (gpxpy.gpx.GPXTrackPoint)

    Returns:
    midpoint (Point)
    """
    del1 = rad(point1.longitude)
    phi1 = rad(point1.latitude)
    del2 = rad(point2.longitude)
    phi2 = rad(point2.latitude)
    deltadel = del2 - del1

    bx = cos(phi2) * cos(deltadel)
    by = cos(phi2) * sin(deltadel)

    phi3 = atan2(sin(phi1) + sin(phi2), sqrt((cos(phi1) + bx)**2 + by**2))
    del3 = del1 + atan2(by, cos(phi1) + bx)

    # return (degrees(del3), degrees(phi3)) # Convert to gpxpy point
    return Point(degrees(phi3), degrees(del3))


def calculate_bearing(point1, point2):
    """
    Parameters:
    point1 (gpxpy.gpx.GPXTrackPoint): Point on original line
    point2 (Point): Calculated midpoint

    Returns:
    A bearing from point1 to point2 in degrees
    """
    phi1 = point2.latitude
    del1 = point2.longitude
    phi2 = point1.latitude
    del2 = point1.longitude
    deltadel = del2 - del1

    bearing = atan2(sin(deltadel) * cos(phi2), cos(phi1)*sin(phi2)-sin(phi1)*cos(phi2)*cos(deltadel))

    return degrees(bearing)


def calculate_projection(point: gpxpy.gpx.GPXTrackPoint, bearing: float, di: float) -> Point:
    geopoint = Point(point.latitude, point.longitude)
    projection = distance(miles=di).destination(point=geopoint, bearing=bearing)
    return projection


def outline_track(track: gpxpy.gpx.GPXTrack):
    ...


def create_gpx(repeaters):
    gpx = gpxpy.gpx.GPX()
    for repeater in repeaters:
        if repeater.band not in ['2m', '70cm']:
            continue

        waypoint = gpxpy.gpx.GPXWaypoint(repeater.lat, repeater.long)
        waypoint.name = repeater.name()
        waypoint.description = " ".join(repeater.description())
        waypoint.symbol = 'Custom 1'

        if repeater.dmr == "Yes":
            waypoint.symbol = 'Custom 2'

        gpx.waypoints.append(waypoint)

    return gpx


if __name__ == "__main__":
    # import requests
    # from repeaters import query_repeaters

    # state = "georgia"
    # url = f'https://www.repeaterbook.com/api/export.php?country=United%20States&state={state}'
    # response = requests.get(url).json()

    # filter = {'Use': 'PRIVATE', 'Operational Status': "Off-air"}
    # require = {"EchoLink Node": ["", "0"], "FM Analog": "Yes", "IRLP Node": ["", "0"], "Wires Node": ""}
    # repeater_data = query_repeaters(response['results'][:-1], filter=filter, require=require)

    # gpx = create_gpx(repeater_data)
    # print(gpx.to_xml())

    gpx_file = open('data/Work Trips.gpx', 'r')
    gpx = gpxpy.parse(gpx_file)

    points = n_mile_divisions(gpx.tracks[0].segments[0], 5)
    midpoints = []
    projection1 = []
    projection2 = []
    bearing = 0
    bearings = []
    proj1 = True
    for i in range(1, len(points) - 1):
        midpoint = calculate_midpoint(points[i-1], points[i+1])
        midpoints.append(midpoint)

        last_bearing = bearing
        bearing = calculate_bearing(points[i], midpoint)
        if ((bearing - last_bearing) > 0):
            proj1 = not(proj1)

        print(proj1, f"{abs(bearing)} - {abs(last_bearing)} = |{abs(abs(bearing)-abs(last_bearing))}|")
        projection = calculate_projection(points[i], bearing, 5)

        if proj1:
            projection1.append((projection.longitude, projection.latitude))
            bearings.append([(midpoint.longitude, midpoint.latitude), (points[i].longitude, points[i].latitude)])
            bearings.append([(midpoint.longitude, midpoint.latitude), (projection.longitude, projection.latitude)])
            bearings.append([(points[i].longitude, points[i].latitude), (projection.longitude, projection.latitude)])
        else:
            projection2.append((projection.longitude, projection.latitude))
            bearings.append([(midpoint.longitude, midpoint.latitude), (points[i].longitude, points[i].latitude)])
            bearings.append([(midpoint.longitude, midpoint.latitude), (projection.longitude, projection.latitude)])
            bearings.append([(points[i].longitude, points[i].latitude), (projection.longitude, projection.latitude)])

    # create_track(name="data/Projection1", description="", points=projection1)
    # create_track(name="data/Projection2", description="", points=projection2)
    tracks = [{'points': projection1, 'name': "Projection1", 'description': ''},
              {'points': projection2, 'name': "Projection2", 'description': ''}]
    for bearing_line in bearings:
        tracks.append({'points': bearing_line, 'name': 'Bearing line', 'description': ''})

    create_tracks(tracks, "data/Projections")
