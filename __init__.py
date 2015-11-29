# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PolygonSimplifier
                                 A QGIS plugin
 Simplifies polygons with preserving topology.
                             -------------------
        begin                : 2015-08-08
        copyright            : (C) 2015 by Attila Ancsin
        email                : attilaancsin@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PolygonSimplifier class from file PolygonSimplifier.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .PolygonSimplifier import PolygonSimplifier
    return PolygonSimplifier(iface)
