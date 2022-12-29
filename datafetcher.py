import sys
#sys.path.append(r"c:\users\tomas\pys\sbdata\venv\lib\site-packages")
import requests
from requests.exceptions import HTTPError
import pandas as pd
from bs4 import BeautifulSoup
from lxml import html


def fetch_data(data_pair, first_game):
    # The csv file to save the data to
    filename = "fliiga2018-2022.csv"

    # The PHP file to pass the data to
    url = "http://www.tilastopalvelu.fi/fb/gameshootingmap/helper/getshootings.php"

    # Assign the request payload to pass in the URL
    data = {"GameID": str(data_pair[0]), "season" : str(data_pair[1])}
    response = requests.post(url, data)
    # Store the JSON response

    fjson = response.json()
    if len(fjson) == 0:
        return
    # Convert the JSON to a Pandas dataframe
    df = pd.DataFrame(fjson)
    # Append the game number to the dataframe
    gamenodf = pd.DataFrame(data={'GAME_ID': [str(data_pair[0])]})
    finaldf = df.assign(**gamenodf.iloc[0])



    # Write the game's data to a CSV file
    if first_game:
        finaldf.to_csv(filename, mode='a', sep='|', encoding='utf-8')
    else:
        finaldf.to_csv(filename, mode='a', sep='|', encoding='utf-8', header=False)





def fetch_game_ids():
    id_list = []
    # F-Liiga/Salibandyliiga games from 2017-2018 to 2021-2022
    # Total games 909

    url_list = ["http://www.tilastopalvelu.fi/fb/modules/mod_schedulehistory/helper/games.php?statgroupid=2193&select=&id=&teamid=&rinkid=&season=2018&",
                "https://www.tilastopalvelu.fi/fb/modules/mod_schedulehistory/helper/games.php?statgroupid=2923&select=&id=&teamid=&rinkid=&season=2019&",
                "http://www.tilastopalvelu.fi/fb/modules/mod_schedulehistory/helper/games.php?statgroupid=5635&select=&id=&teamid=&rinkid=&season=2020&",
                "http://www.tilastopalvelu.fi/fb/modules/mod_schedulehistory/helper/games.php?statgroupid=7000&select=&id=&teamid=&rinkid=&season=2021&",
                "http://www.tilastopalvelu.fi/fb/modules/mod_schedulehistory/helper/games.php?statgroupid=7000&select=&id=&teamid=&rinkid=&season=2022&"]

    #url_list = ["http://www.tilastopalvelu.fi/fb/modules/mod_schedule/helper/games.php?statgroupid=7000&select=&id=&teamid=&rinkid=&rdm=0.9753715826643513&season=2023&"]
    for url in url_list:
        response_json = requests.get(url).json()
        for i in response_json['games']:
            id_list.append([i['UniqueID'], url.split("=")[-1][:-1]])
    return id_list


def fetch_game_data(id_list):
    index = 0
    first_game = True
    for index, game_id in enumerate(id_list):
        if index % 100 == 0:
            print(index, "games scraped")
        fetch_data(game_id, first_game)
        first_game = False
    print("Scraping over, total games scraped:", index)


def main():
    id_list = fetch_game_ids()
    fetch_game_data(id_list)

if __name__ == "__main__":
    main()
