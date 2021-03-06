import re
from resources.lib import client
from libra import cache


class Torec:
    def __init__(self):
        self.torec_link = 'http://www.torec.net/tv_series_subs.asp?p=%s'
        self.torec_series_link = 'http://www.torec.net/sub.asp?sub_id=%s'
        self.torec_items_per_page = 12
        self.torec_total_pages = 500

    def get_tvshows(self, page=1):
        tvshows = []

        re_sub_box = "<a href=\"/sub.asp\?sub_id=(?P<id>\d+)\""
        re_series = "<div class=\"sub_tbox\".*?{0}.*?</div>".format(re_sub_box)

        re_imdb = "<a href=\"http\://www\.imdb\.com/title/tt(?P<imdbid>\d+)/"
        re_sub_rank = "<div class=\"sub_rank_div\".*?{0}.*?</div>".format(re_imdb)

        try:
            page_content = str(client.request(self.torec_link % page))
            for item in re.finditer(re_series, page_content, re.DOTALL):
                import xbmc
                import sys
                if xbmc.abortRequested:
                    return sys.exit()
                series_link = self.torec_series_link % str(item.group('id').strip())
                series_content = str(client.request(series_link))
                for series_item in re.finditer(re_sub_rank, series_content, re.DOTALL):
                    import xbmc
                    import sys
                    if xbmc.abortRequested:
                        return sys.exit()
                    imdbid = "tt" + series_item.group('imdbid').strip()
                    tvshow = {}
                    try:
                        import hashlib
                        tvshowhash = "torec::" + hashlib.sha224("%s" % (imdbid)).hexdigest()
                        fromcache = cache.get(tvshowhash)
                        if fromcache is not None:
                            tvshow = eval(fromcache[1].encode('utf-8'))
                            tvshow['cached'] = "true"
                        else:
                            from libra.imdb import imdb
                            imdb_data = imdb(imdbid=imdbid)
                            tvshow['title'] = imdb_data.get_title()
                            tvshow['year'] = imdb_data.get_year()
                            tvshow['imdbid'] = imdb_data.get_imdbid()
                            tvshow['runtime'] = imdb_data.get_runtime()
                            tvshow['rating'] = imdb_data.get_rating()
                            tvshow['genres'] = imdb_data.get_genres()
                            tvshow['name'] = "%s (%s)" % (tvshow['title'], tvshow['year'])

                            from libra.tvdb import tvdb
                            tvdb_data = tvdb(imdbid=imdbid)
                            tvshow['tvdb'] = tvdb_data.get_seriesid()

                            cache.set(tvshowhash, tvshow)

                    except:
                        continue

                    tvshows.append(tvshow)
        except Exception, e:
            import xbmc
            import traceback
            map(xbmc.log, traceback.format_exc().split("\n"))
            raise

        return tvshows
