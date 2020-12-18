import pandas as pd
import re
import requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

fifa_url = "https://sofifa.com/players?offset="
fifa_columns = ['ID', 'Name', 'Age', 'Photo', 'Nationality', 'Flag', 'Overall', 'Potential', 'Club', 'Club Logo',
                'Value',
                'Wage', 'Special']

data = pd.DataFrame(columns=fifa_columns)
logging.info("Start data ")

# include 300 pages
for offset in range(0, 300):
    logging.info(f"Start scraping: {offset}")
    url = fifa_url + str(offset * 61)
    response_status = requests.get(fifa_url)
    plain_text = response_status.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    table_body = soup.find('tbody')
    for row in table_body.find_all('tr'):
        td = row.findAll('td')
        picture = td[0].find('img').get('data-src')
        pid = td[0].find('img').get('id')
        nationality = td[1].find('a').find('div').find('img').get('title')
        flag_img = td[1].find('img').get('data-src')
        name = td[1].find('a').get('data-tooltip')
        age = td[2].text.strip()
        over_all = td[3].find('span').text.strip()
        potential = td[4].find('span').text.strip()
        club = td[5].find('a').text.strip()
        club_log = td[5].find('img').get('data-src')
        value = td[6].text.strip()
        wage = td[7].text.strip()
        special = td[8].find('span').text.strip()
        player_data = pd.DataFrame([[pid, name, age, picture, nationality, flag_img, over_all, potential, club,
                                     club_log, value, wage, special]])
        player_data.columns = fifa_columns
        data = data.append(player_data, ignore_index=True)

data = data.drop_duplicates()

data.to_csv('data.csv', index=False)

logging.info("finish up data scraping")
