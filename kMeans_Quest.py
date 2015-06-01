def clusterSites(locations, numClusters):
    import numpy as np
    
    #Create the k-means clusters
    
    #After reviewing the plots of the clusters, I think we need to modify the data before clustering.
    #The problem is that the coords are in Lat,Long which doesnt translate perfectly into X,Y.
    #If you inspect the plot, the clusters seem to be horizontally skewed. I suppose this is because
    #of the conversion between lat/long and x/y. Maybe normalizing along each axis will give proportional
    #data points?
    
    from sklearn import cluster
    k = numClusters                     # ~number of daily routes
    kmeans = cluster.KMeans(n_clusters=k, max_iter=1000,n_init = 50)
    kmeans.fit(locations)
    
    #Get the cluster labels and centroids
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    
    #Plot the data
    from matplotlib import pyplot
    
    for i in range(k):
        # select only data observations with cluster label == i
        ds = locations[np.where(labels==i)]
        # plot the data observations
        pyplot.plot(ds[:,0],ds[:,1],'o')
        # plot the centroids
        lines = pyplot.plot(centroids[i,0],centroids[i,1],'kx')
        # make the centroid x's bigger
        pyplot.setp(lines,ms=15.0)
        pyplot.setp(lines,mew=2.0)
    #Add text
    pyplot.xticks(fontsize=12)  
    pyplot.yticks(fontsize=12)
    pyplot.suptitle("K-Means Clustering", fontsize=14) 
    pyplot.title("Cluster Size = %i"%k, fontsize=12) 
    pyplot.show()
    pyplot.savefig('Clustering_clustersize_%i.png'%k, bbox_inches="tight");
    
    return labels
    
    
def classify(labels, locations):  
    #Place locations and classifications into dataframe 
    import pandas
    classified_data = pandas.DataFrame(data = locations, columns = ['Lat','Long'])
    classified_data['Cluster'] = labels
    classified_data['Site_ID'] = range(len(classified_data))
    
    #Create a dictionary with each cluster and all the sites in that cluster
    classifier = {k: list(v) for k,v in classified_data.groupby("Cluster")["Site_ID"]}
    return classified_data, classifier

