#Import all my functions
import kMeans_Quest
import sum_specimens as SS
import tsp
import plotScatter
import plotStep
import driverOptimize as DO
import deliveryProfile as DP
import shiftOptimize as SO
import plotDelivery as plotDel
import plotDelSmooth as plotSmo

#Variable Input
Drivers = 20            #Number of drivers
Min_driver_work = 7.00  #Min number of hours that a driver can work
Max_driver_work = 9.00  #Max number of hours that a driver can work
First_driver_hr = 10    #First hour that drivers can starts route (subject to specimen availability as well)
Last_driver_hr = 23     #Last hour driver can pick up
First_del_hr = 11       #First Delivery Hour
Close_del_hr = 24       #Factory delivery closes
Var = 0.30              #Percentage variance in the average specimens accepted each hour


#Import the map points
import numpy as np
locations = np.genfromtxt('sample_Quest_pts.csv',delimiter=',',skiprows = 1, usecols=[1,3])


#Cluster the data in groups that are locationally-close
#Vary the number of clusters to equal the number of daily routes
k = 40     #Number of clusters
labels = kMeans_Quest.clusterSites(locations,k)
classified_data, classifier = kMeans_Quest.classify(labels,locations)


#Get total daily specimens, desired hourly average, and upper/lower hourly bounds
del_Hours = Close_del_hr - First_del_hr     #Hours Quest wants to evenly distribute deliveries
Daily_Specimens, Lower_bound, Upper_bound, Avg_D, Spec_count = SS.sum_specimens(classified_data, classifier, del_Hours, Var)

Spec_count['min_dist'] = 0
Spec_count['Hr_Length'] = 0.0
Spec_count['Route'] = 0
Spec_count['Route'] = Spec_count['Route'].astype(object)


#Use dictionary based on cluster number to analyze each cluster
for clusterID in classifier.viewkeys():
    
    #Create pandas DataFrame for the classied group
    sites = classified_data.loc[classified_data['Site_ID'].isin(classifier[clusterID])]
    
    #Add the base location twice (start and finish)
    sites.loc[-1]=[42.366197, -71.559268,0,9995,0]
    sites.loc[-2]=[42.366197, -71.559268,0,9995,0]
    sites.index = range(len(sites))
    
    #Create list of locations (Lat,Long) for the group
    site_coords=[]
    for index, site in sites.iterrows():
        site_coords.append((site['Lat'],site['Long']))
  
    #Solve TSP for cluster
    min_dist,opt_route = tsp.tspSolver(site_coords,clusterID)
    
    #Add the min route distance to the results table
    Spec_count.min_dist[Spec_count['Cluster']==clusterID] = min_dist
    
    #Calculate an estimated route time (in hrs) (assumes 30mph and 10min at each stop)
    Spec_count.Hr_Length[Spec_count['Cluster']==clusterID] = np.round((min_dist / 30.0) + (len(opt_route)*(10.0/60)),2)
    
    #Add the route directions to the route list
    Spec_count.set_value(clusterID,'Route',opt_route)

#Visualize the cluster data
plotScatter.plotScatter(Spec_count,k)
#plotStep.plotStep(Spec_count, Daily_Specimens, del_Hours, k)

#Assign routes to drivers
paired,numberChunks,utilization,tooLong = DO.driverOptimizer(Spec_count,Drivers,Min_driver_work,Max_driver_work,First_driver_hr,Last_driver_hr ,First_del_hr,Close_del_hr)

#Creates timelines for drivers and also daily schedule of deliveries
milTimeDel,workerDel,nList = DP.deliveryProfile(Spec_count,First_driver_hr,Close_del_hr)


#Baseline Analysis
###########################
nArray_baseline = np.zeros(len(nList))
baseline = SO.shiftOptimize(nArray_baseline,milTimeDel,First_del_hr,Close_del_hr)
#Shaded, non-optimized plot
plotSmo.plotSmooth(milTimeDel,k,Daily_Specimens,First_del_hr,Close_del_hr,nArray_baseline,'Baseline')
#Step Function non-optimized
#plotDel.plotDelivery(milTimeDel,k,Daily_Specimens,First_del_hr,Close_del_hr)


#Optimized Analysis
###########################
#Factors in offsets of each driver's start time
n_opt,optimal = SO.nOptimize(milTimeDel,nList,First_del_hr,Close_del_hr)
#Shaded, optimized
plotSmo.plotSmooth(milTimeDel,k,Daily_Specimens,First_del_hr,Close_del_hr,n_opt,'Optimized')


#Print Short Summary
##########################################################
print ''
print '     Number of Clusters:',k
print 'Number of Total Drivers:',len(n_opt)
print '            Multi-Route:',numberChunks
print '               Full-Day:',(len(n_opt)-numberChunks-tooLong)
print '           Extended-Day:',tooLong
print 'Percent of multi-routes acceptable as full-days:',"%0.2f" % (utilization,)
print ''
print 'Baseline area:',"%0.3f" % (baseline,)
print 'Optimized area:',"%0.3f" % (optimal.fun)