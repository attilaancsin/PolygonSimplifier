from qgis.core import *
from PyQt4.QtCore import *
from GeneralizationAlgorithm import *
import math

class VisvalingamWhyatt(GeneralizationAlgorithm):
    def simplifyPointList(self, pointList):
        result = []
        i = 1
        while i < len(pointList) - 1:
            area = self.effectiveArea(pointList[i-1], pointList[i], pointList[i+1])
            if area > self.tolerance:
                result.append(pointList[i])
                i = i + 1
            else:
                pointList.pop(i)
        return result

    def effectiveArea(self, point1, point2, point3):
        p1 = QgsPoint(point1[0], point1[1])
        p2 = QgsPoint(point2[0], point2[1])
        p3 = QgsPoint(point3[0], point3[1])
        polygon = [[p1, p2, p3]]
        triangle = QgsGeometry.fromPolygon(polygon)
        return triangle.area()

