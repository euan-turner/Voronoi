## Voronoi
Various algorithms for creating a Voronoi diagram from a set of points in ***Python***.

A Voronoi diagram takes a set **S** of *n* points as input. For *n* ∈ **S**, the diagram contains a polygon, such that *n* is the closest point in **S** to any point in the polygon.

[Formal Definition](https://en.wikipedia.org/wiki/Voronoi_diagram#Formal_definition)

[](https://github.com/euan-turner/Voronoi/blob/main/images/diagram.png)

# Libraries
* shapely
* matplotlib
* random
* dataclasses
* pygame

# Pixels
Extremely slow method of checking each individual location

# Iterative Addition
Incrementally adding points, and updating the regions of existing points, until the entire set has been exhausted.
Time: O(n<sup>2</sup>)

# Divide and Conquer
Not started

# Fortune's Sweeping Line Algorithm
Not started
