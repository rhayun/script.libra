import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from libra.addon import ADDON
from libra.logger import log


def series_thread():
    try:
        import xbmc
        log.info("libra: starting series service")
        while not xbmc.abortRequested:
            b = 1

    except Exception, e:
        import xbmc
        import traceback
        map(xbmc.log, traceback.format_exc().split("\n"))
        raise
