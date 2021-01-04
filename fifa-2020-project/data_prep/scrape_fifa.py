import pandas as pd
import re
import requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

###
# format age_group
###

def get_age_group(age):
    if age < 20:
        return "Below 20 years"
    if age >= 20 and age < 25:
        return "Age: 20 - 25"
    if age >= 25 and age < 30:
        return "Age: 25 - 30"
    if age >=30 and age < 35:
        return "Age: 30 - 35"
    if age >= 35 and age < 40:
        return "Age: 35 - 40"

###
# scrape data
###
def scrape_data():
    fifa_url = "https://sofifa.com/players?offset="
    fifa_columns = ['ID', 'Name', 'Age', 'Photo', 'Nationality', 'Flag', 'Overall', 'Potential', 'Club', 'Club Logo',
                    'Value',
                    'Wage', 'Special', 'FullName', 'Age_Group']

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
            fullname = name
            # Set age group column
            age_group = get_age_group(int(age))
            player_data = pd.DataFrame([[pid, name, age, picture, nationality, flag_img, over_all, potential, club,
                                         club_log, value, wage, special, fullname, age_group]])
            player_data.columns = fifa_columns
            data = data.append(player_data, ignore_index=True)

    data = data.drop_duplicates()

    data.to_csv('data.csv', index=False)

    logging.info("finish up data scraping")

if __name__ == '__main__':
    scrape_data()
