#LGOR = last game on record
# 1. TODO functionalize
# 2. TODO while checking each game, add both players to all_list
# after the loop over existing accounts, make a new list:
# new_accts_list = all_list - existing_accounts
# then, scrape over that list.
# 3. TODO check whether reached the last page and 
# set keep_searching_for_games to false
import requests
from bs4 import BeautifulSoup
from datetime import date
import datetime
import time

#date_of_last_scan = '19-06-2016 00:00'
date_of_last_scan = datetime.datetime.strptime(date_of_last_scan,'%d-%m-%Y %H:%M')
part_list_of_games = []
progress_notifier = []
game_fields = ['date_time', 'winning_player','player1_name','player2_name']

def main():
  from data.dict_of_elos import dict_of_elos
  set_of_existing_players = set(list(dict_of_elos.keys()))
  tags_total = len(set_of_existing_players)
  print "Analyzing ", tags_total, "players..."

  list_of_new_games = []
  set_of_new_players = set([])
  tags_analyzed = 0
  missed_games = 0
  scrape_time = 0
  t0 = time.time()

  # loop existing players
  # big speed gain by not looping over the dict
  for tag in set_of_existing_players:
    tags_analyzed += 1
    if tags_analyzed % 50 == 0:
      print tags_analyzed, "tags analyzed"
      #print "new games found before last scan =", missed_games
      t1 = time.time()
      print "     time elapsed", t1-t0
      #print "     scrape time", scrape_time
      #100*round(tags_analyzed/float(tags_total),3)

    #Some variables for this tag
    LGOR_time = dict_of_elos[tag]['most_recent_game_time']
    LGOR_time = datetime.datetime.strptime(LGOR_time, '%Y-%m-%d %H:%M')
    page = 0
    n_new_games_found = 0
    keep_searching_for_games = True

    # keep incrementing games and pages until:
    # 1. we find the game that we last scanned
    # 2. get to a page with no game data (TODO) 
    while (keep_searching_for_games):
      url = "http://tft.w3arena.net/profile/{0}/?p={1}".format(tag, page)
      #t2 = time.time()
      r = requests.get(url)
      #t3 = time.time()
      soup = BeautifulSoup(r.content, 'html.parser')
      games_on_page = soup.find("table", {"class": "StyledTable"})
      #scrape_time += t3-t2 #yeah, 99.98% of the running time is scrape time, mostly in that requests.get(url) command
      try:
        number_of_games_on_page = len(games_on_page)
      except TypeError:
        keep_searching_for_games = False
        print "game on page length is zero. Tag is", tag
        break
      for game_i in range(0, number_of_games_on_page):
        try:
          game_results = get_game_results(games_on_page, game_i)
        except AttributeError:
          #there are a few newline characters in games_on_page.contents[game_i]
          #test: games_on_page.contents[game_i].isspace()
          continue

        if game_results[1] != "1on1":
          continue

        current_game_time = datetime.datetime.strptime(game_results[4], "%d-%m-%Y %H:%M")

        #we're all caught up. next tag.
        if current_game_time == LGOR_time:
          if n_new_games_found:
            print "  ", tag, n_new_games_found, "new games found. LGOR", LGOR_time, "Current game time", current_game_time
          keep_searching_for_games = False
          break # out of list of games on this page

        #Problem: We somehow missed the last game on record.
        #Current behavior: don't add this game or any further games to the list.
        elif current_game_time < LGOR_time:
          print "WARNING: the last game on record happened after the game under current consideration."
          keep_searching_for_games = False
          break # out of list of games on this page

        #we've found a new game
        elif current_game_time > LGOR_time:
          game_dict = {}
          game_dict = make_new_game_dict(tag, game_results, set_of_new_players)
          #list_of_new_games.append(game_dict)
          n_new_games_found += 1
          if date_of_last_scan > current_game_time:
            missed_games += 1

      # Got to the end of the page, going to the next one
      # Following statement is eval-ed only if loop over games on page ends without breaking.
      # If a game causes a break, this statement is not eval-ed.
      else:
        #print "    End page. Going to next page: " + str(page+1)
        page +=1

  #print "starting list of players", set_of_existing_players
  #print len(set_of_new_players)
  #print len(set_of_existing_players)
  set_of_new_players = set_of_new_players.difference(set_of_existing_players)
  #print len(set_of_new_players)
  #print "set of new players found", set_of_new_players

  new_games_outfile = open('data/list_of_new_games.py', 'w+')
  new_games_outfile.write("list_of_new_games = " + str(list_of_new_games))
  new_games_outfile.close()
  
  new_players_outfile = open('data/list_of_new_players.py', 'w+')
  new_players_outfile.write('list_of_new_players = ' + str(set_of_new_players))
  new_players_outfile.close()

def get_game_results(games_on_page, game_i):
  game_results = games_on_page.contents[game_i].text
  game_results = game_results.splitlines()
  del (game_results[0])
  return game_results

def make_new_game_dict(tag, game_results, set_of_new_players):
  game_dict = {}
  game_dict.fromkeys(game_fields)

  players = (game_results[2].encode("utf-8"), game_results[3].encode("utf-8"))
  if tag not in players:
    print "WARNING: tag is neither P1 nor P2"

  game_dict['date_time'] = game_results[4].encode("utf-8")
  game_dict['player1_name'] = max(players)
  game_dict['player2_name'] = min(players)
  p1_is_tag = (game_dict['player1_name'] == tag)
  game_dict['winning_player'] = game_dict['player1_name'] if (p1_is_tag is (game_results[0] == 'Win')) else game_dict['player2_name']

  set_of_new_players.update(players)

  return game_dict

if __name__ == "__main__":
  main()
