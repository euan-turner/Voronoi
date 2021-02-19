import pygame,random,Classes,shapely.ops
from shapely.geometry import Point,Polygon,LineString

 
##Find new pairs of zones in a list, order pair from left to right
##Takes last list item and pairs with all previous items
def findPairs(arr):
    pairs = []
    lastItem = arr[-1]
    
    for i in range(0,len(arr)-1):
        if lastItem.point.x < arr[i].point.x:
            pairs.append((lastItem,arr[i]))
        else:
            pairs.append((arr[i],lastItem))
    return pairs

##Create a random point, ensure it is unique, return zone instance
def randomPoint(window,radius,zones):

    ##Define random colours for circle and zone
    mainColour = (255,255,255)
    secColour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))


    ##Ensure point is unique
    cont = False
    while not cont:
        cont = True
        centre = (random.randint(5,window.get_width()-5),random.randint(5,window.get_height()-5))
        for z in zones:
            ##Points may be vertical or horizontally aligned, but not identical
            if z.point.x == centre[0] and z.point.y == centre[1]:
                cont = False

    point = Classes.Zone(centre,mainColour,secColour,window)
    point.drawPoint(window,radius)
    return point

##Create and construct bisectors for new pairs of points, returns list of new bisectors
def createBisectors(window,pairs):
    newBisectors = []
    for pair in pairs:
        leftZone,rightZone = pair[0],pair[1]

##      ##Black line connecting points - removed for final
##        pygame.draw.aaline(window,(0,0,0),leftZone.point.coords[:][0],rightZone.point.coords[:][0],1)

        ##Co-ordinates of midpoint
        midX = int(round((leftZone.point.x + rightZone.point.x)/2))
        midY = int(round((leftZone.point.y + rightZone.point.y)/2))

####      ##Black midpoint - removed for final
##        pygame.draw.circle(window,(0,0,0),(midX,midY),3,0)

        ##Finding the bisector

        ##Calculating bisector gradient

        ##Vertical gradient -> point.x
        if leftZone.point.x == rightZone.point.x:
            ##Start point
            x0 = (0,midY)
            ##End point
            xW = (window.get_width(),midY)
            m = '~'
            c = '-'

        ##Horizontal gradient -> point.y
        elif leftZone.point.y == rightZone.point.y:
            ##Start point
            x0 = (midX,0)
            ##End point
            xW = (midX,window.get_height())
            m = 0
            c = midX

        ##Positive or negative gradient
        else:
            ##Original gradient
            origM = (rightZone.point.y - leftZone.point.y)/(rightZone.point.x - leftZone.point.x)
            ##Perpendicular gradient
            m = -(origM**-1)

            ##Finish formula by finding by y-intercept
            c = midY - (midX*m)
                
            ##Start point
            x0 = (0,int(round(c)))
            ##End point
            xW = (window.get_width(),int(round((m*window.get_width())+c)))
            
        
        line = Classes.Bisector(x0,xW,pair,(midX,midY),m,c)
        pair[0].bisectors.append(line)
        pair[1].bisectors.append(line)

##      ##Draw bisector - remove for final
##        line.drawBisector(window)
        newBisectors.append(line)
    
    return newBisectors

##Takes an unordered set of points defining a polygon (lines would cross)
##and sorts thems
def orderPoints(points):
    line = LineString(points)
    poly = line.convex_hull
        
    
    return poly.exterior.coords[:][:-1]
       

##Function to return new subcells from an old Polygon and an intersecting bisector
##polygon is a shapely Polygon instance and bi is a Bisector instance
def createSubcells(polygon,bi):

    newCells = shapely.ops.split(polygon,bi.line)
    return newCells[0],newCells[1]
    
            
            

    
        
            
            
        


    
