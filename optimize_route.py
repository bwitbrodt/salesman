#Good lord. I can claim almost nothing from this function. I went to the Google and found this.
#All I did was modify a few code words for us. BOOOOOOOOOOOOM
#https://gist.github.com/mlalevic/6222750

#Note: the time to complete an optimization is highly variable. I ran it once and got an instant answer,
#but then struggled next time. There are other Python optimization methods available.

def solve_tsp_dynamic(distance_matrix):
    import itertools
    
    #calc all lengths
    all_distances = distance_matrix
    
    #initial value - just distance from 0 to every other point + keep the track of edges
    A = {(frozenset([0, idx+1]), idx+1): (dist, [0,idx+1]) for idx,dist in enumerate(all_distances[0][1:])}
    cnt = len(distance_matrix)
    for m in range(2, cnt):
        B = {}
        for S in [frozenset(C) | {0} for C in itertools.combinations(range(1, cnt), m)]:
            for j in S - {0}:
                B[(S, j)] = min( [(A[(S-{j},k)][0] + all_distances[k][j], A[(S-{j},k)][1] + [j]) for k in S if k != 0 and k!=j])  #this will use 0th index of tuple for ordering, the same as if key=itemgetter(0) used
        A = B
    res = min([(A[d][0] + all_distances[0][d[1]], A[d][1]) for d in iter(A)])
    
    return res[0],res[1]