import requests
from bs4 import BeautifulSoup
from datetime import date
import datetime
import time

game_fields = ['date_time', 'winning_player','player1_name','player2_name']

def GetNewTagsAndGames(tags):
  games = set([])
  set_of_new_players = set([])
  for t in tags:
    tags_analyzed += 1
    if tags_analyzed % 100 == 0:
      print "      ", tags_analyzed, " tags analyzed"
      t1 = time.time()
      print "      time elapsed", t1-t0

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
      #scrape_time += t3-t2 #yeah, 99.98% of the running time is scrape time, mostly in that requests.get(url) command
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

        current_game_time = datetime.datetime.strptime(game_results[4], "%d-%m-%Y %H:%M")

        #we've found a new game
        players, game_dict = MakeNewGameDict(t, game_results, set_of_new_players)

        #add any new players or games to the lists.
        set_of_new_players.update(players)
        games.update([game_dict])

        n_new_games_found += 1

      # Got to the end of the page, going to the next one
      # Following statement is eval-ed only if loop over games on page ends without breaking.
      # If a game causes a break, this statement is not eval-ed.
      else:
        #print "    End page. Going to next page: " + str(page+1)
        page +=1

  return new_tags

def GetGameResults(games_on_page, game_i):
  game_results = games_on_page.contents[game_i].text
  game_results = game_results.splitlines()
  del (game_results[0])
  return game_results

def MakeNewGameDict(tag, game_results, set_of_new_players):
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

if __name__ == "__main__":
  main()
