import xbmc, xbmcaddon, xbmcgui, xbmcplugin, json, urllib, os, sys

from libra import common
from libra.addon import ADDON
from libra.logger import log


class movies:

    def __init__(self):
        self.library_folder = os.path.join(common.transPath(common.get_setting('movie_library')),'')


    def add(self, name, title, year, imdb):
        try:
            id = [imdb,]
            lib = common.jsonrpc('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["imdbnumber", "originaltitle", "year"]}, "id": 1}' % (year, str(int(year)+1), str(int(year)-1)))
            lib = unicode(lib, 'utf-8', errors='ignore')
            lib = json.loads(lib)['result']['movies']
            lib = [i for i in lib if str(i['imdbnumber']) in id or (i['originaltitle'].encode('utf-8') == title and str(i['year']) == year)][0]
        except:
            lib = []

        try:
            if not lib == []: raise Exception()
            self.strmFile({'name': name, 'title': title, 'year': year, 'imdb': imdb})
        except:
            pass

        common.execute('UpdateLibrary(video)')


    def strmFile(self, i):
        try:
            name, title, year, imdb = i['name'], i['title'], i['year'], i['imdb']

            sysname, systitle = urllib.quote_plus(name), urllib.quote_plus(title)

            transname = name.translate(None, '\/:*?&"<>|').strip('.')

            content = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s' % (sys.argv[0], sysname, systitle, year, imdb)

            common.makeFile(self.library_folder)
            folder = os.path.join(self.library_folder, transname)
            common.makeFile(folder)

            try:
                if not 'ftp://' in folder: raise Exception()
                from ftplib import FTP
                ftparg = re.compile('ftp://(.+?):(.+?)@(.+?):?(\d+)?/(.+/?)').findall(folder)
                ftp = FTP(ftparg[0][2],ftparg[0][0],ftparg[0][1])
                try: ftp.cwd(ftparg[0][4])
                except: ftp.mkd(ftparg[0][4])
                ftp.quit()
            except:
                pass

            stream = os.path.join(folder, transname + '.strm')
            file = common.openFile(stream, 'w')
            file.write(str(content))
            file.close()
        except:
            pass


def movies_thread():
    try:
        import xbmc
        log.info("libra: starting movies service")
        while not xbmc.abortRequested:
            a = 1

    except Exception, e:
        import xbmc
        import traceback
        map(xbmc.log, traceback.format_exc().split("\n"))
        raise