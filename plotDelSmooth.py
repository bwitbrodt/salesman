def plotSmooth(deliveries,k,Daily_Total,FactOpen,FactClose,nOptimal,plotType):
    import matplotlib.pyplot as plt
    import numpy
    import pylab
    from descartes import PolygonPatch
    import itertools

    pylab.figure(figsize=(12, 9)) 
    
    ax1 = pylab.subplot(111)  
    ax1.spines["top"].set_visible(False)  
    ax1.spines["right"].set_visible(False)
    ax1.get_xaxis().tick_bottom()  
    ax1.get_yaxis().tick_left()
    
    pylab.xticks(fontsize=12)  
    pylab.yticks(fontsize=12)
    
    pylab.xlabel("Time of Day", fontsize=14)  
    pylab.ylabel("Specimen Deliveries", labelpad = 20, fontsize=14) 
    pylab.suptitle("Daily Delivery Profile", fontsize=16) 
    pylab.title(plotType, fontsize=12)  

    cumList=[]
    #for cluster,clusterdels in deliveries.iteritems():
    for cluster,clusterdels,n in itertools.izip(deliveries.viewkeys(),deliveries.viewvalues(),nOptimal):
        for datapoint in clusterdels:
            x = datapoint[0] + nOptimal[n-1]
            y = datapoint[1]
            cumList.append([x,y])
            plt.bar(x,y , width = 0.08,alpha=0.8, color='silver')
    
    x1min,x1max = pylab.xlim()
    y1min,y1max = pylab.ylim()
    
    cumList.sort()   
    cumList = numpy.array(cumList)
    b= numpy.insert(cumList[:,1],0,0)
    a = numpy.append(cumList[:,0],FactClose)
    b = numpy.cumsum(b)
    cumList = numpy.vstack((a,b)).T

    ax2 = ax1.twinx()
    ax2.plot(cumList[:,0], cumList[:,1] , color="#F0501A", lw=2.0)
    ax2.plot([FactOpen,FactClose], [0,Daily_Total], color = "mediumorchid", lw=2.0, label = 'Hypothetical Constant Flow')
    pylab.ylabel("Total Specimens",labelpad = 20, fontsize=14, rotation = 270) 
    
    x2min,x2max = pylab.xlim()
    y2min,y2max = pylab.ylim()    
                
    poly,delta = shadeRegion(cumList,FactOpen,FactClose,Daily_Total)
    ring_patch = PolygonPatch(poly,fc='y', ec='b', alpha=0.3)
    ax2.add_patch(ring_patch)
    
    xmin = min(x1min,x2min)
    ymin = min(y1min,y2min)
    xmax = max(x1max,x2max)
    ymax = max(y1max,y2max)
    
    ax2.text(xmin + 0.4, ymax - 1000, 'Shaded region represents delta\nbetween delivery schedule and\noptimized constant specimen arrivals', fontsize=10,verticalalignment='top', style='italic')
    ax2.text(xmin + 0.4, ymax-600, "Cluster Size = %i"%k, fontsize=10)  
    pylab.savefig('Delivery_Profile_clustersize_%i.png'%k, bbox_inches="tight");  
 
    plot = pylab.show()
    
    return delta
    
def shadeRegion(datapoints,FactOpen,FactClose,Daily_Total):
    from shapely.geometry import Polygon
    import numpy
    
    datapoints =  numpy.vstack((datapoints,[FactOpen,0]))
    poly = Polygon(datapoints)
    delta = poly.area
    
    return poly, delta