# -*- coding: utf-8 -*-
from __future__ import absolute_import
mVersion = "0.2.4"
def name():
  return "Join lines"
def description():
  return "Permanently join two intersecting or snapped lines"
def category():
  return "Vector"
def qgisMinimumVersion():
  return "1.0"
def version():
  return mVersion
def authorName():
  return "Maxim Dubinin, sim@gis-lab.info"
def icon():
  return "icon.png"
def classFactory(iface):
  from .joinlines import joinlines
  return joinlines(iface)
