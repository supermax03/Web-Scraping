from bs4 import BeautifulSoup
import pandas as pd
import urllib.request

data_columns = ["places", "temperatures", "description"]

def scrap_weather_web_site():
    page = urllib.request.urlopen('https://www.clima.com/argentina').read()
    soup = BeautifulSoup(page, 'html.parser')
    items = soup.find_all('div', class_='m_list_block_cities')[0].find_all('li')

    places = [elem.find("strong").get_text() for elem in items]
    temperatures = [cint(elem.find(class_="m_list_block_cities-temp").get_text()[:-1]) for elem in items]
    descriptions = [elem.find('i').attrs['class'][1] for elem in items]

    weather = pd.DataFrame(
        {data_columns[0]: places,
         data_columns[1]: temperatures,
         data_columns[2]: descriptions},
        columns=data_columns,
        )
    return weather

def cint(item):
    value = item
    try:
        value = int(item)
    finally:
        return value


def getdatasortedbyfield(field, asc=False):
    dataset = None
    if field in data_columns:
        dataset = (scrap_weather_web_site().sort_values(by=[field],
                                                        ascending=asc))
    return dataset


if __name__ == '__main__':
    print(getdatasortedbyfield("temperatures", True))

