from lxml import etree
from geopy import Point
from create_kml import create_rect_kml


class MyPoint(Point):
    def __str__(self):
        return f"{self.longitude},{self.latitude},{self.altitude}"
    def longlat(self):
        return self.longitude, self.latitude


class Rectangle():
    def __init__(self, p1:Point, p2:Point):
        self.p1: MyPoint = MyPoint(p1)
        self.p2: MyPoint = MyPoint(p2)
        self.x1 = p1[1]
        self.y1 = p1[0]
        self.x2 = p2[1]
        self.y2 = p2[0]
        self.missing_corners()

    def missing_corners(self):
        self.p3: MyPoint = MyPoint((self.y1, self.x2))
        self.p4: MyPoint = MyPoint((self.y2, self.x1))

    def __str__(self):
        points = [self.p1, self.p3, self.p2, self.p4]
        return " ".join(map(lambda point: str(point), points))

    def corners(self):
        points = [self.p1, self.p3, self.p2, self.p4]
        new_points = []
        for point in points:
            new_points.append(point.longlat())
        return new_points


def create_coords(coord: list[str]):
    """returns: (lat, lon)
    """
    a = coord.split(',')
    return Point(a[1], a[0], a[2])


def get_coords_from_kml(file):
    tree = etree.parse(file)
    root = tree.getroot()
    NAMESPACE = "{http://www.opengis.net/kml/2.2}%s"
    raw_coordinates = root.find(".//" + NAMESPACE % "coordinates").text.strip().split(" ")

    return list(map(create_coords, raw_coordinates))


if __name__ == "__main__":
    coords = get_coords_from_kml('Trip3.kml')
    rectangles = []
    for i in range(0, len(coords)-1):
        rectangles.append(Rectangle(coords[i], coords[i+1]))
    create_rect_kml(rectangles)
        # print(distance.distance(coords[i], coords[i+1]).mi)

