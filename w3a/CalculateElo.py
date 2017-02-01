import operator
import numpy as np
import datetime
import time
import os
from datetime import date
from shutil import copy

import Utils

from Constants import K_FACTOR_BURST, K_FACTOR_EARLY
from Constants import K_FACTOR_LATE,  K_FACTOR_MID  
from Constants import STARTING_ELO_CONST

from Constants import all_games_file,   all_games_container   #input
from Constants import all_tags_file,    all_tags_container    #output

# player_dictionary format: 
# {'playerXname': {player_dictionary}, 'playerYname' : {player_dictionary}, ...}

def CalculateElo():
  print "Entering CalculateElo()"

  games = Utils.load_data(all_games_file, all_games_container)

  print "  Games imported",len(games), "Refine and sort by date..."

  games = Utils.remove_duplicates(games)

  # sort by date
  games = sorted(games, key=lambda k: 
      datetime.datetime.strptime(k['date_time'], '%d-%m-%Y %H:%M'))  
 
  print "  After removing duplicates..."
  print "  Length of list of games =",len(games)

  all_tags = {}
  empty_player_counter = 0
  for g in games:
    starting_elo   = STARTING_ELO_CONST
    winner         = g['winning_player']
    player1        = g['player1_name']
    player2        = g['player2_name']
    game_date_time = g['date_time']
    game_date_time = time.strftime("%Y-%m-%d %H:%M", time.strptime(game_date_time,"%d-%m-%Y %H:%M"))

    if player1 is "" or player2 is "":
      empty_player_counter += 1
      continue

    if not player1 in all_tags:
      all_tags[player1] = {'tag'                  : player1, 
                           'elo'                  : starting_elo,
                           'ngames'               : 0,       
                           'wins'                 : 0, 
                           'losses'               : 0,       
                           'winrate'              : 0., 
                           'most_recent_game_time': game_date_time
                          }

    #elif (game_time(game_date_time) < LGOR(all_tags[player1])):
    #  raise Exception("P1'S MOST RECENT GAME IS AFTER CURRENT GAME")

    if not player2 in all_tags:
      all_tags[player2] = {'tag'                  : player2,
                           'elo'                  : starting_elo,
                           'ngames'               : 0,
                           'wins'                 : 0,
                           'losses'               : 0,
                           'winrate'              : 0.,
                           'most_recent_game_time': game_date_time
                          }

    #elif (game_time(game_date_time) < LGOR(all_tags[player2])):
    #  raise Exception("P2'S MOST RECENT GAME IS AFTER CURRENT GAME")

    (new_player1_elo, new_player2_elo) = calculate_new_elos( all_tags[player1], 
                                                             all_tags[player2], 
                                                             winner )

    all_tags[player1]['elo'] = round((new_player1_elo),3)
    all_tags[player2]['elo'] = round((new_player2_elo),3)

    adjust_W_L( all_tags[player1], all_tags[player2], winner)
   
    all_tags[player1]['most_recent_game_time'] = game_date_time
    all_tags[player2]['most_recent_game_time'] = game_date_time
    
  elo_list = []
  player_dict_list = []
  for p in all_tags:
    elo_list.append(all_tags[p]['elo'])
    player_dict_list.append(all_tags[p])

  y = int()
  for y in range (100, -1, -10):
    p = np.percentile(elo_list, y, axis=None, out=None, overwrite_input=False, 
        interpolation='linear')
    print (str(p) + " = " + str(y) + "th percentile")

  elo_sorted_player_list = sorted( all_tags.items(), 
                                   key=operator.itemgetter(1,0), 
                                   reverse = True )

  print "  max elo =", elo_sorted_player_list[0]
  print "  min elo =", elo_sorted_player_list[-1]

  print "  empty player counter =", empty_player_counter

  #Utils.back_up(all_tags_file)
  Utils.update_file(all_tags_file, all_tags_container, all_tags, 'd')

  print "Exiting CalculateElo()"

def calculate_new_elos(P1dict, P2dict, winner):
  temp_P1_elo = P1dict['elo']
  temp_P2_elo = P2dict['elo']

  quotientA = 10 ** (temp_P1_elo / 400)
  quotientB = 10 ** (temp_P2_elo / 400)
  expectationA = quotientA / (quotientA + quotientB)
  expectationB = quotientB / (quotientA + quotientB)

  k_factor1 = set_k_factor(P1dict['elo'], P1dict['ngames'])
  k_factor2 = set_k_factor(P2dict['elo'], P2dict['ngames'])

  # Adjust Elo
  if winner == P1dict['tag']:
    temp_P1_elo = temp_P1_elo + k_factor1 * (1 - expectationA)
    temp_P2_elo = temp_P2_elo + k_factor2 * (0 - expectationB)
  elif winner == P2dict['tag']:
    temp_P1_elo = temp_P1_elo + k_factor1 * (0 - expectationA)
    temp_P2_elo = temp_P2_elo + k_factor2 * (1 - expectationB)

  return (round(temp_P1_elo,6), round(temp_P2_elo,6))

def adjust_W_L(P1dict,P2dict,winner):
  if winner == P1dict['tag']:
    P1dict['ngames'] += 1
    P2dict['ngames'] += 1
    P1dict['wins'] += 1
    P2dict['losses'] += 1
    P1dict['winrate'] = round(P1dict['wins'] / float(P1dict['wins'] + P1dict['losses']),4)
    P2dict['winrate'] = round(P2dict['wins'] / float(P2dict['wins'] + P2dict['losses']),4)
  elif winner == P2dict['tag']:
    P1dict['ngames'] += 1
    P2dict['ngames'] += 1
    P2dict['wins'] += 1
    P1dict['losses'] += 1
    P1dict['winrate'] = round(P1dict['wins'] / float(P1dict['wins'] + P1dict['losses']),4)
    P2dict['winrate'] = round(P2dict['wins'] / float(P2dict['wins'] + P2dict['losses']),4)
  else:
    print "WARNING in adjust_W_L: winner is neither player1 nor player 2"

def set_k_factor(elo, ngames):
  k_factor = K_FACTOR_LATE
  if elo < 2400:
    k_factor = K_FACTOR_MID

  if ngames <= 30 and elo < 2300:
    k_factor = K_FACTOR_EARLY

  if ngames <= 5 and elo < 1800:
    k_factor = K_FACTOR_BURST

  return k_factor

def LGOR(d):
  g = d['most_recent_game_time']
  return datetime.datetime.strptime(g,'%Y-%m-%d %H:%M')

def game_time(g):
  return datetime.datetime.strptime(g,'%Y-%m-%d %H:%M')

if __name__ == "__main__":
  CalculateElo()
