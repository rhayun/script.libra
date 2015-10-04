import json, re
from resources.lib import client


class imdb:

    def __init__(self, imdbid=None, title=None, year=None):

        self.imdbid = imdbid
        self.title = title
        self.year = year

        self.imdb_data = {}

        if imdbid is not None:
            if not imdbid.startswith("tt"):
                self.imdbid = "tt%s" % self.imdbid
            self.omdb_link = "http://www.omdbapi.com/?i=%s" % imdbid
        elif title is not None and year is not None:
            title = re.sub('\s','+', title)
            self.omdb_link = "http://www.omdbapi.com/?t=%s&y=%s" % (title, year)

        try:
            omdb_info = client.request(self.omdb_link)
            self.imdb_data = json.loads(omdb_info)
            print self.imdb_data
        except:
            pass


    def get_imdbid(self, digits=False):
        if self.imdbid is None:
            self.imdbid = self.imdb_data.get('imdbID')
        return self.imdbid if digits == False else self.imdbid[2:]


    def get_title(self):
        if self.title is None:
            self.title = self.imdb_data.get('Title')
        return self.title


    def get_year(self):
        if self.year is None:
            self.year = self.imdb_data.get('Year')

        transyear = self.year.encode('utf-8')
        transyear = ''.join(c for c in transyear if c.isdigit())
        transyear = transyear[:4]

        return transyear


    def get_runtime(self):
        try:
          runtime = self.imdb_data.get('Runtime')
          if runtime != None:
            return str(runtime)
        except:
          return '0'


    def get_rating(self):
        try:
          rating = self.imdb_data.get('imdbRating')
          if rating != None:
            return float(rating)
        except:
          return 0

    
    def get_genres(self):
        genre = self.imdb_data.get('Genre')
        if not genre:
            return []
        return [g.strip() for g in genre.split(',')]
