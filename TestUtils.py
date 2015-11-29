from qgis.core import *
from PyQt4.QtCore import *

def layerFromGeom(geometry, name):
    layer = QgsVectorLayer('Polygon?crs=epsg:4326&index=yes', 'simplified', 'memory')
    feat = QgsFeature()
    feat.setGeometry(geometry)
    layer.dataProvider().addFeatures([feat])
    QgsVectorFileWriter.writeAsVectorFormat(layer, 'C:\Users\Attila\Documents\\test\\'+name+'.shp', 'CP1250', None)

def layerFromLayer(layer, name):
    QgsVectorFileWriter.writeAsVectorFormat(layer, 'C:\Users\Attila\Documents\\test\\'+name+'.shp', 'CP1250', None)

def layerFromGeomList(list, name):
    layer = QgsVectorLayer('Polygon?crs=epsg:4326&index=yes', 'simplified', 'memory')
    features = []
    for geom in list:
        feat = QgsFeature()
        feat.setGeometry(geom)
        features.append(feat)
    layer.dataProvider().addFeatures(features)
    QgsVectorFileWriter.writeAsVectorFormat(layer, 'C:\Users\Attila\Documents\\test\\'+name+'.shp', 'CP1250', None)

