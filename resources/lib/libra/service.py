import threading
import xbmc
from libra.logger import log
from libra.movies import movies_thread
from libra.series import series_thread


def run():

    threads = [
        threading.Thread(target=movies_thread),
        threading.Thread(target=series_thread),
    ]
    for t in threads:
        t.daemon = True
        t.start()


    # XBMC loop
    while not xbmc.abortRequested:
        xbmc.sleep(1000)

    log.info("libra: exiting libra services")
