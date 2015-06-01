def plotStep(data, Daily_Total, Hrs, k):
    import pylab
    import matplotlib.pyplot as plt
    import numpy

    data.sort(['Hr_Length'], inplace = True, ascending=[True])
    data.cumSpec = numpy.cumsum(data['Total_Specimens'])

    x = data.Hr_Length
    y = data.cumSpec
    
    pylab.figure(figsize=(12, 9)) 
    ax = pylab.subplot(111)  
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()
    
    pylab.xticks(fontsize=14)  
    pylab.yticks(fontsize=14)
    pylab.xlim(0,Hrs + 1)
    
    pylab.xlabel("Hours", fontsize=16)  
    pylab.ylabel("Total Specimens", fontsize=16) 
    pylab.title("Daily Specimens Deliveries", fontsize=20)  
    
 
    pylab.step(x, y , color="#F0501A", lw=2.0, label="Actual Deliveries")
    pylab.plot([0,Hrs], [0,Daily_Total], color = "#3F5D7D", lw=2.0, label = 'Hypothetical Constant Flow')
    
    pylab.legend(loc='upper left')
    pylab.text(11, 450, "Cluster Size = %i"%k, fontsize=10)  
       
    pylab.savefig('Step_Plot_clustersize_%i.png'%k, bbox_inches="tight");  
 
    plot = pylab.show()
    return plot
