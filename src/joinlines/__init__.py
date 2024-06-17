# -*- coding: utf-8 -*-


def classFactory(iface):
    from .joinlines import joinlines

    return joinlines(iface)
