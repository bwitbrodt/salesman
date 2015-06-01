def deliveryProfile(Spec_count2,DriveStart,FactEnd):
    import pandas
    import numpy
    
    #Creates a tuple dictionary of (Route Length, Num of Specimens) for each driver
    Spec_count2['SpecTime'] = zip(Spec_count2.Hr_Length, Spec_count2.Total_Specimens)
    driverDict = {k: list(v) for k,v in Spec_count2.groupby("Driver")['SpecTime']}
    driverTimes = {k: list(v) for k,v in Spec_count2.groupby("Driver")['Hr_Length']}
    
    #Make times cumulative
    for driver,times in driverTimes.iteritems():
        driverTimes[driver] = numpy.cumsum(times).tolist() 

    
    #Combine cumulative times with Specimens per delivery
    dailyDel = {}
    for k in driverTimes.viewkeys() and driverDict.viewkeys():
        for times,Specs in zip(driverTimes[k], driverDict[k]):
            if not k in dailyDel:
                dailyDel[k] = [(times,Specs[:][1])]
            else:
                dailyDel[k].append((times,Specs[:][1]))   
                      
    #dailyDel[9999]= driverDict[9999]
    
    #Convert times into daytimes
    militaryTimeDel = {}
    for p in dailyDel.viewkeys():
        for hourly,amt in dailyDel[p]:
            if not p in militaryTimeDel:
                militaryTimeDel[p] = [(hourly + DriveStart,amt)]
            else:
                militaryTimeDel[p].append((hourly + DriveStart,amt))     
    
    #Creates a list of possible 'n' values for each driver
    #n = the possible integer shift in start time for the driver
    n_list = {}
    for q in dailyDel.viewkeys():
        max_hour = 0
        for hourly,amt in dailyDel[q]:
            max_hour = max(hourly,max_hour)
        if not q in n_list:
            n_list[q] = range(0,int(FactEnd - DriveStart - max_hour+1))
        else:
            n_list[q].append(range(0,int(FactEnd - DriveStart - max_hour+1)))

    return militaryTimeDel,dailyDel,n_list