    ##Get polygon defining points
    boundPoints = polygon.exterior.coords[:][:-1]
    ##Points of intersection with the polygon
    interPoints = bi.line.intersection(polygon).coords[:]
 
    ##Find distinct polygon bound points - i.e. only present in one resulting subcell
    distinctBounds = [p for p in boundPoints if p not in interPoints]

    ##Y-value is less than it should be (X-value for vertical bisector)
    polya = list(interPoints)
    ##Y-value is greater than it should be (X-value for vertical bisector)
    polyb = list(interPoints)

    ##Define new subcell bounding points
    for b in distinctBounds:
        ##Determine which subcell the bounding points belongs to

        ##Horizontal bisector
        if bi.m == '~':
            yVal = bi.line.coords[:][0][1]
            if b[1] < yVal:
                polya.append(b)
            else:
                polyb.append(b)

        ##Vertical bisector
        elif bi.m == 0:
            xVal = bi.line.coords[:][0][0]
            if b[0] < xVal:
                polya.append(b)
            else:
                polyb.append(b)

        ##Slanted bisector
        else:
            yVal = (b[0]*bi.m)+bi.c
            if b[1] < yVal:
                polya.append(b)
            else:
                polyb.append(b)

    ##Order points
    if len(polya) < 3:
        print("Above")
        print("A: ",polya,"B: ",polyb,"\t",polygon.exterior.coords[:][:-1],"\t",bi.m,bi.c,bi.line.coords[:])
    elif len(polyb) < 3:
        print("Below")
        print("B: ",polyb,"A: ",polya,"\t",polygon.exterior.coords[:][:-1],"\t",bi.m,bi.c,bi.line.coords[:])
    polya = orderPoints(polya)
    polyb = orderPoints(polyb)

    return Polygon(polya),Polygon(polyb)
