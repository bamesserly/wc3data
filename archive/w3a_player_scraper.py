import requests
from bs4 import BeautifulSoup
from list_of_players import list_of_new_players
from list_of_games import list_of_games
# new_players = open('new_players', 'w')



###USED TO GET NEW PLAYERS FROM LIST OF GAMES
# list_of_new_players = []
# list_of_new_players2 = []
#
# for x in range(0, len(list_of_games)):
#     search = list_of_games[x][2]
#     if any(e[0] == search for e in list_of_players):
#         pass
#     else:
#         list_of_new_players.append(list_of_games[x][2])
#     search = list_of_games[x][3]
#     if any(e[0] == search for e in list_of_players):
#         pass
#     else:
#         list_of_new_players.append(list_of_games[x][3])
# for x in range (0, len(list_of_new_players)):
#     player_name = list_of_new_players[x]
#     player_info = [player_name, 0]
#     list_of_new_players2.append(player_info)
# list_of_new_players = [list(t) for t in set(map(tuple, list_of_new_players2))]
# print(list_of_new_players)

# new_players.write(str(list_of_players + ", "))

# list_of_players = list_of_new_players




# # #Extracts player names from ladder, adds them to list of players
# # for x in range (9,11): #range will be 1,11
# #     url = "http://tft.w3arena.net/ladder?laddertype=&lp="+ str(x) + "&lc=100"
# #     r = requests.get(url)
# #     soup = BeautifulSoup(r.content, 'html.parser')
# #     page_data = soup.find_all("div", {"class": "PlayerWithIcon"})
# #     for item in page_data:
# #         player_name = item.text
# #         player_info = [player_name, 0]
# #         list_of_players.append(player_info)




# Obtains the number of game pages for each player in the list of players
for x in range (1000, len(list_of_new_players)):
    player_name = list_of_new_players[x][0]
    url = "http://tft.w3arena.net/profile/" + player_name + "/?p=0"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    page_data = soup.find_all("li")
    page_number_links = []
    for item in page_data:
        page_number_links.append(item.text)
    try:
        max_page_number = int(page_number_links[-2])
    except:
        max_page_number = 0
    list_of_new_players[x][1] = max_page_number
    print(str(list_of_new_players[x]) + ", ", end='', flush=True)



