#-----------------------------------------------
# Name        : silhouette.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Licence     : MIT
# Respect the autor and leave this here
#-----------------------------------------------

import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import fcluster
from scipy.cluster.hierarchy import linkage as scipy_linkage
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.metrics import silhouette_score, silhouette_samples, silhouette_score

# %% Main
def fit(X, metric='euclidean', linkage='ward', minclusters=2, maxclusters=25, Z=None, savemem=False, verbose=3):
    """This function return the cluster labels for the optimal cutt-off based on the choosen hierarchical clustering method.

    Parameters
    ----------
    X : Numpy-array,
        Where rows is features and colums are samples.
    metric : str, (default: 'euclidean').
        Distance measure for the clustering. Options are: 'euclidean','kmeans'.
    linkage : str, (default: 'ward')
        Linkage type for the clustering.
        'ward','single',',complete','average','weighted','centroid','median'.
    minclusters : int, (default: 2)
        Number of clusters that is evaluated greater or equals to minclusters.
    maxclusters : int, (default: 25)
        Number of clusters that is evaluated smaller or equals to maxclusters.
    savemem : bool, (default: False)
        Save memmory when working with large datasets. Note that htis option only in case of KMeans.
    Z : Object, (default: None).
        This will speed-up computation if you readily have Z. e.g., Z=linkage(X, method='ward', metric='euclidean').
    verbose : int, optional (default: 3)
        Print message to screen [1-5]. The larger the number, the more information is returned.

    Returns
    -------
    dict. with various keys. Note that the underneath keys can change based on the used methodtype.
    method: str
        Method name that is used for cluster evaluation.
    score: pd.DataFrame()
        The scoring values per clusters.
    labx: list
        Cluster labels.
    fig: list
        Relevant information to make the plot.

    Examples
    --------
    >>> # Import library
    >>> import clusteval.silhouette as silhouette
    >>> from sklearn.datasets import make_blobs
    >>>
    >>> # Example 1:
    >>> Generate demo data
    >>> X, labels_true = make_blobs(n_samples=750, centers=5, n_features=10)
    >>> # Fit with default parameters
    >>> results = silhouette.fit(X)
    >>> # plot
    >>> silhouette.scatter(results, X)
    >>> silhouette.plot(results)
    >>>
    >>> # Example 2:
    >>> # Try also alternative dataset
    >>> X, labels_true = make_blobs(n_samples=750, centers=[[1, 1], [-1, -1], [1, -1], [-1, 1]], cluster_std=0.4,random_state=0)
    >>> # Fit with some specified parameters
    >>> results = silhouette.fit(X, metric='kmeans', savemem=True)
    >>> # plot
    >>> silhouette.scatter(results, X)
    >>> silhouette.plot(results)

    References
    ----------
    http://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html

    """
    # Make dictionary to store Parameters
    Param = {}
    Param['verbose'] = verbose
    Param['metric'] = metric
    Param['linkage'] = linkage
    Param['minclusters'] = minclusters
    Param['maxclusters'] = maxclusters
    Param['savemem'] = savemem

    # Savemem for kmeans
    if Param['metric']=='kmeans':
        if Param['savemem']:
            kmeansmodel = MiniBatchKMeans
            if Param['verbose']>=3: print('[silhouette] >Save memory enabled for kmeans with method silhouette.')
        else:
            kmeansmodel = KMeans

    # Cluster hierarchical using on metric/linkage
    if (Z is None) and (Param['metric']!='kmeans'):
        Z = scipy_linkage(X, method=Param['linkage'], metric=Param['metric'])

    # Make all possible cluster-cut-offs
    if Param['verbose']>=3: print('[silhouette] >Determining optimal [%s] clustering by silhouette score..' %(Param['metric']))

    # Setup storing parameters
    clustcutt = np.arange(Param['minclusters'],Param['maxclusters'])
    silscores = np.zeros((len(clustcutt)))*np.nan
    sillclust = np.zeros((len(clustcutt)))*np.nan
    clustlabx = []

    # Run over all cluster cutoffs
    for i in tqdm(range(len(clustcutt))):
        # Cut the dendrogram for i clusters
        if Param['metric']=='kmeans':
            labx = kmeansmodel(n_clusters=clustcutt[i], verbose=0).fit(X).labels_
        else:
            labx = fcluster(Z, clustcutt[i], criterion='maxclust')

        # Store labx for cluster-cut
        clustlabx.append(labx)
        # Store number of unique clusters
        sillclust[i] = len(np.unique(labx))
        # Compute silhouette (can only be done if more then 1 cluster)
        if sillclust[i]>1:
            silscores[i] = silhouette_score(X, labx)

    # Convert to array
    clustlabx = np.array(clustlabx)

    # Store only if agrees to restriction of input clusters number
    I1 = np.isnan(silscores)==False
    I2 = sillclust>=Param['minclusters']
    I3 = sillclust<=Param['maxclusters']
    I  = I1 & I2 & I3

    # Get only clusters of interest
    silscores = silscores[I]
    sillclust = sillclust[I]
    clustlabx = clustlabx[I,:]
    clustcutt = clustcutt[I]
    idx = np.argmax(silscores)

    # Store results
    results = {}
    results['method']='silhouette'
    results['score'] = pd.DataFrame(np.array([sillclust,silscores]).T, columns=['clusters','score'])
    results['score']['clusters'] = results['score']['clusters'].astype(int)
    results['labx']  = clustlabx[idx,:]-1
    results['fig'] = {}
    results['fig']['silscores'] = silscores
    results['fig']['sillclust'] = sillclust
    results['fig']['clustcutt'] = clustcutt

    # Return
    return(results)

# %% plot
def plot(results, figsize=(15,8)):
    """Make plot for the gridsearch over the number of clusters.

    Parameters
    ----------
    results : dict.
        Dictionary that is the output of the .fit() function.
    figsize : tuple, (default: (15,8))
        Figure size, (heigh,width).

    Returns
    -------
    tuple, (fig, ax)
        Figure and axis of the figure.

    """
    idx = np.argmax(results['fig']['silscores'])
    # Make figure
    fig, ax1 = plt.subplots(figsize=figsize)
    # Plot
    ax1.plot(results['fig']['sillclust'], results['fig']['silscores'], color='k')
    # Plot optimal cut
    ax1.axvline(x=results['fig']['clustcutt'][idx], ymin=0, ymax=results['fig']['sillclust'][idx], linewidth=2, color='r',linestyle="--")
    # Set fontsizes
    plt.rc('axes', titlesize=14)  # fontsize of the axes title
    plt.rc('xtick', labelsize=10)  # fontsize of the axes title
    plt.rc('ytick', labelsize=10)  # fontsize of the axes title
    plt.rc('font', size=10)
    # Set labels
    ax1.set_xticks(results['fig']['clustcutt'])
    ax1.set_xlabel('#Clusters')
    ax1.set_ylabel('Score')
    ax1.set_title("silhouette score versus number of clusters")
    ax1.grid(color='grey', linestyle='--', linewidth=0.2)
    plt.show()
    # Return
    return(fig,ax1)


# %% Scatter data
def scatter(labx, X=None, figsize=(15,8), verbose=3):
    """Make scatter for the cluster labels with the samples.

    Parameters
    ----------
    labx: list
        Cluster labels for the samples in X (some order).
    X : Numpy-array,
        Where rows is features and colums are samples. The first two columns of the matrix are used for plotting. Note that it is also possible provide tSNE coordinates for a better representation of the data.
    figsize : tuple, (default: (15,8))
        Figure size, (heigh,width).

    Returns
    -------
    tuple, (fig, ax1, ax2)
        Figure and axis of the figure.

    """
    if X is None:
        if verbose>=2: print('[silhouette] >Warning: Input data X is required for the scatterplot.')
        return None

    # Label
    if isinstance(labx, dict):
        labx = labx.get('labx', None)
    # Check labx
    if labx is None:
        if verbose>=3: print('[silhouette] >Error: No labels provided.')
        return None

    # Plot silhouette samples plot
    # n_clusters = len(np.unique(labx))
    n_clusters = len(set(labx)) - (1 if -1 in labx else 0)
    silhouette_avg = silhouette_score(X, labx)
    if verbose>=3: print('[silhouette] >Estimated number of n_clusters: %d, average silhouette_score=%.3f' %(n_clusters, silhouette_avg))

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(X, labx)

    # Create a subplot with 1 row and 2 columns
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    fig.set_size_inches(18, 7)
    ax1.set_xlim([-0.1, 1])

    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])
    y_lower = 10
    uiclust = np.unique(labx)

    # Make 1st plot
    for i in range(0,len(uiclust)):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = sample_silhouette_values[labx == uiclust[i]]
        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i
        color = cm.Set2(float(i) / n_clusters)

        ax1.fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_silhouette_values, facecolor=color, edgecolor=color, alpha=0.7)
        # ax1.fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_silhouette_values, facecolor=getcolors[i], edgecolor=getcolors[i], alpha=0.7)
        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(uiclust[i]))
        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")
    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
    ax1.grid(color='grey', linestyle='--', linewidth=0.2)

    # 2nd Plot showing the actual clusters formed
    color = cm.Set2(labx.astype(float) / n_clusters)
    ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.8,c=color, edgecolor='k')
    ax2.grid(color='grey', linestyle='--', linewidth=0.2)
    ax2.set_title("Estimated cluster labels")
    ax2.set_xlabel("1st feature")
    ax2.set_ylabel("2nd feature")
    # General title
    plt.suptitle(("Silhouette analysis results in n_clusters = %d" %(n_clusters)), fontsize=14, fontweight='bold')
    plt.show()
    # Return
    return(fig, ax1, ax2)
