def sum_specimens(classified_data, classifier, hours, var):

#So far we have not used any specimen count data. I will generate random integers to simulate the
#number of specimens. You should be able to implement historical estimates to better approximate 
#the sample counts of each cluster. Again, you dont need to be accurate on the site level, but rather
#you can aggregate on the cluster-level and so you just need to be semi-accurate there.

    import pandas
    import random
    classified_data['Specimens'] = 0

    #for some reason these next two lines take WAY too long
    for index, site in classified_data.iterrows():
        classified_data.Specimens[index]= random.randint(0,50)
    
    #Create a dataframe and sum all specimens for each cluster
    Spec_count = pandas.DataFrame()
    Spec_count['Cluster'] = classifier.viewkeys()
    Spec_count['Total_Specimens'] = [sum(v) for k,v in classified_data.groupby("Cluster")["Specimens"]]
    
    Daily_Specimens = sum(Spec_count['Total_Specimens'])
    Avg_D = Daily_Specimens / hours
    
    #Lets place upper and lower bounds on hourly amount for some fluctuation
    Lower_bound = Avg_D * (1-var)
    Upper_bound = Avg_D * (1+var)
    
    return Daily_Specimens, Lower_bound, Upper_bound, Avg_D, Spec_count