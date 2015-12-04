# PolygonSimplifier
PolygonSimplifier is a QGIS plugin written in python. It can simplify polygons using the Ramer-Douglas-Peucker, the Visvalingam-Whyatt or the Whirlpool generalization algorithms. It is capable of preserving the topology during generalization.
## How to use it
Install the plugin and start using it from the toolbar with the Simplify polygons icon. The plugin can be started from the Modules menu too.
In the appearing dialog, just select a vector layer, choose a generalization algorithm, add some generalization parameters and click to OK to see the results. If you want topology to be preserved, just turn on the Preserve topology option.
Tip: If you don't see any result, try to adjust the generalization parameter significantly.

![screenshot](https://github.com/attilaancsin/PolygonSimplifier/blob/master/screenshot.PNG)
