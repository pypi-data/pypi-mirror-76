import shapefile as shp
from shapely.geometry import mapping
import sys


def set_geometry(geometry):
    """
    Determine the geometry to write based on its mapped type from shapely

    :param geometry: A shapely geometry type
    :return: The coordinates to write into the pyshp's shapefile
    """
    mapped = mapping(geometry)

    if mapped["type"] == "Polygon":
        return [part for part in mapped["coordinates"]]
    elif mapped["type"] == "MultiPolygon":
        return [part for polygon in mapped["coordinates"] for part in polygon]
    else:
        sys.exit(f"Sorry: {mapped['type']} not currently writeable")


def write_shape_file(write_directory, file_name, headers, write_geometry, write_records):
    """
    This takes a set of shapely geometry and writes it to a shapefile at a given directory with the name file_name
    """

    # TODO We need to allow for field types but this is leading to byte errors.
    shape_file = shp.Writer(f"{write_directory}/{file_name}")
    [shape_file.field(field) for field in headers]

    for geo, rec in zip(write_geometry, write_records):
        # Need the asterisk to determine that it is a list rather than a dict or a string set of inputs
        shape_file.record(*rec)
        shape_file.poly(set_geometry(geo))