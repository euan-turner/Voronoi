import numpy as np
import matplotlib.pyplot as plt
import shapely
import random

from matplotlib.collections import PolyCollection
from shapely.geometry import Polygon, Point, LineString, box
from shapely.ops import split
from dataclasses import dataclass


##Associate Voronoi regions with parent points
@dataclass
class Point_Region:
    point : Point
    region : Polygon


def create_points(max_x : int, max_y : int, n : int) -> list:
    """
    Generate a set of random points constrained to the rectangle
    (0,0) , (max_x,0), (max_x,max_y), (0,max_y)

    Parameters
    ----------
    max_x: maximum x co-ordinate
    max_y: maximum y co-ordinate
    n: number of points

    Returns
    -------
    list of shapely Point instances
    """
    points = []
    for _ in range(n):
        x = random.randint(0,max_x)
        y = random.randint(0,max_y)
        p = Point((x,y))
        points.append(p)

    return points

def voronoi(points : list, bound_poly : Polygon):
    """
    Create the voronoi diagram for a set of points, within a bounded area

    Parameters
    ----------
    points: list of shapely Point instances, to create the diagram from
    bound_poly: the bounding polygon, to prevent regions extending to infinity - a rectangle

    Returns
    -------
    list of Point_Region instances
    """

    point_regions = []

    for point in points:
        ##Cells which will compose the new polygon
        cells = []
        ##Update all formed regions under influence of new point
        for prev_pr in point_regions:
            ##Create bisector of two points - bound_poly is a rectangle, so max(coords) gives dimensions
            bisector = perp_bisector(point, prev_pr.point, max(bound_poly.exterior.coords[:]))
            if len(bisector.intersection(prev_pr.region).coords[:]) > 1:
                cell1, cell2 = split(prev_pr.region, bisector)
            # ##Check if bisector intersects previous region
            # if bisector.intersects(prev_pr.region):
            #     split_points = bisector.intersection(prev_pr.region)
            #     if len(split_points.coords[:]) > 1:
            #         cell1, cell2 = split(prev_pr.region, extend(split_points))
                    #print(prev_pr.region.exterior.coords[:])

                if prev_pr.point.within(cell1):
                    ##cell2 is removed from prev_pr
                    prev_pr.region = cell1
                    cells.append(cell2)
                elif prev_pr.point.within(cell2):
                    ##cell1 is removed from prev_pr
                    prev_pr.region = cell2
                    cells.append(cell1)
                

        if len(cells) == 0:
            ##Case for first point
            pr = Point_Region(point, bound_poly)
        else:
            ##Form convex hull of all assembled cells
            new_points = []
            for c in cells:
                new_points += c.exterior.coords[:][:-1]
            new_poly = LineString(new_points).convex_hull
            pr = Point_Region(point, new_poly)
        
        point_regions.append(pr)
    
    return point_regions



def perp_bisector(a : Point, b : Point, dims : (int,int)) -> LineString:
    """
    Find  the perpendicular bisector of two points, with end points on the bounding polygon

    Parameters
    ----------
    a,b: Points to bisect
    dims: the dimensions of the bounding polygon

    Returns
    -------
    shapely LineString
    """

    ax = a.x
    ay = a.y
    bx = b.x
    by = b.y
    mx = (ax+bx)/2
    my = (ay+by)/2

    ##Points are vertically aligned -> Bisector is horizontal
    if ax == bx:
        start = Point((0,my))
        end = Point((dims[0], my))
    ##Points are horizontally aligned -> Bisector is vertical
    elif ay == by:
        start = Point((mx,0))
        end = Point((mx,dims[1]))
    else:
        init_m = (by - ay) / (bx - ax)
        perp_m = - (1/init_m)
        c = my - (perp_m*mx)
        start = Point((0,c))
        end = Point((dims[0], dims[0]*perp_m + c))

    return LineString([start,end])

def extend(line : LineString) -> LineString:
    """
    Extend a LineString, to guard against accuracy errors

    Parameters
    ----------
    line: line to extend

    Returns
    -------
    LineString
    """
    coords = line.coords[:]
    p1 = list(coords[0])
    p2 = list(coords[1])
    deltax = abs(p2[0] - p1[0])
    deltay = abs(p2[1] - p1[1])
    if p1[0] < p2[0]:
        p1[0] -= 0.1*deltax
        p2[0] += 0.1*deltax
    else:
        p1[0] += 0.1*deltax
        p2[0] -= 0.1*deltax
    if p1[1] < p2[1]:
        p1[1] -= 0.1*deltay
        p2[1] += 0.1*deltay
    else:
        p1[1] += 0.1*deltay
        p2[1] -= 0.1*deltay
    return LineString([p1,p2])


def display(orig_points : list, voronoi_prs : list):
    """
    Display the original points, and the generated Voronoi diagram
    in adjacent subplots

    Parameters
    ----------
    orig_points: A list of the points used to create the Voronoi diagram
    voronoi_prs: A list of Points_Region instances

    """

    ##Plot original points
    x = [p.x for p in orig_points]
    y = [p.y for p in orig_points]

    fig = plt.figure(figsize = (8,8))
    
    for pr in voronoi_prs:
        plt.plot(pr.point.x, pr.point.y, 'ro')
        plt.plot(*pr.region.exterior.xy)
   

    plt.show()


original_points = create_points(250,250,20)
bound = box(0,0,250,250)
prs = voronoi(original_points, bound)
display(original_points, prs)
