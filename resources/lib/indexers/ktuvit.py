import re
from resources.lib import client
from libra import cache


class Ktuvit:
    def __init__(self):
        self.ktuvit_link = 'http://www.ktuvit.com/browsesubtitles.php?cs=movies&page=%s'
        self.ktuvit_items_per_page = 32
        self.ktuvit_total_pages = 32
        self.ktuvit_max_items = 1000

    def get_movies(self, page=1):
        movies = []

        re_movie_anchor = "<a href=\"view.php\?id=(?P<id>\d+)#\d+\" title=\"(?P<nameHe>.*?)\|(?P<nameEn>.*?)\|(?P<year>.*?)\""
        re_movie = "<table.*?{0}.*?Israel-Flag.png.*?</table>".format(re_movie_anchor)

        try:
            page_content = str(client.request(self.ktuvit_link % page))
            for item in re.finditer(re_movie, page_content, re.DOTALL):
                import xbmc
                import sys
                if xbmc.abortRequested:
                    return sys.exit()
                movie = {'title': item.group('nameEn').strip(), 'year': item.group('year').strip()}
                movie['name'] = "%s (%s)" % (movie['title'], movie['year'])
                try:
                    import hashlib
                    moviehash = "ktuvit::" + hashlib.sha224("%s (%s)" % (movie['title'], movie['year'])).hexdigest()
                    fromcache = cache.get(moviehash)
                    if fromcache is not None:
                        movie = eval(fromcache[1].encode('utf-8'))
                        movie['cached'] = "true"
                    else:
                        from libra.imdb import imdb
                        imdb_data = imdb(title=movie['title'], year=movie['year'])
                        if imdb_data.imdb_data.get('Error'):
                            continue
                        movie['imdbid'] = imdb_data.get_imdbid()
                        movie['runtime'] = imdb_data.get_runtime()
                        movie['rating'] = imdb_data.get_rating()
                        movie['genres'] = imdb_data.get_genres()

                        cache.set(moviehash, movie)

                except:
                    continue

                movies.append(movie)

        except Exception, e:
            import xbmc
            import traceback
            map(xbmc.log, traceback.format_exc().split("\n"))
            raise

        return movies
