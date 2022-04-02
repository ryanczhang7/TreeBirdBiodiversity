import numpy as np


def shannon_index(species_df, gridId, overallCountCol, speciesCountCol):
    """
    returns an geodataframe with the shannon entropy indices for each grid
    :param species_df: max y-coordinate from the boundary
    :param gridId: the column containing the ID's of the grid
    :param overallCountCol: the overall count of observations in a grid
    :param speciesCountCol: the count of observations for a specific species in a grid
    :return: a geodataframe with the shannon entropy indices
    """
    species_df['p_i'] = species_df[speciesCountCol] / species_df[overallCountCol]
    species_df['entropy'] = np.log(species_df['p_i']) * species_df['p_i']
    shannon_df = species_df.groupby(gridId).sum('entropy').reset_index()
    shannon_df['shannon_index'] = -shannon_df['entropy']