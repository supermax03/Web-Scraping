#####################################################################################
# TO RUN THIS EXAMPLE SUCCESSFULLY YOU WILL NEED TO INSTALL plotly on your computer
#####################################################################################

from bs4 import BeautifulSoup
import requests
import plotly.plotly as py
from plotly.graph_objs import *
import sys

_URL_ = "https://www.youtube.com/feed/guide_builder"
_SUBSCRIBERS_ = 'subscribers'


def youtube_scraping():
    page = requests.get(_URL_)
    soup = BeautifulSoup(page.content, "html.parser")
    list = soup.find_all('div', class_='yt-lockup-content')
    youtube_channels = []
    youtube_subscribers = []
    for item in list:
        youtube_channel = item.find('a').get_text()
        subscribers = item.find('li').get_text() if item.find('li') else '0'
        subscribers = subscribers[:subscribers.find(_SUBSCRIBERS_)].strip().replace(',', '')
        if subscribers.isnumeric():
            youtube_channels.append(youtube_channel)
            youtube_subscribers.append(int(subscribers))
    return [youtube_channels, youtube_subscribers]


##################################################################
# YOU WILL NEED AN ACCOUNT (IT IS FREE). GET IT AT https://plot.ly
##################################################################
def plot(*data):
    trace = Pie(labels=data[0][0], values=data[0][1])
    data = Data([trace])
    py.plot(data, filename='basic_pie_chart')


if __name__ == '__main__':
    try:
        plot(youtube_scraping())
    except:
        print(sys.exc_info())
