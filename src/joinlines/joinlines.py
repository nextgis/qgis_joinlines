import os
from os import path
from typing import Optional

from qgis.core import (
    QgsApplication,
    QgsDistanceArea,
    QgsFeatureRequest,
    QgsGeometry,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QCoreApplication, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox

from . import about_dialog


class joinlines:
    def __init__(self, iface):
        """Initialize the class"""
        self.iface = iface
        self.plugin_dir = path.dirname(__file__)
        self._translator = None
        self.__init_translator()

    def initGui(self):
        self.action = QAction(
            QIcon(path.join(self.plugin_dir, "icon.png")),
            self.tr("Join two lines"),
            self.iface.mainWindow(),
        )
        self.action.setWhatsThis(self.tr("Permanently join two lines"))
        self.action.setStatusTip(
            self.tr(
                "Permanently join two lines (removes lines used for joining)"
            )
        )

        self.action.triggered.connect(self.run)

        self.actionAbout = QAction(
            self.tr("About"),
            self.iface.mainWindow(),
        )

        self.actionAbout.triggered.connect(self.about)

        self.iface.addVectorToolBarIcon(self.action)
        self.iface.addPluginToVectorMenu(
            self.tr("&Join two lines"), self.action
        )
        self.iface.addPluginToVectorMenu(
            self.tr("&Join two lines"), self.actionAbout
        )

    def unload(self):
        self.iface.removeVectorToolBarIcon(self.action)
        self.iface.removePluginVectorMenu(
            self.tr("&Join two lines"), self.action
        )
        self.iface.removePluginVectorMenu(
            self.tr("&Join two lines"), self.actionAbout
        )

        self.action.deleteLater()
        self.action = None
        self.actionAbout.deleteLater()
        self.actionAbout = None

    def about(self):
        dlg = about_dialog.AboutDialog(os.path.basename(self.plugin_dir))
        dlg.exec()

    def __init_translator(self):
        # initialize locale
        locale = QgsApplication.instance().locale()

        def add_translator(locale_path):
            if not path.exists(locale_path):
                return
            translator = QTranslator()
            translator.load(locale_path)
            QCoreApplication.installTranslator(translator)
            self._translator = translator  # Should be kept in memory

        add_translator(
            path.join(self.plugin_dir, "i18n", f"joinlines_{locale}.qm")
        )

    def run(self):
        cl = self.iface.activeLayer()
        # cl = self.iface.mapCanvas().currentLayer()
        if cl is None:
            infoString = self.tr("No layers selected")
            QMessageBox.information(
                self.iface.mainWindow(), self.tr("Warning"), infoString
            )
            return
        if not isinstance(cl, QgsVectorLayer):
            infoString = self.tr("Not a vector layer")
            QMessageBox.information(
                self.iface.mainWindow(), self.tr("Warning"), infoString
            )
            return
        if cl.geometryType() != QgsWkbTypes.GeometryType.LineGeometry:
            infoString = self.tr("Not a line layer")
            QMessageBox.information(
                self.iface.mainWindow(), self.tr("Warning"), infoString
            )
            return
        featids = cl.selectedFeatureIds()
        if len(featids) != 2:
            infoString = self.tr("Only two lines should be selected")
            QMessageBox.information(
                self.iface.mainWindow(), self.tr("Warning"), infoString
            )
            return
        selfeats = cl.selectedFeatures()
        geom0 = QgsGeometry(selfeats[0].geometry())
        geom1 = QgsGeometry(selfeats[1].geometry())

        # Find intersection point (not used!)
        # itspnt = QgsPoint(itsct.vertexAt(0))
        # if QgsPoint(itsct.vertexAt(1))!=QgsPoint(0,0):
        #   infoString = "Intersection contains more then 1 point"
        #   QMessageBox.information(self.iface.mainWindow(),"Warning",infoString)
        #   return
        itsct = geom1.intersection(geom0)
        itspnt = itsct.vertexAt(0)
        if not itsct.vertexAt(1).isEmpty():
            infoString = self.tr("Intersection contains more then 1 point")
            QMessageBox.information(
                self.iface.mainWindow(), "Warning", infoString
            )
            return

        # get first and last point for each line
        geom0.convertToSingleType()
        geom1.convertToSingleType()
        lastpointindex0 = len(geom0.asPolyline()) - 1
        lastpointindex1 = len(geom1.asPolyline()) - 1
        # lastpointindex0 = len(geom0.asMultiPolyline) - 1
        # lastpointindex1 = len(geom1.asMultiPolyline) - 1
        pnt00 = geom0.vertexAt(0)
        pnt01 = geom0.vertexAt(lastpointindex0)
        pnt10 = geom1.vertexAt(0)
        pnt11 = geom1.vertexAt(lastpointindex1)

        if itspnt != pnt00 and itspnt != pnt01:
            # create two lists of points
            pnts0 = geom0.asPolyline()
            pnts1 = geom1.asPolyline()

            # split first line
            (res, newlist, topolist) = geom1.splitGeometry(pnts0, False)
            if res == 1:  # split failed
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    self.tr("Join error"),
                    self.tr("Lines should have common point or intersection"),
                )
                return
            pnts = geom1.asPolyline()
            f = QgsDistanceArea()
            dist1 = f.measureLine(pnts)

            pnts = newlist[0].asPolyline()
            f = QgsDistanceArea()
            dist2 = f.measureLine(pnts)

            if dist1 > dist2:
                cl.changeGeometry(featids[0], geom1)

            if dist2 > dist1:
                cl.changeGeometry(featids[0], newlist[0])

            # split second line

            (res, newlist, topolist) = geom0.splitGeometry(pnts1, False)
            if res == 1:  # split failed
                QMessageBox.warning(
                    self.iface.mainWindow(),
                    self.tr("Join error"),
                    self.tr("Lines should have common point or intersection"),
                )
                return
            pnts = geom0.asPolyline()
            f = QgsDistanceArea()
            dist1 = f.measureLine(pnts)

            pnts = newlist[0].asPolyline()
            f = QgsDistanceArea()
            dist2 = f.measureLine(pnts)

            if dist1 > dist2:
                cl.changeGeometry(featids[1], geom0)

            if dist2 > dist1:
                cl.changeGeometry(featids[1], newlist[0])

            # Get new geometries back

            request = QgsFeatureRequest().setFilterFids(featids)
            features = [feat for feat in cl.getFeatures(request)]

            f0 = features[0]
            geom0 = QgsGeometry(f0.geometry())

            f1 = features[1]
            geom1 = QgsGeometry(f1.geometry())

            # get first and last point for each line
            lastpointindex0 = len(geom0.asPolyline()) - 1
            lastpointindex1 = len(geom1.asPolyline()) - 1
            pnt00 = geom0.vertexAt(0)
            pnt01 = geom0.vertexAt(lastpointindex0)
            pnt10 = geom1.vertexAt(0)
            pnt11 = geom1.vertexAt(lastpointindex1)

        # combine two lines based on 4 possible cases
        respnts = []
        if pnt00 == pnt10:
            pnts1res = geom0.asPolyline()
            pnts1res.reverse()
            respnts = geom1.asPolyline()
            del respnts[0]
            pnts1res.extend(respnts)
            respnts = pnts1res

        if pnt00 == pnt11:
            pnts1res = geom0.asPolyline()
            respnts = geom1.asPolyline()
            del pnts1res[0]
            respnts.extend(pnts1res)

        if pnt01 == pnt10:
            pnts1res = geom0.asPolyline()
            respnts = geom1.asPolyline()
            del respnts[0]
            pnts1res.extend(respnts)
            respnts = pnts1res

        if pnt01 == pnt11:
            pnts1res = geom0.asPolyline()
            respnts = geom1.asPolyline()
            respnts.reverse()
            del respnts[0]
            pnts1res.extend(respnts)
            respnts = pnts1res

        newgeom = QgsGeometry.fromPolylineXY(respnts)

        # selfeats[0].setGeometry(newgeom)
        # curLayer.commitChanges()
        cl.startEditing()
        cl.beginEditCommand(self.tr("Join selected lines"))
        cl.changeGeometry(featids[0], newgeom)
        cl.endEditCommand()
        cl.beginEditCommand(self.tr("Delete feature"))
        cl.deleteFeature(featids[1])
        cl.endEditCommand()
        self.iface.mapCanvas().refresh()

    def tr(
        self,
        source_text: str,
        disambiguation: Optional[str] = None,
        n: int = -1,
    ) -> str:
        return QgsApplication.translate(
            "joinlines", source_text, disambiguation, n
        )
