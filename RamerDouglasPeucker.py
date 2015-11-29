from qgis.core import *
from PyQt4.QtCore import *
from GeneralizationAlgorithm import *
import math

"""Represents an object that implements the well-known Ramer-Douglas-Peucker generalization algorithm."""
class RamerDouglasPeucker(GeneralizationAlgorithm):
    def simplifyPointList(self, pointList):
        """Recursively simplifies a point list."""
        dmax = 0
        index = 0
        end = len(pointList)
        for i in range(1, end - 1):
            d = self.distanceToSegment(pointList[i], pointList[0], pointList[end - 1])
            if d > dmax:
                index = i
                dmax = d
        if dmax > self.tolerance:
            result1 = self.simplifyPointList(pointList[:(index+1)])
            result2 = self.simplifyPointList(pointList[index:])
            result = result1[0:len(result1)-1] + result2
        else:
            result = [pointList[0], pointList[end - 1]]
        return result

    def distanceToSegment(self, point, lineStart, lineEnd):
        """Calculates the distance of a point from a specified line segment."""
        v = [lineEnd.x() - lineStart.x(), lineEnd.y() - lineStart.y()]  # direction vector
        n = [-v[1], v[0]]                                           # normal vector
        A = n[0]
        B = n[1]
        C = -(A * lineEnd.x() + B * lineEnd.y())
        numerator = math.fabs(A * point.x() + B * point.y() + C)
        denominator = math.sqrt(math.pow(A, 2) + math.pow(B, 2))
        return numerator / denominator

