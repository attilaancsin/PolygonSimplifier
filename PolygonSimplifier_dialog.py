# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PolygonSimplifierDialog
                                 A QGIS plugin
 Simplifies polygons with preserving topology.
                             -------------------
        begin                : 2015-08-08
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Attila Ancsin
        email                : attilaancsin@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QFileDialog, QMessageBox
from LayerCollectionReader import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'PolygonSimplifier_dialog_base.ui'))


class PolygonSimplifierDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(PolygonSimplifierDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        # Connecting slots.
        self.browseButton.clicked.connect(self.showBrowserDialog)
        self.preserveTopology.stateChanged['int'].connect(self.enableMinimumPolygonSize)
        self.algorithms.currentIndexChanged['QString'].connect(self.changeToleranceLabelText)

    def showBrowserDialog(self):
        """Shows a file browser dialog to enter the output path."""
        fileName = QFileDialog.getSaveFileName(None, 'Save output shapefile','','Shapefiles (*.shp *.SHP)')
        self.outputPath.setText(fileName)

    def enableMinimumPolygonSize(self, state):
        """Enables the Minimum polygon size checkbox according to the specified state."""
        if state == 2:
            self.minimumPolygonSize.setEnabled(False)
        else:
            self.minimumPolygonSize.setEnabled(True)

    def changeToleranceLabelText(self, algorithmName):
        if algorithmName == "Ramer-Douglas-Peucker":
            self.toleranceLabel.setText("Epsilon value:")
        if algorithmName == "Visvalingam-Whyatt":
            self.toleranceLabel.setText("Area threshold:")
        if algorithmName == "Whirlpool":
            self.toleranceLabel.setText("Neighbour distance:")

    def loadLayers(self, iface):
        """Reads currently loaded layers from QGIS"""
        self.iface = iface
        self.layerCollectionReader = LayerCollectionReader(self.iface)
        self.layers.clear()
        self.layers.addItems(self.layerCollectionReader.getLayerNames())
        # Return true if any layer is loaded.
        if self.layers.count() > 0:
            return True
        else:
            return False

    def getSelectedLayer(self):
        """Returns the layer object according to the selected layer name on the dialog."""
        layerName = self.layers.currentText()
        selectedLayer = self.layerCollectionReader.getLayerByName(layerName)
        return selectedLayer
