import pygame,Classes,Methods
from shapely.geometry import Point,Polygon,LineString
 
##Window set-up
w,h = 1000,500
window = pygame.display.set_mode((w,h))
window.fill((255,255,255))
pygame.display.set_caption('Voronoi Diagram')

zones = []
bisectorList = []
usedPairs = 0
zonePairs = []

##Window-bounding polygon
windowBounds = Polygon([(0,0),(w,0),(w,h),(0,h)])

##Original Point
zone = Methods.randomPoint(window,2,zones)
zones.append(zone)

for i in range(100):
    zone = Methods.randomPoint(window,2,zones)
    zones.append(zone)
    zonePairs += Methods.findPairs(zones)
    newBisectors = Methods.createBisectors(window,zonePairs[usedPairs::])
    bisectorList += newBisectors

    usedPairs = len(zonePairs)

    ##Specific change for second point
    if i == 0:
        ##Bisector of 1st and 2nd point
        bi = bisectorList[0]
        ##Other parent
        prevZone = zones[0]

        polya,polyb = Methods.createSubcells(prevZone.polygon,bi)



        ##Determine parentage of new polygons
        if zone.point.within(polya):
            zone.points = polya.exterior.coords[:][:-1]
            prevZone.points = polyb.exterior.coords[:][:-1]
        else:
            zone.points = polyb.exterior.coords[:][:-1]
            prevZone.points = polya.exterior.coords[:][:-1]

        ##Update zone polygons
        for zone in zones:
            zone.updatePolygon()
            
            
        
        
    
    else:
        ##Iterate through previous zones to check if they are affected by the new point
        ##Divide affected zones into pair of subcells and reallocate by centroids

        ##Polygon ubcells which will combine to form the polygon of the new points
        zoneCells = []
        
        ##Established zones
        for prev in zones[:-1]:

            ##Identify shared bisector of prev and zone
            bi = [b for b in prev.bisectors if b in zone.bisectors][0]

            ##Check for intersection with prev Polygon
            interPoints = bi.line.intersection(prev.polygon).coords[:]

            
            ##Check intersection with bisector does not occur along the edge of the polygon
            ##i.e. check intersection points(if they are defining coords of the polygon)
            ##are not adjacent in prev.polygon.coords
            ##edgeIntersectQ = [x for x in range(len(prev.polygon.exterior.coords[:][:-1])) if prev.polygon.exterior.coords[:][:-1][x:x+2] == interPoints or prev.polygon.exterior.coords[:][:-1][x-1:x+1] == list(reversed(interPoints))]
            
            
            ##Checking for more than 1 interPoint to prevent error when trying to make
            ##LineString from single co-ordinate
            if len(interPoints)>1:## and not(bool(edgeIntersectQ)):
                ##Divide polygon into two polygons
                polya,polyb = Methods.createSubcells(prev.polygon,bi)

                ##Determine parentage of new polygons

                ##Get centroid of new polygon A
                centroida = polya.centroid
    
                checkLine = LineString([centroida.coords[:][0],prev.point.coords[:][0]])

                ##If line intersects with bisector, polygon A belongs to new zone, vice versa
                parentQ = checkLine.intersection(bi.line)
                ##Intersection occurs, polya belongs to new zone
                if bool(parentQ):
                    zoneCells.append(polya)
                    prev.points = polyb.exterior.coords[:][:-1]
                    prev.updatePolygon()

                else:
                    zoneCells.append(polyb)
                    prev.points = polya.exterior.coords[:][:-1]
                    prev.updatePolygon()

        ##Convert zoneCells from a list of polygons to a list of all defining points
        zonePoints = []
        for c in zoneCells:
            zonePoints += c.exterior.coords[:][:-1]

        ##Get convex hull of subcells creating polygon for new cell
        newPolygon = LineString(zonePoints).convex_hull
        zone.points = newPolygon.exterior.coords[:][:-1]
        zone.updatePolygon()

        ##Draw new polygons on screen
        for z in zones:
            z.drawZone(window)
        for z in zones:
            z.drawPoint(window,2)

            
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    pygame.display.flip()            
                    
                
            
##Errors with some bisectors, check introduced checks for specific errors, e.g. intersections
##along a line

            
        
        
            

        
        
        
        
        
        
