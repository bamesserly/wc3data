import requests
from bs4 import BeautifulSoup
from list_of_players import list_of_new_players
new_games_temp = open('new_games_temp3.txt', 'w+')

part_list_of_games = []
progress_notifier = []

#cyles through player names, collecting all games
for x in range (25426, len(list_of_new_players)): #range will be 0,len(list_of_players)
  player_name = list_of_new_players[x][0]
  max_page_number = list_of_new_players[x][1]
  #Extracts each game on each game page for a given player name
  for x in range (0, max_page_number +1):  #player_name[x][1] +1 here
    page_number = str(x)
    url = "http://tft.w3arena.net/profile/" + player_name + "/?p=" + page_number
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    page_data = soup.find_all("table", {"class": "StyledTable"})
    for item in page_data:
      for x in range (3, 23):
        try:
          game_results_pre = (item.contents[x].text)
          game_results = (game_results_pre.splitlines())
          del (game_results[0])
          if (game_results[0]) == "Win" and (game_results[1]) == "1on1":
            game_results[0] = player_name
          elif (game_results[0]) == "Lose" and (game_results[1]) == "1on1" and (game_results[2])==player_name:
            game_results[0] = (game_results[3])
          elif (game_results[0]) == "Lose" and (game_results[1]) == "1on1" and (game_results[2])!=player_name:
            game_results[0] = (game_results[2])
          elif (game_results[1])=="2on2":
            del (game_results)
          #part_list_of_games.append(game_results)
          new_games_temp.write(str(game_results) + ", ") #, end='', flush=True)
          # print(str(game_results) + ", ", end='', flush=True)
          new_games_temp.flush()
        except:
          pass

          #print(str((len(part_list_of_games))) + " after " + str(page_number) + " pages")
                    #print(game_results)

                    #test6.write(str(game_results + ", "))

#print("\n" + "Finished collecting games of " + str(player_name))

new_games_temp.close()

# print(len(complete_list_of_games))
# print(len(list_of_games))
#progress_notifier.append(player_name)
