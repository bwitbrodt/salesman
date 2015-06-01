def nOptimize(deliveries,nOffsets,FactOpen,FactClose):    
    from scipy.optimize import minimize
    import numpy
    
    nlims = tuple((min(item),max(item)) for item in nOffsets.viewvalues())
    n_res = numpy.zeros(len(nOffsets))
    
    def fun(x):
        dels,FactOpen,FactClose = preLoad
    
    res = minimize(shiftOptimize, n_res, args=(deliveries,FactOpen,FactClose), method='COBYLA', bounds=nlims)
    return res.x,res

def shiftOptimize(nArray,deliveries,FactOpen,FactClose):
    import numpy
    import itertools

    cumList=[]
    for cluster,clusterdels,n in itertools.izip(deliveries.viewkeys(),deliveries.viewvalues(),nArray):
        for datapoint in clusterdels:
            x = datapoint[0] + n
            y = datapoint[1]
            cumList.append([x,y])

    cumList.sort()   
    cumList = numpy.array(cumList)
    b= numpy.insert(cumList[:,1],0,0)
    a = numpy.append(cumList[:,0],FactClose)
    b = numpy.cumsum(b)
    cumList = numpy.vstack((a,b)).T  
    
    #from shapely.geometry import Polygon
    #datapoints =  numpy.vstack((cumList,[FactOpen,0]))
    #poly = Polygon(datapoints)
    #delta = poly.area           
    
    import Polygon
    test= Polygon.Polygon(cumList)
    delta = test.area()                                    
                                                                                                                
    return delta
    

