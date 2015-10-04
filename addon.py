import urlparse, sys, os, xbmcaddon
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))


try:
    action = params['action']
except:
    action = None
try:
    name = params['name']
except:
    name = None
try:
    title = params['title']
except:
    title = None
try:
    year = params['year']
except:
    year = None
try:
    imdb = params['imdb']
except:
    imdb = '0'
try:
    tvdb = params['tvdb']
except:
    tvdb = '0'
try:
    tvshowtitle = params['tvshowtitle']
except:
    tvshowtitle = None


if action is None:
    print "======= Libra ========"
    # from resources.lib.indexers import navigator
    # navigator.navigator().root()

elif action == 'movieToLibrary':
    from libra import movies
    movies.Movies().add(name, title, year, imdb)

# elif action == 'seriesToLibrary':
#     from libra import series
#     series.Series().add(name, title, year, imdb)

elif action == 'play':
    from libra.sources import Sources
    s = Sources()
    s.play(name, title, year, imdb, tvdb, tvshowtitle)

# from libra.imdb import imdb

# i = imdb(imdbid="tt1781922")
# print "========================================"
# print i.get_title()
# print i.get_year()
# print i.get_genres()
# print "======================================="

# from libra.tvdb import tvdb

# i = tvdb(imdbid="tt0411008")
# print "========================================"
# print i.get_series_name()
# print i.get_year()
# print i.get_seriesid()
# print i.get_imdbid()
# print "======================================="


# from libra.movies import movies

# m = movies()
# m.add("No Escape (2015)", "No Escape", "2015", "tt1781922")


# from libra.sources import sources
# s = sources()
# s.play("Southpaw (2015)", "Southpaw", "2015", "tt1798684", None, None)

# from indexers.ktuvit import ktuvit
# k = ktuvit().get_movies()
# for i in k:
#     print i['title']

# from indexers.torec import torec
# k = torec().get_tvshows(page=2)
# for i in k:
#     print i

