
from shapely.geometry import Point, Polygon
import shapely.wkt
from pyproj import Proj, Transformer, CRS
def geo_to_utm(coordinates, utm_zone):
    # Definiere die Parameter für das projizierte Koordinatensystem (ETRS89)
    proj_params = {
        'proj': 'utm',
        'zone': utm_zone,
        'ellps': 'GRS80',  # Das ETRS89-Referenzsystem verwendet das GRS80-Ellipsoid
        'units': 'm',
        'type': 'crs'
    }

    # Erstelle das projizierte Koordinatensystem
    projected_crs = Proj(proj_params)

    # Initialisiere leere Liste für die projizierten Koordinaten
    projected_coordinates = []

    # Transformiere Geo-Koordinaten in projizierte Koordinaten für jedes Paar
    for lon, lat in coordinates:
        x, y = projected_crs(lon, lat)
        projected_coordinates.append((x, y))

    return projected_coordinates

def utm_to_geo_points(input, utm_zone):
    # Definiere das UTM-Koordinatensystem
    utm_crs_params = {
        'proj': 'utm',
        'zone': utm_zone,
        'ellps': 'GRS80',
        'units': 'm'
    }
    utm_crs = CRS(utm_crs_params)

    # Initialisiere leere Liste für die geographischen Koordinaten
    geo_coordinates = []

    # Transformiere projizierte Koordinaten zurück in Geo-Koordinaten
    transformer = Transformer.from_crs(utm_crs, "EPSG:4326", always_xy=True)

    if isinstance(input, list):
        for point in input:
            # Wenn das Feature ein Punkt ist
            x, y = point.x, point.y
            # Transformiere die Koordinaten zurück in Geo-Koordinaten
            lon_back, lat_back = transformer.transform(x, y)
            # Erstelle ein Point-Objekt für die Geo-Koordinaten und füge es zur Liste hinzu
            geo_coordinates.append(Point(lon_back, lat_back))
    else:
        print("Input ist nicht vom Typen Point")
    return geo_coordinates

def utm_to_geo_polygon(utm_polygon, utm_zone):
    # Definiere das UTM-Koordinatensystem
    utm_crs_params = {
        'proj': 'utm',
        'zone': utm_zone,
        'ellps': 'GRS80',
        'units': 'm'
    }
    utm_crs = CRS(utm_crs_params)

    # Transformiere projizierte Koordinaten zurück in Geo-Koordinaten
    transformer = Transformer.from_crs(utm_crs, "EPSG:4326", always_xy=True)

    def transform_coordinates(utm_coords):
        lon, lat = transformer.transform(utm_coords[0], utm_coords[1])
        return lon, lat

    utm_polygon = shapely.wkt.loads(utm_polygon)
    geographic_polygon = Polygon([transform_coordinates(coord) for coord in utm_polygon.exterior.coords])

    return geographic_polygon

def get_utm_zone(coords_geo):
    # Entnehme den Längengrad der ersten Koordinate
    lon = coords_geo[0][0]

    # Eine UTM-Zone umfasst 6 Grad Längengrad
    utm_zone = int((lon + 180) / 6) + 1

    return utm_zone

# Testcode
if __name__ == "__main__":
    # Beispielhafte Liste von Punkten im utm-KGS
    utm_points = [
        Point(2000000, 1000000),
        Point(2100000, 1100000),
        Point(2200000, 1200000),
        Point(2300000, 1300000),
        Point(2400000, 1400000),
    ]
    coords = [(10.590081, 51.0777842), (10.5898449, 51.0777573), (10.589081, 51.0777842), (10.5908449, 51.0777573)]
    polygon = Polygon(utm_points)

    utm_zone = get_utm_zone(coords)

    coords_geo = utm_to_geo_points(utm_points, utm_zone)
    print(f"Zurücktransformierte Koordinaten in geographische Koordinaten: {coords_geo}")

    coords = geo_to_utm(coords, utm_zone)

   # coords_geo2 = utm_to_geo_polygon(polygon, utm_zone)
    #print(f"Zurücktransformierte Koordinaten in geographische Koordinaten: {coords_geo2}")




