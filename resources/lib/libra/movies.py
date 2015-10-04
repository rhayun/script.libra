import os
import sys
import re
import xbmc
import json
import urllib

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

from libra import common
from libra.addon import ADDON_NAME
from libra.logger import log


class Movies:

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
            if not lib == []:
                raise Exception()
            return self.strm_file({'name': name, 'title': title, 'year': year, 'imdb': imdb})
        except:
            return False

    def strm_file(self, i):
        try:
            name, title, year, imdb = i['name'], i['title'], i['year'], i['imdb']

            sysname, systitle = urllib.quote_plus(name), urllib.quote_plus(title)

            transname = name.translate(None, "\/:*?&'`<>|").strip('.')

            content = 'plugin://script.libra/?action=play&name=%s&title=%s&year=%s&imdb=%s' % (sysname, systitle, year, imdb)

            common.makeFile(self.library_folder)
            folder = os.path.join(self.library_folder, transname)
            if common.fileExists(folder + "/"):
                return False
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
            strmfile = common.openFile(stream, 'w')
            strmfile.write(str(content))
            strmfile.close()

            nfo_stream = os.path.join(folder, transname + '.nfo')
            nfofile = common.openFile(nfo_stream, 'w')
            nfocontent = "http://www.imdb.com/title/%s" % imdb
            nfofile.write(str(nfocontent))
            nfofile.close()
        except:
            return False

        print "Create %s" % stream
        return True


class MoviesThread:
    def __init__(self):
        self.property = '%s_service_property' % ADDON_NAME.lower()

    def thread(self):
        try:
            import xbmc
            from resources.lib.indexers import ktuvit

            update_rate = common.get_setting("movie_update_rate")
            update_rate_hours = 24 # every day
            if update_rate == 1:
                update_rate_hours *= 7  # once a week
            elif update_rate == 2:
                update_rate_hours *= 30  # once a month

            # Check last run for each service
            last_run = self.last_run()

            try:
                common.window.setProperty(self.property, last_run)
            except:
                return

            service_property = common.window.getProperty(self.property)
            import datetime
            t1 = datetime.timedelta(hours=update_rate_hours)
            t2 = datetime.datetime.strptime(service_property, '%Y-%m-%d %H:%M:%S.%f')
            t3 = datetime.datetime.now()

            check = abs(t3 - t2) > t1
            if check is not False:
                log.info("libra: starting movies service")
                service_property = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                common.window.setProperty(self.property, service_property)

                try:
                    dbcon = database.connect(common.libraDbFile)
                    dbcur = dbcon.cursor()
                    dbcur.execute("CREATE TABLE IF NOT EXISTS service (""setting TEXT, ""value TEXT, ""UNIQUE(setting)"");")
                    dbcur.execute("DELETE FROM service WHERE setting = 'last_run__movies'")
                    dbcur.execute("INSERT INTO service Values (?, ?)", ('last_run__movies', service_property))
                    dbcon.commit()
                    dbcon.close()
                except:
                    try:
                        dbcon.close()
                    except:
                        pass

                ktuvit = ktuvit.Ktuvit()
                page = 1
                added = 0
                while page <= ktuvit.ktuvit_total_pages or added < 32: # need to be replace with setting
                    if xbmc.abortRequested:
                        return sys.exit()

                    movies = ktuvit.get_movies(page=page)
                    if movies:
                        for movie in movies:
                            if not self.is_valid_year(movie['year']):
                                continue
                            if not self.is_valid_genre(movie['genres']):
                                continue
                            if not self.is_valid_rating(movie['rating']):
                                continue
                            success = Movies().add(re.sub("#039;", "", movie['name']), movie['title'], movie['year'], movie['imdbid'])
                            if success is True:
                                added += 1

                    if added > 32 or page > 32:
                        break;
                    page += 1
            common.execute('UpdateLibrary(video)')
        except:
            return

    def last_run(self):
        last_run_date = "1970-01-01 23:59:00.000000"
        try:
            dbcon = database.connect(common.libraDbFile)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS service (""setting TEXT, ""value TEXT, ""UNIQUE(setting)"");")
            dbcur.execute("SELECT * FROM service WHERE setting = 'last_run__movies'")
            fetch = dbcur.fetchone()
            if fetch is None:
                dbcur.execute("INSERT INTO service Values (?, ?)", ('last_run__movies', last_run_date))
                dbcon.commit()
            else:
                last_run_date = str(fetch[1])
            dbcon.close()
        except:
            pass
        return last_run_date

    def is_valid_year(self, year):
        return int(common.get_setting('movie_year_from')) <= int(year) <= int(common.get_setting('movie_year_to'))

    def is_valid_rating(self, rating):
        return float(common.get_setting('movie_rating_from')) <= float(rating) <= float(common.get_setting('movie_rating_to'))

    def is_valid_genre(self, genres):
        valid = False
        if common.get_setting('mg_all') == 'true':
            valid = True
        else:
            for genre in genres:
                genre = re.sub('\s-\.', '_', genre.strip())
                if common.get_setting('mg_' + genre.lower()) == 'true':
                    valid = True
                    break
        return valid


def movies_thread():
    while not xbmc.abortRequested:
        indicator = os.path.join(common.dataPath, 'settings.xml')
        if common.fileExists(indicator):
            MoviesThread().thread()
        xbmc.sleep(60000)
