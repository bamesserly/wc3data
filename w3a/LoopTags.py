from bs4 import BeautifulSoup
from datetime import date
import requests
import datetime
import time
import Utils

# need for get_LGOR
#from data.active_tags_info  import active_tags
#from data.retired_tags_info import retired_tags
from data.all_tags_info import all_tags

from Constants import all_tags_list_file, all_tags_list_container #input
from Constants import all_games_file,   all_games_container   #output
from Constants import query_delay, game_fields, earliest_time


def LoopTags(tags, build):
  print "  Entering LoopTags()"

  found_games = []
  found_tags  = set([])

  t0 = time.time()
  tags_analyzed = 0
  for t in tags:

    # Slow down scraping for w3a servers
    if not build:
      time.sleep(query_delay)

    # Get games until finding LGOR or until no more games
    page = 0
    n_new_games_found = 0
    LGOR = get_LGOR(t, build) # Last game on record.
    #print LGOR
    keep_searching_for_games = True
    while (keep_searching_for_games):
      games_on_page = get_games_on_page(t, page)   #special BSoup container.

      # try to find games on this page
      try:
        number_of_games_on_page = len(games_on_page)

      #No more games found. Break.
      except TypeError:
        keep_searching_for_games = False
        break

      # Loop found games
      for game_i in range(0, number_of_games_on_page):
        try:
          game_results = get_game_results(games_on_page, game_i)
        except AttributeError:
          #there can be "\n" in games_on_page.contents[game_i]
          #test: games_on_page.contents[game_i].isspace()
          continue

        if game_results[1] != "1on1":
          continue

        current_game_time = datetime.datetime.strptime(game_results[4], "%d-%m-%Y %H:%M")

        # We're all caught up. next tag.
        if current_game_time == LGOR:
          keep_searching_for_games = False
          break # out of list of games on this page

        # Found a game
        elif current_game_time > LGOR:
          competitors, game_dict = make_game_dict(t, game_results)
          n_new_games_found += 1

          # Update lists
          found_tags.update(competitors)
          found_games.append(game_dict)

        #current_game_time < LGOR:
        #Problem: We somehow missed the last game on record.
        #Current behavior: don't add this game or any further games to the list.
        else:
          print "    WARNING: the last game on record happened after the game under current consideration."
          keep_searching_for_games = False
          break # out of list of games on this page


      # End Page. Go to next page.
      # Eval-ed only if page's games loop ends without breaking.
      else:
        page += 1

    print "   ", t, "--", n_new_games_found, "games found"
    tags_analyzed += 1
    if tags_analyzed % 25 == 0:
      print_status(t0, tags_analyzed)


  # For build mode, save progress at the end of iteration
  #if build:
  #  #Utils.back_up(all_games_file)
  #  #Utils.back_up(all_tags_list_file)

  #  Utils.update_file(all_games_file, all_games_container, found_games, 'd')
  #  Utils.update_file(all_tags_list_file,  all_tags_list_container,  found_tags, 'l')

  # Until we're running more smoothly, we need to save on every iteration
  Utils.update_file(all_games_file, all_games_container, found_games, 'l_d')
  Utils.update_file(all_tags_list_file,  all_tags_list_container,  found_tags, 'l')

  print "  Exiting LoopTags()"
  return found_games, found_tags

def get_LGOR(t, build):
  if build:
    LGOR = earliest_game

  # This is slow, but alternatives not great either. 
  elif t in all_tags:
    LGOR = all_tags[t]['most_recent_game_time']
    LGOR = datetime.datetime.strptime(LGOR,'%Y-%m-%d %H:%M')

  # New account
  else:
    LGOR = earliest_game

  return LGOR

def get_games_on_page(t, page):
  url = "http://tft.w3arena.net/profile/{0}/?p={1}".format(t, page)
  r = requests.get(url)
  soup = BeautifulSoup(r.content, 'html.parser')
  games_on_page = soup.find("table", {"class": "StyledTable"})
  return games_on_page

def get_game_results(games_on_page, game_i):
  game_results = games_on_page.contents[game_i].text
  game_results = game_results.splitlines()
  del (game_results[0])
  return game_results

def make_game_dict(tag, game_results):
  game_dict = {}
  game_dict.fromkeys(game_fields)

  competitors = (game_results[2].encode("utf-8"), game_results[3].encode("utf-8"))
  if tag not in competitors:
    print "WARNING: tag is neither P1 nor P2"

  game_dict['date_time'] = game_results[4].encode("utf-8")
  game_dict['player1_name'] = min(competitors)   # max/min provides unique, 
  game_dict['player2_name'] = max(competitors)   # alphanumeric ordering for 
                                                 # every player pair

  p1_is_tag = (game_dict['player1_name'] == tag)
  tag_wins   = (game_results[0] == 'Win')
  game_dict['winning_player'] = ( game_dict['player1_name'] 
                                  if (p1_is_tag is tag_wins)
                                  else game_dict['player2_name'] )

  return competitors, game_dict

def print_status(t0, tags_analyzed):
  print "\n    ====", tags_analyzed, " tags analyzed"
  t1 = time.time()
  print "    ==== time elapsed during this iteration", t1-t0, "\n"

if __name__ == "__main__":
  LoopTags() 

'''
  import glob
  def SaveNewGames( new_games, data_file, object_name ):
    if not new_games:
      print "      No games for", data_file, "during this iteration."
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

    # Back up the old game list
    #BackUp(data_file)

    # Save the new comprehensive game list
    updated_games_file = open(data_file, 'w+')
    updated_games_file.write("games = " + str(list_of_games))
    updated_games_file.close()

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

  all_tags = Utils.load_data(all_tags_file, all_tags_container)
  all_tags.update(found_tags)

  all_tags_file = open('data/all_tags.py', 'w+')
  all_tags_file.write("all_tags = " + str(all_tags))
  all_tags_file.close()

  # Return the new tags
  ###############
  ## Tags Stuff #
  ###############
  # Get the most current master tag list
  from data.list_of_existing_players import existing_players
  set_of_existing_tags = set(existing_players)
  #maybe this isn't working?

  # Create the return_tag_list which contains all the elements 
  # in set_of_new_tags and not in set_of_existing_tags.
  return_tags = set_of_new_tags.difference( set_of_existing_tags ) 

  # Add the new tags to the master tag list 
  set_of_existing_tags.update(set_of_new_tags)

  # Back up the old tag list

  # Save the new tag list

  ################
  ## Games Stuff #
  ################
  SaveNewGames(games2015, "data/games2015.py", "games")
  SaveNewGames(games2016, "data/games2016.py", "games")
  SaveNewGames(games2017, "data/games2017.py", "games")

  return found_games, found_tags
'''
