from qgis.core import *
from PyQt4.QtCore import *
from GeneralizationAlgorithm import *
import math

class Whirlpool(GeneralizationAlgorithm):
    def simplifyPointList(self, pointList):
        epsilon = self.tolerance
        result = []
        cluster = []
        for i in range(len(pointList)-1):
            if self.distance(pointList[i], pointList[i+1]) < epsilon:
                cluster.append(QgsPoint(pointList[i][0], pointList[i][1]))
            else:
                if len(cluster) > 0:
                    gravityPoint = self.gravityOfCluster(cluster)
                    cluster = []
                    result.append(gravityPoint.asPoint())
                else:
                    result.append(pointList[i])
        return result

    def distance(self, point1, point2):
        Xa = point1[0]
        Ya = point1[1]
        Xb = point2[0]
        Yb = point2[1]
        return math.sqrt(math.pow(Xa - Xb, 2) + math.pow(Ya - Yb, 2))

    def gravityOfCluster(self, cluster):
        multiPoint = QgsGeometry.fromMultiPoint(cluster)
        return multiPoint.centroid()

