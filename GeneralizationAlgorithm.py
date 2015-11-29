from qgis.core import *
from PyQt4.QtCore import *
import math

"""Base class of a generalization algorithm."""
class GeneralizationAlgorithm:
    def __init__(self, tolerance):
        """Creates a new instance of the GeneralizationAlgorithm class with the specified tolerance value."""
        self.tolerance = tolerance

    def simplify(self, feature):
        """Simplifies the geometry of the specified feature. The returned feature is similar to the"""
        """simplified one, except its geometry."""
        geom = feature.geometry()
        # We handle Polygons and MultiPolygons differently.
        if geom.wkbType() == QGis.WKBPolygon:
            rings = []
            for pointList in geom.asPolygon():
                end = len(pointList)-1
                result = self.simplifyPointList(pointList[:end])
                result.append(pointList[0])
                if len(result) < 4:
                    rings.append(self.getBasePolygon(pointList))
                else:
                    rings.append(result)
            newGeometry = QgsGeometry.fromPolygon(rings)
        elif geom.wkbType() == QGis.WKBMultiPolygon:
            polygons = []
            for polygon in geom.asMultiPolygon():
                rings = []
                for pointList in polygon:
                    end = len(pointList)-1
                    result = self.simplifyPointList(pointList[:end])
                    result.append(pointList[0])
                    if len(result) < 4:
                        rings.append(self.getBasePolygon(pointList))
                    else:
                        rings.append(result)
                polygons.append(rings)
            newGeometry = QgsGeometry.fromMultiPolygon(polygons)
        newFeature = QgsFeature()
        newFeature.setAttributes(feature.attributes())
        newFeature.setFeatureId(feature.id())
        newFeature.setGeometry(newGeometry)
        return newFeature

    def simplifyPointList(self, pointList):
        return pointList

    def getBasePolygon(self, pointList):
        last = len(pointList)-1
        secondIndex = last / 4
        thirdIndex = secondIndex * 2
        return [pointList[0], pointList[secondIndex], pointList[thirdIndex], pointList[last]]
