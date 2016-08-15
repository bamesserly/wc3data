import requests
from bs4 import BeautifulSoup
from dict_of_elos import dict_of_elos
from datetime import date
import datetime
import time
#new_games_temp = open('new_games.txt', 'w+')

part_list_of_games = []
progress_notifier = []

for tag in dict_of_elos:
  print tag
  most_recent_game_time = dict_of_elos[tag]['most_recent_game_time']
  page = 0
  keep_searching_for_games = True
  n_new_games_scanned = 0
  while (keep_searching_for_games):
    url = "http://tft.w3arena.net/profile/{0}/?p={1}".format(tag, page)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    page_data = soup.find_all("table", {"class": "StyledTable"})
    for item in page_data:
      for x in range (3, len(item)):
        try:
          game_results_pre = (item.contents[x].text)
          game_results = (game_results_pre.splitlines())
          del (game_results[0])
        except AttributeError:
          #can happen with first or last page that doesn't have full 20 games
          pass

        n_new_games_scanned += 1
        if( datetime.datetime.strptime(game_results[4], "%d-%m-%Y %H:%M") < datetime.datetime.strptime('19-06-2016 00:00', "%d-%m-%Y %H:%M")):
          print "  most recent game " + str(datetime.datetime.strptime(most_recent_game_time, '%Y-%m-%d %H:%M'))
          print "  current game     " + str(datetime.datetime.strptime(game_results[4], "%d-%m-%Y %H:%M"))

        #Check time condition
        if(datetime.datetime.strptime(most_recent_game_time, '%Y-%m-%d %H:%M') >= datetime.datetime.strptime(game_results[4], "%d-%m-%Y %H:%M")):
          if( datetime.datetime.strptime(game_results[4], "%d-%m-%Y %H:%M") < datetime.datetime.strptime('19-06-2016 00:00', "%d-%m-%Y %H:%M")):
            print "  we've read all the games up until the last one on record"
            print "    most recent game " + str(datetime.datetime.strptime(most_recent_game_time, '%Y-%m-%d %H:%M'))
            print "    current game     " + str(datetime.datetime.strptime(game_results[4], "%d-%m-%Y %H:%M"))
          n_new_games_scanned -= 1
          #print "    new games retreived = " + str(n_new_games_scanned)
          keep_searching_for_games = False
          break #for x in range (3, len(item))
      else:
        print "I finished the x in range loop, I'm moving on to page " + str(page+1)
        page +=1
        continue
      #break #for item in page_data
'''
  url = "http://tft.w3arena.net/profile/" + tag + "/?p=0"
  #url = "http://tft.w3arena.net/profile/" + "FaceControl" + "/?p=0"
  #url = "http://tft.w3arena.net/profile/" + "HuntressShaped" + "/?p=0"
    #print url
    #print soup.prettify()
    #print page_data

      if (datetime.datetime.strptime(game_date_time, '%Y-%m-%d %H:%M') <


      game_date_time = time.strftime("%Y-%m-%d %H:%M", time.strptime(game_date_time,"%d-%m-%Y %H:%M")) 

27-07-2015 08:55

    #game_date_time = time.strftime("%Y-%m-%d %H:%M", time.strptime(game_date_time,"%d-%m-%Y %H:%M"))

      #print game_results

      except:
        pass

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
'''
"""



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
"""
