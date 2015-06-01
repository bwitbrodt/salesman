def distTable(data, classified_data):
    import numpy
    
    #Create pandas DataFrame for the classified group
    sites = classified_data.loc[classified_data['Site_ID'].isin(data)]
    
    #Add the base location twice (start and finish)
    sites.loc[-1]=[42.366197, -71.559268,0,9999,0]
    sites.loc[-2]=[42.366197, -71.559268,0,9999,0]
    sites.index = range(len(sites))
    
    #Create list of locations (Lat,Long) for the group
    site_coords=[]
    for index, site in sites.iterrows():
        site_coords.append([site['Lat'],site['Long']])
    
    #Calcualte a 
    N = len(site_coords)
    distance_matrix = numpy.zeros((N, N))

#Calculate a distance matrix (distance from each point to everyother point)
#Note this distance in miles. It does factor in curvature
#Curvature is calculated using the haversine formula. However, I envision 
#you using historical travel data
#rather than euclidean distance calcs to determine route times 
   
    for i in xrange(N):
        for j in xrange(N):
            lati = sites.Lat[i]
            loni = sites.Long[i]
            latj = sites.Lat[j]
            lonj = sites.Long[j]
            distance_matrix[i, j] = haversine(loni, lati, lonj, latj)
            distance_matrix[j, i] = distance_matrix[i, j]
            
    return distance_matrix



#This function factors in the curvature of the Earth. To help simplify the
#rest of the calculations, I also return only integer values of the final distance.

def haversine(lon1, lat1, lon2, lat2):
    from math import radians, cos, sin, asin, sqrt
    
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth. Use 3956 for miles
    return int(c * r)