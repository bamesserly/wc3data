# 1. TODO functionalize
# 2. TODO while checking each game, add both players to all_list
# after the loop over existing accounts, make a new list:
# new_accts_list = all_list - existing_accounts
# then, scrape over that list.
# 3. TODO check whether reached the last page and 
# set keep_searching_for_games to false
import requests
from bs4 import BeautifulSoup
from dict_of_elos import dict_of_elos
from datetime import date
import datetime
import time
#new_games_temp = open('new_games.txt', 'w+')

date_of_last_scan = '19-06-2016 00:00'
game_fields = ['date_time', 'winning_player','player1_name','player2_name']
part_list_of_games = []
progress_notifier = []
list_of_new_games = []

# loop existing players
for tag in dict_of_elos:
  print tag
  most_recent_game_time = dict_of_elos[tag]['most_recent_game_time']
  page = 0
  keep_searching_for_games = True
  n_new_games_scanned = 0
  # keep incrementing games and pages until:
  # 1. we find the game that we last scanned
  # 2. get to a page with no game data (TODO) 
  while (keep_searching_for_games):
    url = "http://tft.w3arena.net/profile/{0}/?p={1}".format(tag, page)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    page_data = soup.find_all("table", {"class": "StyledTable"})
    # TODO: maybe with itertools combine these into a single loop
    for item in page_data:
      for x in range (3, len(item)):
        try:
          game_results_pre = (item.contents[x].text)
          game_results = (game_results_pre.splitlines())
          del (game_results[0])
        except AttributeError:
          #can happen with first or last page that doesn't have full 20 games
          pass

        # Check if solo
        if game_results[1] != "1on1":
          continue

        # Check if we have caught up to the most recent game
        # if so, break out of both for loops and the while loop
        if(datetime.datetime.strptime(most_recent_game_time, '%Y-%m-%d %H:%M') >= 
            datetime.datetime.strptime(game_results[4], "%d-%m-%Y %H:%M")):
          if n_new_games_scanned > 0:
            print "    most recent game " + str(most_recent_game_time)
            print "    new games retreived = " + str(n_new_games_scanned)
          keep_searching_for_games = False
          break #for x in range (3, len(item))
        # TODO make sure this is breaking out of both for loops

        # Check if this game is before we last scanned (so we missed it the 1st time)
        # TODO do something about this case?
        if( datetime.datetime.strptime(game_results[4], "%d-%m-%Y %H:%M") < 
              datetime.datetime.strptime(date_of_last_scan, "%d-%m-%Y %H:%M")): 
          print "  WARNING: GAME(S) AFTER MOST RECENT ON RECORD BUT BEFORE 6-19-2016"
          print "    current game     " + str(datetime.datetime.strptime(game_results[4], "%d-%m-%Y %H:%M"))

        # Get the game info and save it
        # TODO make second list
        game_dict = {}
        game_dict.fromkeys(game_fields)
        game_dict['date_time'] = game_results[4].encode("utf-8")
        if (tag == game_results[2]) is not (tag == game_results[3]):
          game_dict['player1_name'] = tag
          game_dict['player2_name'] = game_results[3] if (game_results[2] == tag) else (game_results[2])
          game_dict['winning_player'] = tag if (game_results[0] == 'Win') else (game_dict['player2_name'])
        else:
          print "WARNING: CURRENT PLAYER IS NEITHER P1 NOR P2"
          print "tag " + tag
          print "player1 " + game_dict['player1_name']
          print "player2 " + game_dict['player2_name']

        n_new_games_scanned += 1
        list_of_new_games.append(game_dict)

      # Got to the end of the page, going to the next one
      # TODO make sure this is breaking out of both for loops
      else:
        print "  End page. Going to next page: " + str(page+1)
        page +=1
        continue

'''
          if game_results[0] == "Win":
            game_info['winning_player'] = tag
            game_info['player2_name'] = game_results[2] if (game_results[1] == tag) else game_results[1]
          else:
            game_info['winning_player'] = game_results[2]
            game_info['player2_name'] = game_results[2] if (game_results 
          game_info['player1_name'] = tag
          game_info['player2_name'] = game_results[2] if (game_results[1] == game_info['player1_name']) else game_results[1]
          game_info['winning_player'] = tag if game_results[0] == tag else
        else:


      #break

  {'date_time': '08-09-2015 13:50', 'player1_name': 'zzz', 'player2_name': 'H1mmla', 'winning_player': 'zzz'}
  url = "http://tft.w3arena.net/profile/" + tag + "/?p=0"
  #url = "http://tft.w3arena.net/profile/" + "FaceControl" + "/?p=0"
  #url = "http://tft.w3arena.net/profile/" + "HuntressShaped" + "/?p=0"
  #print url
  #print soup.prettify()
  #print page_data
  #if( datetime.datetime.strptime(game_results[4], "%d-%m-%Y %H:%M") < datetime.datetime.strptime('19-06-2016 00:00', "%d-%m-%Y %H:%M")):
    #print "  we've read all the games up until the last one on record"
    #print "    most recent game " + str(datetime.datetime.strptime(most_recent_game_time, '%Y-%m-%d %H:%M'))
    #print "    current game     " + str(datetime.datetime.strptime(game_results[4], "%d-%m-%Y %H:%M"))

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
