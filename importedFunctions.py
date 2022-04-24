# https://github.com/JuantAldea/Separating-Axis-Theorem/
# blob/master/python/separation_axis_theorem.py
# https://web.archive.org/web/20141127210836/
# http://content.gpwiki.org/index.php/Polygon_Collision
# https://textbooks.cs.ksu.edu/cis580/04-collisions/04-separating-axis-theorem/

from math import sqrt
from cmu_112_graphics import *

def normalize(vector):
    """
    :return: The vector scaled to a length of 1
    """
    norm = sqrt(vector[0] ** 2 + vector[1] ** 2)
    return vector[0] / norm, vector[1] / norm

def dot(vector1, vector2):
    """
    :return: The dot (or scalar) product of the two vectors
    """
    return vector1[0] * vector2[0] + vector1[1] * vector2[1]

def edge_direction(point0, point1):
    """
    :return: A vector going from point0 to point1
    """
    return point1[0] - point0[0], point1[1] - point0[1]

def orthogonal(vector):
    """
    :return: A new vector which is orthogonal to the given vector
    """
    return vector[1], -vector[0]

def vertices_to_edges(vertices):
    """
    :return: A list of the edges of the vertices as vectors
    """
    return [edge_direction(vertices[i], vertices[(i + 1) % len(vertices)])
            for i in range(len(vertices))]

def project(vertices, axis):
    """
    :return: A vector showing how much of the vertices lies along the axis
    """
    dots = [dot(vertex, axis) for vertex in vertices]
    return [min(dots), max(dots)]

def overlap(projection1, projection2):
    """
    :return: Boolean indicating if the two projections overlap
    """
    return min(projection1) <= max(projection2) and \
           min(projection2) <= max(projection1)

def separating_axis_theorem(vertices_a, vertices_b):
    edges = vertices_to_edges(vertices_a) + vertices_to_edges(vertices_b)
    axes = [normalize(orthogonal(edge)) for edge in edges]

    for axis in axes:
        projection_a = project(vertices_a, axis)
        projection_b = project(vertices_b, axis)

        overlapping = overlap(projection_a, projection_b)

        if not overlapping:
            return False

    return True

################################################################################

# https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

# https://pynative.com/python-delete-lines-from-file/
# #h-delete-all-lines-from-a-file

def truncate(path):
    with open(path, "wt") as f:
        f.truncate()

################################################################################

# https://www.geeksforgeeks.org/
# check-if-any-point-overlaps-the-given-circle-and-rectangle/

# Python3 implementation to check if any
# point overlaps the given Circle
# and Rectangle

# Function to check if any point
# overlaps the given Circle
# and Rectangle
def checkOverlap(R, Xc, Yc, X1, Y1, X2, Y2):

	# Find the nearest point on the
	# rectangle to the center of
	# the circle
	Xn = max(X1, min(Xc, X2))
	Yn = max(Y1, min(Yc, Y2))
	
	# Find the distance between the
	# nearest point and the center
	# of the circle
	# Distance between 2 points,
	# (x1, y1) & (x2, y2) in
	# 2D Euclidean space is
	# ((x1-x2)**2 + (y1-y2)**2)**0.5
	Dx = Xn - Xc
	Dy = Yn - Yc
	return (Dx**2 + Dy**2) <= R**2

################################################################################