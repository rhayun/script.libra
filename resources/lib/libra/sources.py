import sys, xbmcaddon,xbmcgui,xbmcplugin, urllib

from libra import common

class sources:
    def __init__(self):
        self.sources = []
        self.sourcesDictionary()


    def play(self, name, title, year, imdb, tvdb, tvshowtitle):
        import xbmc
        content = 'movie' if tvshowtitle == None else 'episode'
        source = self.sourcesDialog()

        if content == 'movie':
            url = urllib.quote_plus("http://www.imdb.com/title/%s/" % imdb)
            if source[0] == "Genesis":
                stream ="plugin://%s/?action=play&imdb=%s&year=%s&name=%s&title=%s&tmdb=&url=%s" % (source[1], imdb[2:], year, name.replace(' ','%20'), title.replace(' ','%20'), url)
            elif source[0] == "Pulsar":
                stream ="plugin://%s/movie/%s/play" % (source[1], imdb)
            elif source[0] == "SALTS":
                stream ="plugin://%s/?mode=get_sources&video_type=Movie&title=%s&year=%s&slug=%s" % (source[1], title, year, slug)
        
        elif content == 'episode':
            pass

        listitem = xbmcgui.ListItem(path=stream, thumbnailImage=None)
        listitem.setInfo(type="Video", infoLabels={ "Title": str(source[0]) })
        #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play( stream, listitem)


    def sourcesDialog(self):
        try:
            if len(self.sources) > 1:
                labels = [i[0] for i in self.sources]
                select = common.selectDialog(labels)
                if select == -1: return 'close://'
                source = self.sources[select]
            else:
                source = self.sources[0]

            return source

        except:
            return


    def sourcesDictionary(self):
        if common.get_setting('s_genesis') == "true":
            try:
                genesis = xbmcaddon.Addon('plugin.video.genesis').getAddonInfo('name')
                self.sources.append(['Genesis', 'plugin.video.genesis'])
            except:
                pass

        if common.get_setting('s_pulsar') == "true":
            try:
                pulsar = xbmcaddon.Addon('plugin.video.pulsar').getAddonInfo('name')
                self.sources.append(['Pulsar', 'plugin.video.pulsar'])
            except:
                pass

        if common.get_setting('s_salts') == "true":
            try:
                salts = xbmcaddon.Addon('plugin.video.salts').getAddonInfo('name')
                self.sources.append(['SALTS', 'plugin.video.salts'])
            except:
                pass
