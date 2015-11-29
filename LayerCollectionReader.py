from qgis.core import *
from PyQt4.QtCore import *

class LayerCollectionReader:
    def __init__(self, iface):
        self.iface = iface

    def getLayerNames(self):
        layerNames = []
        for layer in self.iface.legendInterface().layers():
            if self.isValidLayerType(layer):
                layerNames.append(layer.name())
        return layerNames

    def getLayerByName(self, layerName):
        for layer in self.iface.legendInterface().layers():
            if layer.name() == layerName:
                return layer

    def isValidLayerType(self, layer):
        if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Polygon:
            return True
        return False


