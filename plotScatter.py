def plotScatter(data,k):
    import pylab
    import matplotlib.pyplot as plt
    import numpy

    x = data.Hr_Length
    y = data.Total_Specimens
    
    pylab.figure(figsize=(12, 9)) 
    ax = pylab.subplot(111)  
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()
    
    pylab.xticks(fontsize=12)  
    pylab.yticks(fontsize=12)
    
    pylab.xlabel("Length of Route (hours)", fontsize=14)  
    pylab.ylabel("Specimens per Route", fontsize=14) 
    pylab.title("Specimens vs Route Length\nCluster-level ", fontsize=20)  
    
    pylab.scatter(x,y)
    
    pylab.legend(loc='upper left')
    
    xmin,xmax = pylab.xlim()
    ymin,ymax = pylab.ylim()
    
    pylab.text(xmax - 1.72,ymin + 20, "Cluster Size = %i"%k, fontsize=10)  
    
    plt.axvspan(7, 9, facecolor='y', alpha=0.3)
    plt.axvspan(9, xmax, facecolor='r', alpha=0.3)
    
    ax.text(0.83, 0.99, 'Longer than workday', transform=ax.transAxes, fontsize=10,verticalalignment='top', style='italic')
    ax.text(0.665, 0.99, 'Day-long Routes', transform=ax.transAxes, fontsize=10,verticalalignment='top', style='italic')
    ax.text(0.23, 0.99, 'Routes for Combinations', transform=ax.transAxes, fontsize=10,verticalalignment='top', style='italic')

    for i,row in data.iterrows():
        ax.annotate(data.Cluster[i], (data.Hr_Length[i]+.07,data.Total_Specimens[i]+.07),fontsize=8)
    
    pylab.xlim(0,11)
        
    pylab.savefig('Scatter_Plot_clustersize_%i.png'%k, bbox_inches="tight");  
 
    plot = pylab.show()
    return plot
    