import requests
import time
from bs4 import BeautifulSoup


class Movie:
    def __init__(self, title, director, duration, genre, summary, cast, trailers):
        self.title = title
        self.genre = genre
        self.duration = duration
        self.summary = summary
        self.director = director
        self.cast = cast
        self.trailers = trailers

    def addActor(self, *actors):
        for actor in actors:
            self.cast.append(actor)

    def addTrailer(self, *trailers):
        for trailer in trailers:
            self.trailers.append(trailer)

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def setDuration(self, duration):
        self.duration = duration

    def getDuration(self):
        return self.duration

    def getSummary(self):
        return self.summary

    def setSummary(self, summary):
        self.summary = summary

    def setDirector(self, director):
        self.director = director

    def getDirector(self):
        return self.director

    def getGenre(self):
        return self.genre

    def setGenre(self, genre):
        self.genre = genre

    def getTrailers(self):
        return self.trailers

    def getCast(self):
        return self.cast

    Title = property(fget=getTitle, fset=setTitle)
    Duration = property(fget=getDuration, fset=setDuration)
    Summary = property(fget=setSummary, fset=setSummary)
    Genre = property(fget=getGenre, fset=setGenre)
    Director = property(fget=getDirector, fset=setDirector)
    Trailers = property(fget=getTrailers)
    Cast = property(fget=getCast)


class IMDB:
    __url__ = 'http://www.imdb.com'
    movies = {"new": "movies-coming-soon/{0}/?ref_=inth_cs", "intheaters": "movies-in-theaters/?ref_=cs_inth"}
    @staticmethod
    def getmovies(desc,date):
        films = []
        if desc in IMDB.movies:
            page = requests.get('/'.join((IMDB.__url__, IMDB.movies[desc])).format(date))
            soup = BeautifulSoup(page.content, "html.parser")
            items = soup.find_all('div', class_="list_item")
            for movie in items:
                title = movie.find('h4').get_text()
                duration = movie.find('time').get_text() if movie.find('time') else '0'
                summary = movie.find('div', class_='outline').get_text() if movie.find('div',
                                                                                       class_='outline').get_text() else ''
                genre = [genre.get_text() for genre in movie.find_all('span', {'itemprop': 'genre'})]
                cast = [actor.get_text() for actor in movie.find_all('span', {'itemprop': 'actors'})]
                directors = [director.get_text() for director in movie.find_all('span', {'itemprop': 'director'})]
                trailers = [trailer.attrs['href'] for trailer in movie.find_all('a', {'itemprop': 'trailer'})]
                film = Movie(title, directors, duration, genre, summary, cast, trailers)
                films.append(film)

        return films


if __name__ == '__main__':
    for film in IMDB.getmovies("new",time.strftime("%Y-%m")):
        print(film.__dict__)

