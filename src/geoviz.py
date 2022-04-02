import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba


def base_geoviz(gdf, boundary_gdf, column, plot_size_x):
    """
    Plots a geovisualization in the standard geopandas format
    :param gdf: the geodataframe you want to plot with
    :param boundary_gdf: the geodataframe to be used as the background
    :param column: the column containing the values to plot
    :param plot_size_x: the size of the plot, this scales
    """
    x_min, y_min, x_max, y_max = boundary_gdf.total_bounds
    plot_size_y = plot_size_x * .9 * (y_max - y_min) / (x_max - x_min)

    fig, ax = plt.subplots(figsize=(plot_size_x, plot_size_y))
    boundary_gdf.plot(ax=ax, color='snow')
    gdf.plot(ax=ax, column=gdf[column], legend=True)
    ax.set_title('Shannon-Wiener Index of Bird Diversity Per Grid Cell',
                 fontdict={'fontsize': plot_size_x * 1.5, 'fontweight': 'medium'})
    ax.set_xlabel('Longitude [deg]', fontdict={'fontsize': plot_size_x, 'fontweight': 'medium'})
    ax.set_ylabel('Latitude [deg]', fontdict={'fontsize': plot_size_x, 'fontweight': 'medium'})
    plt.xticks(fontsize=plot_size_x * .75)
    plt.yticks(fontsize=plot_size_x * .75)
    fig.show()


def gradient_geoviz(gdf, boundary_gdf, column, plot_size_x, color):
    """
    Plots a geovisualization in the standard geopandas format
    :param gdf: the geodataframe you want to plot with
    :param boundary_gdf: the geodataframe to be used as the background
    :param column: the column containing the values to plot
    :param plot_size_x: the size of the plot, this scales
    :param color: The color you want to use for the gradient
    """
    gdf['color'] = color
    gdf['margin'] = (gdf[column] - gdf[column].min()) / (gdf[column].max() - gdf[column].min())
    gdf['alpha'] = gdf['alpha'] * (1 - .15) + .15
    gdf['color_rgba'] = gdf[['color', 'alpha']].apply(lambda row: to_rgba(row['color'], alpha=row['alpha']), axis=1)
    x_min, y_min, x_max, y_max = boundary_gdf.total_bounds
    plot_size_y = plot_size_x * .9 * (y_max - y_min) / (x_max - x_min)

    fig, ax = plt.subplots(figsize=(plot_size_x, plot_size_y))
    boundary_gdf.plot(ax=ax, color='snow')
    gdf.plot(ax=ax, column=gdf[column], color=gdf['color_rgba'])
    ax.set_title('Shannon-Wiener Index of Bird Diversity Per Grid Cell',
                 fontdict={'fontsize': plot_size_x * 1.5, 'fontweight': 'medium'})
    ax.set_xlabel('Longitude [deg]', fontdict={'fontsize': plot_size_x, 'fontweight': 'medium'})
    ax.set_ylabel('Latitude [deg]', fontdict={'fontsize': plot_size_x, 'fontweight': 'medium'})
    plt.xticks(fontsize=plot_size_x * .75)
    plt.yticks(fontsize=plot_size_x * .75)
    fig.show()
