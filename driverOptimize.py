def splitter(data,n):
    l = zip(data.Hr_Length.tolist(),data.Cluster.tolist())

    numresult = [[] for i in range(n)]
    idxresult = [[] for i in range(n)]
    sums   = {i:0 for i in range(n)}
    c = 0
    for e,g in l:
        for i in sums:
            if c == sums[i]:
                numresult[i].append(e)
                idxresult[i].append(g)
                break
        sums[i] += e
        c = min(sums.values())    
    return numresult, idxresult  

def driverOptimizer(Spec_count1,Drivers,Min_driver_work,Max_driver_work,First_driver_hr,Last_driver_hr ,First_del_hr,Last_del_hr):
    import pandas
    import numpy
    driverSched = pandas.DataFrame(columns = ['Driver_ID','Route'])
    driverSched['Driver_ID'] = range(1,Drivers+1)
    
    #Add column for Driver ID assignment to each cluster
    Spec_count1['Driver'] = numpy.nan
    temp_Spec_count = pandas.DataFrame()
    
    D_count = 1
    tooLong = (Spec_count1.Hr_Length>Max_driver_work).sum()

    
    #Downselect the fullday routes and the too-long routes
    for index,driver in driverSched.iterrows():
        
        #Create temp dataframe with all clusters that are not assigned
        temp_Spec_count = Spec_count1[Spec_count1['Driver'].isnull()]
        count = 0
        
        
        for index,cluster in temp_Spec_count.iterrows():
            
            #Check if route exceeds max route length
            #if cluster.Hr_Length > Max_driver_work:
                #tooLong = tooLong + 1
            
            #Check if route is an all-day route
            if cluster.Hr_Length > Min_driver_work and count == 0:
                Spec_count1.Driver[cluster.Cluster] = driver['Driver_ID']
                count = count+1
                D_count = D_count + 1
    
    #Collect the remaining unassigned routes
    temp_Spec_count = Spec_count1[Spec_count1['Driver'].isnull()] 
    
    chunking_results = pandas.DataFrame(columns = ['numChunks','chunkidx','utilization'])
    chunking_results['numChunks']=range(1,1+len(temp_Spec_count))
    chunking_results['chunkidx'] = chunking_results['chunkidx'].astype(object)
    chunking_results['utilization'] = chunking_results['utilization'].astype(float)
    
    #Use greedy algo to optimize the assignment of chunks of remaining routes
    for i in range(1,1+len(temp_Spec_count)):
        
        chunks,chunkIdx = splitter(temp_Spec_count,i)
        
        #Tracks the cluster IDs in each chunk
        chunking_results.set_value(i-1,'chunkidx',chunkIdx)
        
        #Count the number of groups that fit within workday limits
        counter = 0
        for j in chunks:
            temp = sum(j)
            if temp>=Min_driver_work:
                if temp<= Max_driver_work:
                    counter = counter +1
   
        #Calculate a utilization for each number of chunks (# of "acceptable working hr" chunks / total chunks)    
        chunk_utilization = float(counter) / i
        chunking_results.utilization[chunking_results['numChunks']==(i)] = chunk_utilization
    
    pairings = chunking_results['chunkidx'].ix[chunking_results['utilization'].idxmax()]
    numChunks = chunking_results['numChunks'].ix[chunking_results['utilization'].idxmax()]
    maxutil = chunking_results['utilization'].ix[chunking_results['utilization'].idxmax()]

    #count = count + 1
    for item in pairings:
        Spec_count1.Driver[Spec_count1['Cluster'].isin(item)] = D_count
        D_count = D_count + 1

    return pairings,numChunks,maxutil, tooLong
