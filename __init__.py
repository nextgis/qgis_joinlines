# -*- coding: utf-8 -*-
mVersion = "0.2.1"
def name():
  return "Join lines"
def description():
  return "Permanently join two intersecting or snapped lines"
def qgisMinimumVersion(): 
  return "1.0" 
def version():
  return mVersion
def authorName():
  return "Maxim Dubinin, sim@gis-lab.info"
def classFactory(iface):
  from joinlines import joinlines
  return joinlines(iface)
