import json
from resources.lib import client


class tvdb:

    def __init__(self, imdbid):

        self.imdbid = imdbid

        self.tvdb_data = {}
        if not imdbid.startswith("tt"):
            self.imdbid = "tt%s" % self.imdbid
        self.tvdb_link = "http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s" % imdbid

        try:
            self.tvdb_data = client.request(self.tvdb_link)
        except Exception, e:
            import xbmc
            import traceback
            map(xbmc.log, traceback.format_exc().split("\n"))
            raise


    def get_imdbid(self, digits=False):
        return self.imdbid if digits == False else self.imdbid[2:]

    
    def get_seriesid(self):
        try:
            return client.parseDOM(self.tvdb_data, 'seriesid')[0]
        except:
            return False


    def get_series_name(self):
        try:
            return client.parseDOM(self.tvdb_data, 'SeriesName')[0]
        except:
            return False



    def get_year(self):
        try:
            first_aired = client.parseDOM(self.tvdb_data, 'FirstAired')[0]
            return first_aired.split("-")[0] 
        except:
            return False

