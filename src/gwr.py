import numpy as np
import pandas as pd
import geopandas as gpd

from mgwr.gwr import GWR, MGWR
from mgwr.sel_bw import Sel_BW


def run_GWR(g_X, g_y, c, std=False):
  """
  returns a GWR model
  :param g_X: (n x p) matrix of predictor variable 
  :param g_y: (n x 1) matrix of response variable
  :param c: centroids of each of the observations 
  :param std: indicator to standardize the predictor variables
  """
  g_coords = [(x,y) for x,y in zip(c.x , c.y)]
 
  g_X_std = (g_X - g_X.mean(axis=0)) / g_X.std(axis=0)
  g_y_std = (g_y - g_y.mean(axis=0)) / g_y.std(axis=0)

  gwr_selector = Sel_BW(g_coords, g_y_std, g_X_std)
  gwr_bw = gwr_selector.search(bw_min=2)

  if std:
    g_X = g_X_std

  model = GWR(g_coords, g_y, g_X, gwr_bw)
  gwr_results = model.fit()

  return gwr_results
