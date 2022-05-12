
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go

def cluster(data_df, return_figure=False):

    """Deterministically cluster the data into two clusters, using K-means clustering.
    Returns the cluster centres and optionally a scatter plot.

    Cluster centroids are returned as they come out of the underlying clustering algorithm and *also* 
    sorted by x coordinate, to deal with the "label switching problem" discussed for example here:
    https://stats.stackexchange.com/questions/224759/
    We want to have both versions available."""
    
    # Fix random_state for reproducibility
    clusterer = KMeans(n_clusters=2, init='k-means++', n_init=1, random_state=3)

    clusterer.fit(data_df)
        
    cl1_centroid, cl2_centroid = clusterer.cluster_centers_
    if cl1_centroid[0] < cl2_centroid[0]:
        x1, y1, x2, y2 = cl1_centroid[0], cl1_centroid[1], cl2_centroid[0], cl2_centroid[1]
        colour_map = {0: '0', 1: '1'}
    else:
        x1, y1, x2, y2 =  cl2_centroid[0], cl2_centroid[1], cl1_centroid[0], cl1_centroid[1]
        colour_map = {0: '1', 1: '0'}
    
    if return_figure:
        plot_df = data_df.copy()
        plot_df['cluster'] = clusterer.labels_
        plot_df['cluster'] = plot_df['cluster'].map(colour_map)
        plot_df = plot_df.sort_values('cluster', ignore_index=True)
        figure = px.scatter(data_frame=plot_df, x='x', y='y', color='cluster', height=700, width=700)
        figure.update_layout(showlegend=False)
        
        # Add the centroids :)
        
        figure.add_trace(go.Scatter(x=[x1, x2], y=[y1, y2],
            mode='markers',
            marker = {
                'color': ['#636EFA', '#EF553B'],
                'size': 15,
                'line': {'color': 'Black', 'width': 1},
                'symbol': 'x'
            }))
    else:
        figure = None
        
    return {
        
        # Sorted by x-coordinate:
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2,
        
        # Unsorted:
        'x1u': cl1_centroid[0],
        'y1u': cl1_centroid[1],
        'x2u': cl2_centroid[0],
        'y2u': cl2_centroid[1],
        
        'figure': figure
    }
