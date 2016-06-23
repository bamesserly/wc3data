import requests
from bs4 import BeautifulSoup
from list_of_players import list_of_new_players
player_update_temp = open('player_update_temp.txt', 'w+')


for x in range (17728, len(list_of_new_players)): #range will be 0,len(list_of_players)
    player_name = list_of_new_players[x][0]
    url = "http://tft.w3arena.net/profile/" + player_name + "/?p=1"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    page_data = soup.find_all("div", {"class": "winLossContainer"})
    data_set = []
    for item in page_data:
        data_set.append(item.text)
    data_set2 = data_set[0].split('\n')
    while '' in data_set2:
        data_set2.remove('')
    wins = data_set2[0][:-6]
    loses = data_set2[1][:-8]
    try:
        percentage = str(round((int(wins)/(int(wins) + int(loses)) * 100), 2))
    except:
        percentage = 100.00
    list_of_new_players[x].append(wins)
    list_of_new_players[x].append(loses)
    list_of_new_players[x].append(percentage)
    #print(list_of_players[x])
    player_update_temp.write(str(list_of_new_players[x]) + ", ")  # , end='', flush=True)
    # print(str(game_results) + ", ", end='', flush=True)
    player_update_temp.flush()