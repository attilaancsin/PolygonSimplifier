from qgis.core import *
from PyQt4.QtCore import *
from TopologyCorrector import *

"""Represents an object that can run a specified simplifier algorithm."""
class SimplifierAlgorithmRunner:
    def __init__(self, algorithm):
        """Initializes a new instance of the SimplifierAlgorithmRunner class."""
        self.algorithm = algorithm

    def run(self, inputLayer, preserveTopology, minPolygonSize):
        """Runs simplifier algorithm on the specified layer then returns the result"""
        """in a new layer."""
        outputFeatureCollection = []

        # Simplify input features.
        for feature in inputLayer.getFeatures():
            simplifiedFeature = self.algorithm.simplify(feature)
            # Drop undersized polygons if needed.
            if not preserveTopology and simplifiedFeature.geometry().area() < minPolygonSize:
                continue
            outputFeatureCollection.append(simplifiedFeature)

        # Add simplified features to a new layer.
        outputLayer = self.createSimilarLayer(inputLayer, 'simplified')
        outputLayer.dataProvider().addFeatures(outputFeatureCollection)
        errorLayer = self.createSimilarLayer(inputLayer, 'errors')

        # Preserve topology if needed.
        if preserveTopology:
            topologyCorrector = TopologyCorrector(inputLayer, outputLayer, errorLayer)
            topologyCorrector.correct()

        return outputLayer, errorLayer

    def createSimilarLayer(self, inputLayer, name):
        """Creates a new layer that is similar to the specified input layer."""
        layer = QgsVectorLayer('Polygon?crs=epsg:4326&index=yes', name, 'memory')
        layer.dataProvider().addAttributes(inputLayer.pendingFields())
        layer.updateFields()
        return layer
