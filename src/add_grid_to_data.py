#First read in the ids, longitude and latitude for the datasets then convert to GeoDataFrames

gdf_trees = gpd.GeoDataFrame(tree_coords,geometry=gpd.GeoSeries.from_xy(tree_coords.longitude,tree_coords.latitude),crs='EPSG:4326')
gdf_grid = gpd.GeoDataFrame(df_grid, geometry=gpd.GeoSeries.from_wkt(df_grid.geometry), crs="EPSG:4326")

#This does a left inner join based on if the point geometry is within the grid geometry
combined = gdf_trees.sjoin(gdf_grid, how='left')

#Subsetting to just id and grid number
combined_df = combined[["id", "ID"]]
combined_df.columns = ["id", "grid"]
combined_df["grid"] = combined_df["grid"].astype("Int64")

#Appending a column to a dataset has been tricky. What we have done make a copy of the dataset that is being appended to, and create this id/grid dataset
#Then do a left join with this on the copy dataset in a query. Delete the original dataset, then save the query as the original dataset.
