import pandas as pd 
import numpy as np 
import sys
import math
import heapq
import itertools


# read the road segments data
df_rs = pd.read_csv('road-segments.txt', delimiter=' ', header=None, names=["city1","city2","distance","speed_limit","highway"])
df_rs["time"]=df_rs.distance/df_rs.speed_limit #adding a time column 
df_rs["prob_accidents"] = 0
#adding a column for probability of accidents to keep a track of the safe routes
for i in range(0,df_rs.shape[0]):
    if 'I-' in df_rs['highway'][i]:
       df_rs["prob_accidents"].iloc[i] = float(df_rs['distance'].iloc[i]/1000000) #for interstate 1 per million
    else:
        df_rs["prob_accidents"].iloc[i] = float(df_rs['distance'].iloc[i]*2/1000000) #for non-interstate 2 per million

#read the city-gps data    
df_gps=pd.read_csv('city-gps.txt',delimiter=' ', header=None, names=["city","latitude","longitude"])

sp=df_rs.speed_limit.mean() #average speed for the data
avg_seg=df_rs.distance.sum()/df_rs.shape[0] #average segment length for the data


#generates the successors by comparing the city given with the possible neighbouring cities/route
def successors(city_s):
    fringe=[]
    for i in range(0,df_rs.shape[0]):
        if df_rs.city1[i]==city_s:
            fringe.append([df_rs.city1[i],df_rs.city2[i],df_rs.distance[i],df_rs.speed_limit[i],df_rs.highway[i],df_rs.time[i],df_rs.prob_accidents[i]])
        elif df_rs.city2[i]==city_s:
            fringe.append([df_rs.city2[i],df_rs.city1[i],df_rs.distance[i],df_rs.speed_limit[i],df_rs.highway[i],df_rs.time[i],df_rs.prob_accidents[i]])
    #print(fringe)
    return fringe





# Ref: https://stackoverflow.com/questions/36873187/heuristic-for-an-a-path-finding-gps
#This function calculates the heuristics using haversine formula
def calculate_heuristic(lat_s,long_s,lat_d,long_d):
    R = 3963
    dLat = deg2rad(lat_d-lat_s)
    dLon = deg2rad(long_d-long_s)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat_s)) * math.cos(deg2rad(lat_d)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c; 
    return d

def deg2rad(deg):
    return deg * (math.pi/180)

# this funciton returns the goal with the ideal segment cost
def calculate_min_heuristic_seg(city_s,city_d):
    cost_segment=1
    visited_node=[]
    fringe_segment = [(0,0,city_s,[])]
    heapq.heapify(fringe_segment)
    lat_d = df_gps.loc[df_gps.city==city_d, 'latitude'].iloc[0] 
    long_d = df_gps.loc[df_gps.city==city_d, 'longitude'].iloc[0]
    lat_s =  df_gps.loc[df_gps.city==city_s, 'latitude'].iloc[0]  
    long_s =  df_gps.loc[df_gps.city==city_s, 'longitude'].iloc[0] 
    while len(fringe_segment) !=0:
        succ = heapq.heappop(fringe_segment) #popping out the path with the least hueristic value
        if succ[2]==city_d: # checking the goal state
            return succ[3]
        visited_node.append(succ[2])  #keeping a track of the visited nodes
        for move in successors(succ[2]):
            try:
                lat_c = df_gps.loc[df_gps.city==move[1], 'latitude'].iloc[0]  
                long_c = df_gps.loc[df_gps.city==move[1], 'longitude'].iloc[0]
                h_s= calculate_heuristic(lat_c,long_c,lat_d,long_d) # heuristic is the haversine distance from current state to goal divided by the average segment length
            except:
                h_s=0  # cathces the case where a certain destination does not have lat and long
            if move[1] not in visited_node:
                cost_segment=len(succ[3])
                # cost + heuristic
                f=cost_segment+h_s/avg_seg
                heapq.heappush(fringe_segment,(f,move[2],move[1],succ[3]+[move]))

# this funciton returns the goal with ideal safe path        
def calculate_min_heuristic_safe(city_s,city_d):
    prob=0
    visited_node=[]
    fringe_segment = [(0,0,city_s,[])]
    heapq.heapify(fringe_segment)
    lat_d = df_gps.loc[df_gps.city==city_d, 'latitude'].iloc[0] 
    long_d = df_gps.loc[df_gps.city==city_d, 'longitude'].iloc[0]
    lat_s =  df_gps.loc[df_gps.city==city_s, 'latitude'].iloc[0]  
    long_s =  df_gps.loc[df_gps.city==city_s, 'longitude'].iloc[0] 
    while len(fringe_segment) !=0:
        succ = heapq.heappop(fringe_segment) #popping out the path with the least hueristic value
        if succ[2]==city_d: # checking the goal state
            return succ[3]
        visited_node.append(succ[2]) #keeping a track of the visited nodes
        for move in successors(succ[2]):
            try:
                lat_c = df_gps.loc[df_gps.city==move[1], 'latitude'].iloc[0]  
                long_c = df_gps.loc[df_gps.city==move[1], 'longitude'].iloc[0]
                h_s= calculate_heuristic(lat_c,long_c,lat_d,long_d)  # heuristic is the haversine distance from current state to goal divided by the probabilites for interstate accidents and non-interstate accidents
            except: 
                h_s=0  # cathces the case where a certain destination does not have lat and long
            if move[1] not in visited_node:
                prob=0
                for i in succ[3]:
                    prob=prob+i[6]  # caclulating the safe probability from start state to current state
                # cost + heuristic
                f = prob + (h_s/1000000+h_s/2000000)
                heapq.heappush(fringe_segment,(f,move[2],move[1],succ[3]+[move]))
    
# this segment returns the goal with ideal distance path
def calculate_min_heuristic_distance(city_s,city_d):
    seg = []
    cost_segment=1
    dist=0
    time=0
    speed=0
    prob=0
    interstate=0
    path=''
    noninterstate=0
    visited_node=[]
    fringe_segment = [(0,0,city_s,[])]
    heapq.heapify(fringe_segment)
    lat_d = df_gps.loc[df_gps.city==city_d, 'latitude'].iloc[0] 
    long_d = df_gps.loc[df_gps.city==city_d, 'longitude'].iloc[0]
    lat_s =  df_gps.loc[df_gps.city==city_s, 'latitude'].iloc[0]  
    long_s =  df_gps.loc[df_gps.city==city_s, 'longitude'].iloc[0] 
    while len(fringe_segment) !=0:
        succ = heapq.heappop(fringe_segment) #popping out the path with the least hueristic value
        if succ[2]==city_d: # checking the goal state
            return succ[3]
        visited_node.append(succ[2]) #keeping a track of the visited nodes
        for move in successors(succ[2]):
            try:
                lat_c = df_gps.loc[df_gps.city==move[1], 'latitude'].iloc[0]  
                long_c = df_gps.loc[df_gps.city==move[1], 'longitude'].iloc[0]
                h_s= calculate_heuristic(lat_c,long_c,lat_d,long_d) # heuristic is the haversine distance from current state to the goal state 
            except:
                h_s=0 # cathces the case where a certain destination does not have lat and long
            if move[1] not in visited_node:
                dist=0
                for i in succ[3]:
                    dist=dist+i[2] # caclulating the distance travelled from start state to current state
                # cost + heuristic
                f = dist + h_s
                heapq.heappush(fringe_segment,(f,move[2],move[1],succ[3]+[move]))

# this segment returns the goal with ideal time path                
def calculate_min_heuristic_time(city_s,city_d):
    seg = []
    cost_segment=1
    dist=0
    time=0
    speed=0
    prob=0
    interstate=0
    path=''
    noninterstate=0
    visited_node=[]
    fringe_segment = [(0,0,city_s,[])]
    heapq.heapify(fringe_segment)
    lat_d = df_gps.loc[df_gps.city==city_d, 'latitude'].iloc[0] 
    long_d = df_gps.loc[df_gps.city==city_d, 'longitude'].iloc[0]
    lat_s =  df_gps.loc[df_gps.city==city_s, 'latitude'].iloc[0]  
    long_s =  df_gps.loc[df_gps.city==city_s, 'longitude'].iloc[0] 
    while len(fringe_segment) !=0:
        succ = heapq.heappop(fringe_segment) #popping out the path with the least hueristic value
        if succ[2]==city_d: # checking the goal state
            return succ[3]
        visited_node.append(succ[2]) #keeping a track of the visited nodes
        for move in successors(succ[2]):
            try:
                lat_c = df_gps.loc[df_gps.city==move[1], 'latitude'].iloc[0]  
                long_c = df_gps.loc[df_gps.city==move[1], 'longitude'].iloc[0]
                h_s= calculate_heuristic(lat_c,long_c,lat_d,long_d)  # heuristic is the haversine distance from current state to the goal state 
            except:
                h_s=0  # cathces the case where a certain destination does not have lat and long
            if move[1] not in visited_node:
                time=0
                for i in succ[3]:
                    time=time+i[5]  # caclulating the time travelled from start state to current state
                # cost + heuristic
                f = time + h_s/sp
                heapq.heappush(fringe_segment,(f,move[2],move[1],succ[3]+[move]))


def get_route(city_s,city_d,cost):
    cost_fn=cost
    distance=float(0)
    safe=float(0)
    time=float(0)
    route=[]
    if cost_fn == "segments":
        seg = calculate_min_heuristic_seg(city_s,city_d)
        for i in seg: #iterating through the popped out goal to get the sum of distance, time and probability of safe path
            distance = distance+i[2]
            time = time + i[5]
            safe=safe+ i[6]
            route.append((i[1],str(i[4])+" for "+str(i[2])+" miles"))
        return{"total-segments" : len(seg), "total-miles": distance , "total-hours" : time,  "total-expected-accidents" : safe ,  "route-taken" : route}
    elif cost_fn == "distance":
        seg= calculate_min_heuristic_distance(city_s,city_d)
        for i in seg: #iterating through the popped out goal to get the sum of distance, time and probability of safe path
            distance = distance+i[2]
            time = time + i[5]
            safe=safe+ i[6]
            route.append((i[1],str(i[4])+" for "+str(i[2])+" miles"))
        return{"total-segments" : len(seg), "total-miles": distance , "total-hours" : time,  "total-expected-accidents" : safe ,  "route-taken" : route}
    elif cost_fn == "time":
        seg= calculate_min_heuristic_time(city_s,city_d)
        for i in seg: #iterating through the popped out goal to get the sum of distance, time and probability of safe path
            distance = distance+i[2]
            time = time + i[5]
            safe=safe+ i[6]
            route.append((i[1],str(i[4])+" for "+str(i[2])+" miles"))
        return{"total-segments" : len(seg), "total-miles": distance , "total-hours" : time,  "total-expected-accidents" : safe ,  "route-taken" : route}
    elif cost_fn == "safe":
        seg= calculate_min_heuristic_safe(city_s,city_d)
        for i in seg: #iterating through the popped out goal to get the sum of distance, time and probability of safe path
            distance = distance+i[2]
            time = time + i[5]
            safe=safe+ i[6]
            route.append((i[1],str(i[4])+" for "+str(i[2])+" miles"))
        return{"total-segments" : len(seg), "total-miles": distance , "total-hours" : time,  "total-expected-accidents" : safe ,  "route-taken" : route}

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "safe"):
        raise(Exception("Error: invalid cost function"))
    
    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n    Total segments: %6d" % result["total-segments"])
    print("    Total miles: %10.3f" % result["total-miles"])
    print("    Total hours: %10.3f" % result["total-hours"])
    print("    Total accidents: %15.8f" % result["total-expected-accidents"])

"""
	for city_min,h in fringe_dict.items():
		if h==fringe_h[0]:
			return city_min
"""
