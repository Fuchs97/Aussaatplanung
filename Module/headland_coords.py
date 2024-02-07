from shapely.geometry import Point, Polygon

def points_headland_area(polygon_headland, points):
    points_headland = []
    for point in points:
        # Punkt wird gespeichert, falls er sich innerhalb des Polygons befindet
        if polygon_headland.contains(point) or polygon_headland.touches(point) or polygon_headland.distance(point) < 1e-10:
            points.remove(point)
            points_headland.append(point)

    return points_headland, points

def points_headland_circ(polygon_inside, points):
    points_headland = []
    for point in points:
        # Punkt wird gespeichert, falls er sich innerhalb des Polygons befindet
        if polygon_inside.contains(point) or polygon_inside.touches(point) or polygon_inside.distance(point) < 1e-10:
            pass
        else:
            points.remove(point)
            points_headland.append(point)

    return points_headland, points

if __name__ == "__main__":
    #---------------- Parameter ------------------------------
    # Polygonkoordinaten
    polygon = Polygon([(1, 1), (4, 1), (6, 4), (1, 6)])