import pygame
from shapely.geometry import Point,Polygon,LineString
 
##Zone class for point colour, area colour, centre point, drawing funcs
class Zone():

    def __init__(self,centre,mainColour,secColour,window):
        self.point = Point(centre)
        self.main = mainColour
        self.sec = secColour
        self.points = [(0,0),(window.get_width(),0),(window.get_width(),window.get_height()),(0,window.get_height())]
        self.polygon = Polygon(self.points)
        self.bisectors = []

    def __str__(self):
        return point.coords
        
    def drawPoint(self,window,radius):
        pygame.draw.circle(window,self.main,self.point.coords[:][0],radius,0)

    def drawZone(self,window):
        pygame.draw.polygon(window,self.sec,self.polygon.exterior.coords,0)
        pygame.draw.polygon(window,(0,0,0),self.polygon.exterior.coords,1)
        
    def updatePolygon(self):
        self.polygon = Polygon(self.points)

##Bisector class for LineString instance, colour, parent points, origin point, gradient
class Bisector():

    def __init__(self,start,end,parents,origin,gradient,intercept):
        self.colour = (0,255,0)
        self.line = LineString([start,end])
        self.parents = parents
        self.origin = origin
        self.m = gradient
        self.c = intercept

    def drawBisector(self,window):
        pygame.draw.aaline(window,self.colour,self.line.coords[0],self.line.coords[1],1)

        
        
