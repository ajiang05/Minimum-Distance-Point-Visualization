import math

"""
1. We need to accept an array of coordinates
2. We order the coordinates in terms of the x value from least to greatest
3. we get length of the array of coordinates
4.If it is 2 then we return the distance between the 2
5.If it is 3 we return the minimum distance between the 3
6. We have to get the midpoint of array by doing floor(length/2)
7. We get the Minimum distance point of the left side recursively. 0-midpoint
8.We get the Minimum distance on the right side recursively
midpoint+1-length
9.We get the min = min(left,right)
10. Get all the points in the strip by interating through the points and subtract midpoint-x<=min because we want all points that are are less or equal to midpoint
11. Add all these points into an array called strip
12. We iterate through the strip using a nested for loop to compare each point with the next 6 points
12a.In the left and right side of strip each point must be at least delta distance apart if it isnt then we would have found it earlier.There could also be less than 7 points so we can use the length of strip
13.We only interate i-i+6 because there can only be max of seven points to compare with
14. 


"""
#Accept array of tuples
def MDP2(coords):
    return MDP(sorted(coords, key=lambda p: p[0]))
def MDP(coords):
    n = len(coords)
    
    #Base case: Checks for points less than 3 
    if n <=3:
        return bruteForce(coords)
    
    #Gets the minimum distance for points of both the right and left side
    midpoint = n//2
    leftmin = MDP(coords[0:midpoint])
    rightmin = MDP(coords[midpoint:n])

    #gets the points that fit within the strip abs(mid-point_x)<=min
    curr_min = min(leftmin,rightmin)
    strip = []
    for coord in coords:
        if abs(coords[midpoint][0]-coord[0])<=curr_min:
            strip.append(coord)
    strip = sorted(strip, key = lambda p:p[1])
    for i in range(0,len(strip)-1):
        for j in range(i+1,min(i+8,len(strip))):
            curr_min = min(distance(strip[i],strip[j]), curr_min)
    
    return curr_min

#Accepts two tuples
def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

#Base Case
def bruteForce(coords):
    minDis = float('inf')
    if len(coords) == 1:
        return minDis
    for i in range(0,len(coords)-1):
        for j in range(i+1,len(coords)):
            minDis = min(distance(coords[i],coords[j]),minDis)
    return minDis