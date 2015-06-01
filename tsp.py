
import random
import sys
import getopt
from PIL import Image, ImageDraw, ImageFont
from math import sqrt

def rand_seq(size):
    '''generates values in random order
    equivalent to using shuffle in random,
    without generating all values at once'''
    values=range(size)
    for i in xrange(size):
        # pick a random index into remaining values
        j=i+int(random.random()*(size-i))
        # swap the values
        values[j],values[i]=values[i],values[j]
        # return the swapped value
        yield values[i] 

def all_pairs(size):
    '''generates all i,j pairs for i,j from 0-size'''
    for i in rand_seq(size):
        for j in rand_seq(size):
            yield (i,j)

def reversed_sections(tour):
    '''generator to return all possible variations where the section between two cities are swapped'''
    for i,j in all_pairs(len(tour)):
        if i != j:
            copy=tour[:]
            if i < j:
                copy[i:j+1]=reversed(tour[i:j+1])
            else:
                copy[i+1:]=reversed(tour[:j])
                copy[:j]=reversed(tour[i+1:])
            if copy != tour: # no point returning the same tour
                yield copy

def swapped_cities(tour):
    '''generator to create all possible variations where two cities have been swapped'''
    for i,j in all_pairs(len(tour)):
        if i < j:
            copy=tour[:]
            copy[i],copy[j]=tour[j],tour[i]
            yield copy

def cartesian_matrix(coords):
    '''create a distance matrix for the city coords that uses haversine distance'''
    matrix={}
    for i,(x1,y1) in enumerate(coords):
        for j,(x2,y2) in enumerate(coords):
            matrix[i,j]=haversine(x1,y1,x2,y2)
    return matrix
    
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

def tour_length(matrix,tour):
    '''total up the total length of the tour based on the distance matrix'''
    total=0
    num_cities=len(tour)
    for i in range(num_cities):
        j=(i+1)%num_cities
        city_i=tour[i]
        city_j=tour[j]
        total+=matrix[city_i,city_j]
    return total

def write_tour_to_img(coords,tour,title,img_file):

    maxx,maxy, minx, miny = 0,0,100000,100000
    for x,y in coords:
        maxx=max(x,maxx)
        maxy=max(abs(y),maxy)
        minx=min(x,minx)
        miny=min(abs(y),miny)
    xsize = maxx - minx
    ysize = maxy - miny
    img=Image.new("RGB",(500,500),color=(255,255,255))
    
    x_scale = 450 / xsize
    y_scale = 450 / ysize
    
    font=ImageFont.load_default()
    d=ImageDraw.Draw(img);
    num_cities=len(tour)
    for i in range(num_cities):
        j=(i+1)%num_cities
        city_i=tour[i]
        city_j=tour[j]
        x1,y1=coords[city_i]
        x1 = (x1-minx+20) + ((x1-minx) * x_scale)
        y1 = (abs(y1)-miny+20) + ((abs(y1)-miny) * y_scale)
        x2,y2=coords[city_j]
        x2 = (x2-minx+20) + ((x2-minx) * x_scale)
        y2 = (abs(y2)-miny+20) + ((abs(y2)-miny) * y_scale)
        d.line((int(x1),int(y1),int(x2),int(y2)),fill=(0,0,0))
        d.text((int(x1)+7,int(y1)-5),str(i),font=font,fill=(32,32,32))
    
    for x,y in coords:
        x1 = (x-minx+20) + ((x-minx) * x_scale)
        y1 = (abs(y)-miny+20) + ((abs(y)-miny) * y_scale)
        #x,y=int(x),abs(int(y))
        d.ellipse((x1-3,y1-3,x1+3,y1+3),outline=(0,0,0),fill=(196,196,196))
    
    d.text((1,1),title,font=font,fill=(0,0,0))
    
    del d
    img.save(img_file, "PNG")

def init_random_tour(tour_length):
   tour=range(tour_length)
   random.shuffle(tour)
   return tour

def run_anneal(init_function,move_operator,objective_function,max_iterations,start_temp,alpha):
    if start_temp is None or alpha is None:
        usage();
        print "missing --cooling start_temp:alpha for annealing"
        sys.exit(1)
    from sa import anneal
    iterations,score,best=anneal(init_function,move_operator,objective_function,max_iterations,start_temp,alpha)
    return iterations,score,best


def tspSolver(site_coords,clusterID):
    
    def run_anneal_with_temp(init_function,move_operator,objective_function,max_iterations):
        return run_anneal(init_function,move_operator,objective_function,max_iterations,start_temp,alpha)

    max_iterations = 20000
    out_file_name = 'Cluster_%i.png' % clusterID
    move_operator=reversed_sections
    run_algorithm=run_anneal_with_temp
    verbose=None
    start_temp,alpha=10,0.9995
        
    # enable more verbose logging (if required) so we can see workings of the algorithms
    import logging
    format='%(asctime)s %(levelname)s %(message)s'
    if verbose:
        logging.basicConfig(level=logging.INFO,format=format)
    else:
        logging.basicConfig(format=format)
    
    # setup the things tsp specific parts hillclimb needs
    coords = site_coords
    init_function=lambda: init_random_tour(len(coords))
    matrix=cartesian_matrix(coords)
    objective_function=lambda tour: -tour_length(matrix,tour)
    
    logging.info('using move_operator: %s'%move_operator)
    
    iterations,score,best=run_algorithm(init_function,move_operator,objective_function,max_iterations)
    
    # output results
    #print "Iterations:",iterations
    #print "Min Distance:",abs(score),'miles'
    #print "Route:",best
    
    if out_file_name:
        write_tour_to_img(coords,best,'%s %s: %i %s'%('Cluster',clusterID,abs(score),'miles'),file(out_file_name,'w'))

    return abs(score),best