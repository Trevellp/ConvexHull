# This class stores one single point with an x and y position.
# Each Point object just remembers where it is on a graph.
class Point:
    def __init__(self, x, y):
        self.x = x  # store the x position (left to right)
        self.y = y  # store the y position (up and down)

    # This makes it easier to print points in a nice readable format, like (1, 2)
    def __repr__(self):
        return f"({self.x}, {self.y})"


# This function checks which way three points turn.
# It helps us see if we are making a left turn, right turn, or going straight.
# A positive result means left turn (good for the hull).
# A negative result means right turn (goes inward, so we remove that point).
# A result of zero means the points are in a straight line.
def direction(a, b, c):
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


# This function builds the convex hull — the "fence" that goes around all the points.
# It uses a simple step-by-step method called the "monotone chain" algorithm.
def convex_hull(points):
    # First, we remove any exact duplicate points so we don’t process the same spot twice.
    uniq = {(p.x, p.y) for p in points}  # turns each point into a number pair
    pts = [Point(x, y) for (x, y) in uniq]  # make new Point objects without duplicates

    # If there’s only 0 or 1 point, the hull is just those points — nothing to build.
    if len(pts) <= 1:
        return pts

    # Sort the points from left to right (x value), and from bottom to top (y value).
    # Sorting helps us trace the boundary in an orderly way.
    pts.sort(key=lambda p: (p.x, p.y))

    # Now we build the "lower edge" of the hull (the bottom half).
    lower = []
    for p in pts:
        # While there are at least two points in the list,
        # check if adding the new one bends the line inward (right turn).
        # If it does, remove the last point — we only want outermost ones.
        # If you change <= to <, it will keep points that lie on straight edges.
        while len(lower) >= 2 and direction(lower[-2], lower[-1], p) <= 0:
            lower.pop()  # remove the inner point that causes a bend
        lower.append(p)  # add the new outer point

    # Next, we build the "upper edge" of the hull (the top half).
    upper = []
    for p in reversed(pts):  # we go backward to handle the top half
        while len(upper) >= 2 and direction(upper[-2], upper[-1], p) <= 0:
            upper.pop()  # remove inward bends again
        upper.append(p)

    # The first and last points of each edge are the same corner,
    # so we remove one copy from each to avoid repeating corners.
    # Then we combine both halves to make the full outline.
    return lower[:-1] + upper[:-1]


# This small demo runs if you start this file directly.
# It creates a few points and prints the convex hull around them.
if __name__ == "__main__":
    # These are our sample points.
    # You can picture them as dots on graph paper.
    # Some points are inside the shape, and some are corners of the hull.
    data = [
        Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2),  # corners of a square
        Point(1, 1), Point(1, 2), Point(0, 1), Point(2, 1),  # points inside the square
        Point(2, 2), Point(0, 0)  # duplicates added on purpose
    ]

    # Build the hull and print the result.
    hull = convex_hull(data)
    print("Hull:", hull)
