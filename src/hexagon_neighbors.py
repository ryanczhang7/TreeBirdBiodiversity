import geopandas
from shapely.geometry import Polygon
import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


def get_neighbor_centroids(reference, hexagon_grid_gdf):
    """
    Get a geodataframe of the neighboring hexagons of the reference hexagon
    :param reference: the hexagon you are finding the neighbors for
    :param hexagon_grid_gdf: the original geodataframe of hexagons
    :return: a geodataframe containing the polygons neighbors
    """
    # Filtering for the polygons that intersect with our reference polygon
    mask = (hexagon_grid_gdf['geom'].intersects(reference))
    valid = hexagon_grid_gdf[mask]
    # The reference intersects with itself, so drop that
    neighbors = valid[valid['geom'] != reference]
    # Getting the centroid from the polygon, to easily calculate direction
    neighbors['centroid'] = neighbors['geom'].centroid
    # Getting the coordinates from the centroid
    neighbors['coord'] = neighbors['centroid'].apply(lambda x: (x.x, x.y))
    return neighbors


def get_neighbor_directions(neighbors, reference):
    """
    Get the implicit vector representing the directions of the neighboring hexagons wrt reference
    :param reference: the hexagon you are finding the neighbors for
    :param neighbors: the geodataframe of neighboring hexagons of the reference
    :return: the geodataframe neighbors, now containing implicit directions
    """
    # Subtracting the reference coordinate from each neighbor's coordinate
    # Then round and get the sign of the differences
    neighbors['direction'] = neighbors['coord'].apply(
        lambda x: np.sign(
            np.around(
                np.subtract(
                    x, (reference.centroid.x, reference.centroid.y)
                ), 6
            )
        )
    )
    return neighbors


def get_neighbors(idx, hexagon_id, reference, hexagon_grid_gdf):
    """
    Get the ID of the neighbor hexagons for each direction
    :param idx: the index of the hexagon we are fiding the neighbors for, from hexagon_grid_gdf
    :param hexagon_id: the ID of hexagon you are finding the neighbors for
    :param reference: the hexagon you are finding the neighbors for
    :param hexagon_grid_gdf: the original geodataframe of hexagons
    :return: the geodataframe neighbors, now containing actual directions
    """
    direction_dict = {}
    neighbors = get_neighbor_centroids(reference, hexagon_grid_gdf)
    neighbors = get_neighbor_directions(neighbors, reference)

    # Based on the orientation of our hexagons, there are only six
    # possible cases for directions for a hexagon's neighbors
    for row in neighbors[['ID', 'direction']].itertuples(index=True, name='Pandas'):
        direction_dict['ID'] = hexagon_id
        direction_dict['geom'] = reference
        if np.array_equal(row.direction, np.array([1.0, -1.0])):
            direction_dict['southeast'] = row.ID
            continue
        elif np.array_equal(row.direction, np.array([1.0, 1.0])):
            direction_dict['northeast'] = row.ID
            continue
        elif np.array_equal(row.direction, np.array([-1.0, 1.0])):
            direction_dict['northwest'] = row.ID
            continue
        elif np.array_equal(row.direction, np.array([-1.0, -1.0])):
            direction_dict['southwest'] = row.ID
            continue
        elif np.array_equal(row.direction, np.array([0.0, 1.0])):
            direction_dict['north'] = row.ID
            continue
        elif np.array_equal(row.direction, np.array([0.0, -1.0])):
            direction_dict['south'] = row.ID
            continue

    return pd.DataFrame(direction_dict, index=[idx], dtype=object)


def get_neighbor_hexagon_dataframe(hexagon_grid_gdf):
    """
    Starting with a geodataframe of hexagons, return a dataframe containing columns for each of
    its six neighbors in each direction (or potentially less for border hexagons)
    :param hexagon_grid_gdf: the original geodataframe of hexagons
    :return: the geodataframe neighbors, now containing actual directions
    """
    # Using itertuples to iterative get the ID's of the neighbors in each direction
    neighbors_df = pd.DataFrame()
    for row in hexagon_grid_gdf.itertuples(index=True, name='Pandas'):
        neighbors = get_neighbors(row.Index, row.ID, row.geom, hexagon_grid_gdf)
        neighbors_df = neighbors_df.append(neighbors)
    return neighbors_df
