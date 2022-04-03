from youtube_search import YoutubeSearch

class Search:

    def __init__(self):
        self.yt_url = None

    def getYt_song(self, song):
        result = YoutubeSearch(song, max_results=10).to_dict()
        url = "https://www.youtube.com"+result[0].get('url_suffix')
        title = result[0].get('title')
        return title, url

