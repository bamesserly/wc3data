# Takes a list of tags, loops through the tags, and
# loops through the games of each tag.
# Saves each game to a file, ordered by date.
# Returns a list of yet unrecorded opponents 
import requests
from bs4 import BeautifulSoup
from datetime import date
import datetime
import time
import glob
from importlib import import_module
import os
from shutil import copy

game_fields = ['date_time', 'winning_player','player1_name','player2_name']

def GetNewTagsAndGames(tags):
  t0 = time.time()
  tags_analyzed = 0
  games2013 = []
  games2014 = []
  games2015 = []
  games2016 = []
  games2017 = []
  set_of_new_tags = set([])
  for t in tags:
    tags_analyzed += 1
    if tags_analyzed % 5 == 0:
      print "      ==", tags_analyzed, " tags analyzed"
      t1 = time.time()
      print "      ==time elapsed", t1-t0
      print "      ==new tags found", len(set_of_new_tags)
      print "      ==number of new games found by last tag", n_new_games_found

    #Some variables for this tag
    page = 0
    n_new_games_found = 0
    keep_searching_for_games = True

    # keep incrementing games and pages until get to a page with no game data
    while (keep_searching_for_games):
      url = "http://tft.w3arena.net/profile/{0}/?p={1}".format(t, page)
      #t2 = time.time()
      r = requests.get(url)
      #t3 = time.time()
      soup = BeautifulSoup(r.content, 'html.parser')
      games_on_page = soup.find("table", {"class": "StyledTable"})
      # scrape_time += t3-t2 #yeah, 99.98% of the running time is scrape time, 
      # mostly in that requests.get(url) command
      try:
        number_of_games_on_page = len(games_on_page)
      except TypeError:
        keep_searching_for_games = False
        #print "No games_on_page. Tag is", t  # Is this acutally a problem?
        break
      for game_i in range(0, number_of_games_on_page):
        try:
          game_results = GetGameResults(games_on_page, game_i)
        except AttributeError:
          #there can be newlines "\n" in games_on_page.contents[game_i]
          #to test do: games_on_page.contents[game_i].isspace()
          continue

        if game_results[1] != "1on1":
          continue

        #we've found a new game
        tags, game_dict = MakeNewGameDict(t, game_results)
        n_new_games_found += 1

        #add any new players the lists.
        set_of_new_tags.update(tags)

        #add each game to a year-specific list
        gtime = datetime.datetime.strptime(game_dict['date_time'], "%d-%m-%Y %H:%M")
        year = gtime.year
        if year < 2014:
          games2013.append(game_dict)
        elif (2014 <= year and year < 2015):
          games2014.append(game_dict)
        elif (2015 <= year and year < 2016):
          games2015.append(game_dict)
        elif (2016 <= year and year < 2017):
          games2016.append(game_dict)
        elif 2017 <= year:
          games2017.append(game_dict)


      # Got to the end of the page, going to the next one
      # The following is eval-ed only if loop over games on page 
      # reaches end without breaking.
      else:
        #print "    End page. Going to next page: " + str(page+1)
        page += 1

    print "      tag =", t, n_new_games_found, "- games found"

  ################
  ## Games Stuff #
  ################
  SaveNewGames(games2013, "data/games2013.py", "games")
  SaveNewGames(games2014, "data/games2014.py", "games")
  SaveNewGames(games2015, "data/games2015.py", "games")
  SaveNewGames(games2016, "data/games2016.py", "games")
  SaveNewGames(games2017, "data/games2017.py", "games")
  
  ###############
  ## Tags Stuff #
  ###############
  # Get the most current master tag list
  from data.list_of_existing_players_short import existing_players
  set_of_existing_tags = set(existing_players)

  # Create the return_tag_list which contains all the elements 
  # in set_of_new_tags and not in set_of_existing_tags.
  return_tags = set_of_new_tags.difference( set_of_existing_tags ) 
  
  # Add the new tags to the master tag list 
  set_of_existing_tags.update(set_of_new_tags)

  # Back up the old tag list
  BackUp('data/list_of_existing_players_short.py')

  # Save the new tag list
  updated_tags_file = open('data/list_of_existing_players_short.py', 'w+')
  updated_tags_file.write("existing_players = " + str(set_of_existing_tags))
  updated_tags_file.close()

  return return_tags

def BackUp(path):
  i = 0
  while (i<100):
    if not os.path.exists(path + '{0}'.format(i)):
      new_backup = path + '{0}'.format(i)
      #print 'Number of player list backups = ', i
      #shutil.copy(path, new_backup)
      copy(path, new_backup)
      break
    i += 1

def GetGameResults(games_on_page, game_i):
  game_results = games_on_page.contents[game_i].text
  game_results = game_results.splitlines()
  del (game_results[0])
  return game_results

def MakeNewGameDict(tag, game_results):
  game_dict = {}
  game_dict.fromkeys(game_fields)

  players = (game_results[2].encode("utf-8"), game_results[3].encode("utf-8"))
  if tag not in players:
    print "WARNING: tag is neither P1 nor P2"

  game_dict['date_time'] = game_results[4].encode("utf-8")
  game_dict['player1_name'] = min(players)   # max/min provides unique, 
  game_dict['player2_name'] = max(players)   # alphanumeric ordering for every 
                                             # player pair

  p1_is_tag = (game_dict['player1_name'] == tag)
  tag_wins   = (game_results[0] == 'Win')
  game_dict['winning_player'] = ( game_dict['player1_name'] 
                                  if (p1_is_tag is tag_wins)
                                  else game_dict['player2_name'] )

  return players, game_dict

def SaveNewGames( new_games, data_file, object_name ):
  if not new_games:
    print "No games for", data_file
    return

  # Read in file with importlib a la the 
  # "from data.list import the_list" syntax
  module_name = data_file.replace("/", ".") #data/list.py --> data.list.py
  module_name = module_name[:-3]            #data.list.py --> data.list
  module = import_module( module_name )
  list_of_games = getattr(module, object_name)

  # Add the new tags to the master tag list 
  list_of_games = list_of_games + new_games

  #unique-ify the list
  #list_of_games = [ dict(tupleized) for tupleized in set(
  #                           tuple(item.items()) for item in list_of_games)]
  list_of_games = [dict(t) for t in set([tuple(d.items()) for d in list_of_games])]

  # Back up the old tag list
  BackUp(data_file)

  # Save the new tag list
  updated_games_file = open(data_file, 'w+')
  updated_games_file.write("games = " + str(list_of_games))
  updated_games_file.close()

if __name__ == "__main__":
  main()
