from qgis.core import *
from PyQt4.QtCore import *
from TestUtils import *

class TopologyCorrector:
    def __init__(self, originalLayer, newLayer, errorLayer):
        self.originalLayer = originalLayer
        self.newLayer = newLayer
        self.errorLayer = errorLayer

    def correct(self):
        self.fillGaps()
        self.cutOverlaps()

    def fillGaps(self):
        backgroundGeometry = self.createBackgroundGeometry()
        layerFromGeom(backgroundGeometry, "background")
        gaps = self.createGaps(backgroundGeometry)
        #layerFromGeomList(gaps, "gaps")
        if len(gaps) > 0:
            self.mergeGaps(gaps)

    def createBackgroundGeometry(self):
        geometries = []
        for f in self.originalLayer.getFeatures():
            geom = f.geometryAndOwnership()
            geometries.append(geom)
        union = QgsGeometry.unaryUnion(geometries)
        box = QgsGeometry.fromRect(union.boundingBox())
        return box.buffer(10, 1)

    def createGaps(self, background):
        gaps = []
        errors = []
        multiGap = QgsGeometry(background)
        for f in self.newLayer.getFeatures():
            geom = f.geometry()
            if geom.isGeosValid():
                multiGap = multiGap.difference(geom)
            else:
                errors.append(f)
        #layerFromGeom(multiGap, 'multigap')
        for g in multiGap.asMultiPolygon():
            gap = QgsGeometry.fromPolygon(g)
            centroid = gap.centroid()
            for f in self.originalLayer.getFeatures():
                if f.geometry().contains(centroid):
                    gaps.append(gap)
                    break
        max = gaps[0]
        for gap in gaps:
            if gap.boundingBox().height() > max.boundingBox().height():
                max = gap
        gaps.remove(max)
        self.errorLayer.dataProvider().addFeatures(errors)
        return gaps

    def mergeGaps(self, gaps):
        for gap in gaps:
            self.mergeGap(gap)

    def mergeGap(self, gap):
        maximumIntersectionArea = 0.0
        maximumIntersectionId = -1
        for f in self.originalLayer.getFeatures():
            geom = f.geometry()
            intersection = geom.intersection(gap)
            if (intersection.area() > maximumIntersectionArea):
                maximumIntersectionArea = intersection.area()
                maximumIntersectionId = f.id()
        if maximumIntersectionId != -1:
            feature = self.newLayer.getFeatures(QgsFeatureRequest(maximumIntersectionId + 1)).next()
            mergedGeometry = QgsGeometry.unaryUnion([feature.geometry(),gap.buffer(0.01, 0)])
            self.newLayer.dataProvider().changeGeometryValues({ maximumIntersectionId + 1 : mergedGeometry })

    def cutOverlaps(self):
        overlaps = self.createOverlaps()
        #layerFromGeomList(overlaps, 'overlaps')
        features = []
        for f in self.newLayer.getFeatures():
            features.append(f)
        for i in range(len(features)):
            geom1 = features[i].geometry()
            for j in range(i+1,len(features)):
                geom2 = features[j].geometry()
                inter = geom1.intersection(geom2)
                if inter.area() > 0.0:
                    for splitLine in geom2.asPolygon():
                        copyGeom = QgsGeometry(geom1)
                        result, newGeometries, topoTestPoints = copyGeom.splitGeometry(splitLine, False)
                        newGeoms = [copyGeom]
                        newGeoms += newGeometries
                        newGeom = self.getNewGeom(newGeoms)
                        geom1 = newGeom
                        self.newLayer.dataProvider().changeGeometryValues({ features[i].id() : newGeom })
                        self.newLayer.updateExtents()

    def createOverlaps(self):
        overlaps = []
        for f1 in self.newLayer.getFeatures():
            geom1 = f1.geometry()
            for f2 in self.newLayer.getFeatures():
                if f1.id() != f2.id():
                    geom2 = f2.geometry()
                    inter = geom1.intersection(geom2)
                    if inter.area() > 0.0:
                        for poli in inter.asMultiPolygon():
                            overlap = QgsGeometry.fromPolygon(poli)
                            overlaps.append(overlap)
        return overlaps

    def getNewGeom(self, newGeometries):
        maxArea = 0.0
        maxId = -1
        for i in range(len(newGeometries)):
            if newGeometries[i].area() > maxArea:
                maxArea = newGeometries[i].area()
                maxId = i
        return newGeometries[maxId]
