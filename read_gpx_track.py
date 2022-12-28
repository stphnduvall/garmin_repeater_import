import gpxpy
import gpxpy.gpx
from geopy.distance import lonlat, distance
from geopy.units import rad, degrees
from create_kml import create_track, create_rect_kml
from math import sin, cos, sqrt, asin, acos, atan2

def mile_divisions(segment: gpxpy.gpx.GPXTrackSegment):
    total_distance = 0.0
    cur_distance = 0.0
    mile_markers = []
    for p in range(0, len(segment.points) - 1):
        pt_distance = distance(lonlat(segment.points[p].longitude, segment.points[p].latitude), lonlat(segment.points[p+1].longitude, segment.points[p+1].latitude)).miles
        cur_distance += pt_distance
        total_distance += pt_distance

        if cur_distance > 5:
            mile_markers.append((segment.points[p+1].longitude, segment.points[p+1].latitude))
            cur_distance = 0.0

    test = []
    for i in range(1, len(mile_markers)-1):
        del1 = rad(mile_markers[i-1][0])
        phi1 = rad(mile_markers[i-1][1])
        del2 = rad(mile_markers[i+1][0])
        phi2 = rad(mile_markers[i+1][1])
        deltadel = del2 - del1

        bx = cos(phi2) * cos(deltadel)
        by = cos(phi2) * sin(deltadel)

        phi3 = atan2(sin(phi1) + sin(phi2), sqrt((cos(phi1) + bx)**2 + by**2))
        del3 = del1 + atan2(by, cos(phi1) + bx)

        test.append((degrees(del3), degrees(phi3)))
        print(degrees(del3), degrees(phi3))

    create_track(test, name="Testing midpoint")
    create_track(mile_markers, name="5mile line")


if __name__ == "__main__":
    gpx_file = open('Work Trips.gpx', 'r')
    gpx = gpxpy.parse(gpx_file)

    mile_divisions(gpx.tracks[0].segments[0])
    # new_track = gpxpy.gpx.GPXTrack()
    # new_segment = gpxpy.gpx.GPXTrackSegment()

    # for i in range(0, len(gpx.tracks[0].segments[0].points), 10):
    #     new_segment.points.append(gpx.tracks[0].segments[0].points[i])
    # new_track.segments.append(new_segment)
    # new_track.name = "10pt avg"
    # gpx.tracks.append(new_track)

    # print(gpx.to_xml(version="1.0"))