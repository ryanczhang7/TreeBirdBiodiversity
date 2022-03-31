from shapely.geometry import Polygon
import math
import geopandas as gpd

"""
I did not write this code. This code was sourced from github and stackoverflow
https://wsdookadr.github.io/posts/p4/
https://gis.stackexchange.com/questions/341218/creating-a-hexagonal-grid-of-regular-hexagons-of-definite-area-anywhere-on-the-g
"""


def create_hex_centers(x_min, y_min, x_max, y_max, side):
    """
    returns an array of Points describing hexagons centers that are inside the given bounding_box
    :param y_max: max y-coordinate from the boundary
    :param x_max: max x-coordinate from the boundary
    :param y_min: min y-coordinate from the boundary
    :param x_min: min x-coordinate from the boundary
    :param side: The size of the hexagons'
    :return: The hexagon grid
    """
    grid = []

    v_step = math.sqrt(3) * side
    h_step = 1.5 * side

    h_skip = math.ceil(x_min / h_step) - 1
    h_start = h_skip * h_step

    v_skip = math.ceil(y_min / v_step) - 1
    v_start = v_skip * v_step

    h_end = x_max + h_step
    v_end = y_max + v_step

    if v_start - (v_step / 2.0) < y_min:
        v_start_array = [v_start + (v_step / 2.0), v_start]
    else:
        v_start_array = [v_start - (v_step / 2.0), v_start]

    v_start_idx = int(abs(h_skip) % 2)

    c_x = h_start
    c_y = v_start_array[v_start_idx]
    v_start_idx = (v_start_idx + 1) % 2
    while c_x < h_end:
        while c_y < v_end:
            grid.append((c_x, c_y))
            c_y += v_step
        c_x += h_step
        c_y = v_start_array[v_start_idx]
        v_start_idx = (v_start_idx + 1) % 2

    return grid


def create_hexagon(length, x, y):
    """
    Create a hexagon centered on (x, y)
    :param length: length of the hexagon's edge
    :param x: x-coordinate of the hexagon's center
    :param y: y-coordinate of the hexagon's center
    :return: The polygon containing the hexagon's coordinates
    """
    c = [[x + math.cos(math.radians(angle)) * length,
          y + math.sin(math.radians(angle)) * length] for angle in range(0, 360, 60)]
    return Polygon(c)


def create_hexgrid(side, polygon_boundary):
    """
    Create a hexagon grid over a given polygon
    :param side: length of the hexagon's edge
    :param polygon_boundary: a single polygon that defines the outer boundaries
    :return: A geodataframe of the hexagon grid
    """
    x_min, y_min, x_max, y_max = polygon_boundary.total_bounds
    hexagon_centers = create_hex_centers(x_min, y_min, x_max, y_max, side)
    grid_cells = []
    for center in hexagon_centers:
        new_cell = create_hexagon(side, center[0], center[1])
        if new_cell.intersects(polygon_boundary):
            grid_cells.append(new_cell)
        else:
            pass

    hexagon_grid = gpd.GeoDataFrame(geometry=grid_cells)
    return hexagon_grid
