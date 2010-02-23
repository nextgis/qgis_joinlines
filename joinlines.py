# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources

class joinlines:

  def __init__(self, iface):
    """Initialize the class"""
    self.iface = iface
  
  def initGui(self):
    self.action = QAction(QIcon(":/plugins/joinlines/icon.png"), "Join two lines", self.iface.mainWindow())
    self.action.setStatusTip("Permanently join two lines")
    
    QObject.connect(self.action, SIGNAL("activated()"), self.run)
    
    self.iface.addPluginToMenu("&Join two lines", self.action)
    
  def unload(self):
    self.iface.removePluginMenu("&Join two lines",self.action)
    self.iface.removeToolBarIcon(self.action)

  def run(self):
    layersmap=QgsMapLayerRegistry.instance().mapLayers()
    layerslist=[]
    curLayer = self.iface.mapCanvas().currentLayer()
    if (curLayer == None):
      infoString = QString("No layers selected")
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      return
    if (curLayer.type() <> curLayer.VectorLayer):
      infoString = QString("Not a vector layer")
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      return
    if curLayer.geometryType() <> QGis.Line: 
      infoString = QString("Not a line layer")
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      return
    featids = curLayer.selectedFeaturesIds()
    if (len(featids) != 2):
      infoString = QString("Only two lines should be selected")
      QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
      return
    selfeats = curLayer.selectedFeatures()
    geom0 = QgsGeometry(selfeats[1].geometry())
    geom1 = QgsGeometry(selfeats[0].geometry())
    
    i=0
    pnts=[]
    vertex=geom1.vertexAt(i)
    while (vertex!=QgsPoint(0,0)):
        apnt = QgsPoint(geom0.vertexAt(i))
        pnts.append(apnt)
        i+=1
        vertex=geom0.vertexAt(i)
    i=1
    vertex=geom1.vertexAt(i)
    while (vertex!=QgsPoint(0,0)):
        apnt = QgsPoint(geom1.vertexAt(i))
        pnts.append(apnt)
        i+=1
        vertex=geom1.vertexAt(i)
    
    newgeom = QgsGeometry.fromPolyline(pnts)
    #selfeats[0].setGeometry(newgeom)
    #curLayer.commitChanges()
    curLayer.deleteSelectedFeatures()
    feat = QgsFeature()
    feat.setGeometry(newgeom)
    pr=curLayer.dataProvider()
    pr.addFeatures([feat])
    self.iface.mapCanvas().refresh()