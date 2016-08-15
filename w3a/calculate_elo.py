import operator
import numpy as np
import csv
from datetime import date
import datetime

K_FACTOR_BURST = 100
K_FACTOR_EARLY = 48
K_FACTOR_MID   = 36
K_FACTOR_LATE  = 24

# player_dictionary format: 
# {'playerXname': {player_dictionary}, 'playerYname' : {player_dictionary}, ...}

def main():
  from list_of_games import list_of_games

  list_of_elos = open('list_of_elos.py', 'w+')

  # Consolodate all games
  print(str(len(list_of_games)) + " games imported. Refine and sort by date...")

  # Remove duplicates, remove games with a 'missing player'
  list_of_games = [ dict(tupleized) for tupleized in set(
                              tuple(item.items()) for item in list_of_games)]
  # sort list of games by date
  list_of_games = sorted(list_of_games, key=lambda k: 
      datetime.datetime.strptime(k['date_time'], '%d-%m-%Y %H:%M'))  
 
  print "after removing duplicates..."
  print "length of list of games = " + str(len(list_of_games))

  player_dictionaries = {}
  for x in list_of_games:
    starting_elo = 1500.
    winner = x['winning_player']
    player1 = x['player1_name']
    player2 = x['player2_name']
    game_date_time = x['date_time']

    if not player1 in player_dictionaries:
      player_dictionaries[player1] = {'tag':player1, 'elo':starting_elo,
                                      'ngames':0,'wins':0,'losses':0,'winrate':0.,
                                      'most_recent_game_time': game_date_time}
    elif (datetime.datetime.strptime(game_date_time, '%d-%m-%Y %H:%M') < 
        datetime.datetime.strptime(player_dictionaries[player1]['most_recent_game_time'],'%d-%m-%Y %H:%M')):
      raise Exception("P1'S MOST RECENT GAME IS AFTER CURRENT GAME")

    if not player2 in player_dictionaries:
      player_dictionaries[player2] = {'tag':player2, 'elo':starting_elo,
                                      'ngames':0,'wins':0,'losses':0,'winrate':0.,
                                      'most_recent_game_time': game_date_time}
    elif (datetime.datetime.strptime(game_date_time, '%d-%m-%Y %H:%M') < 
        datetime.datetime.strptime(player_dictionaries[player2]['most_recent_game_time'],'%d-%m-%Y %H:%M')):
      raise Exception("P2'S MOST RECENT GAME IS AFTER CURRENT GAME")

    (new_player1_elo, new_player2_elo) = calculate_new_elos(
        player_dictionaries[player1], player_dictionaries[player2], winner)

    player_dictionaries[player1]['elo'] = round((new_player1_elo),2)
    player_dictionaries[player2]['elo'] = round((new_player2_elo),2)

    adjust_W_L(player_dictionaries[player1],player_dictionaries[player2],winner)
   
    player_dictionaries[player1]['most_recent_game_time'] = game_date_time
    player_dictionaries[player2]['most_recent_game_time'] = game_date_time
    

  elo_list = []
  player_dict_list = []
  for x in player_dictionaries:
    elo_list.append(player_dictionaries[x]['elo'])
    player_dict_list.append(player_dictionaries[x])

  make_elo_spreadsheet(player_dict_list)

  y = int()
  for y in range (100, -1, -10):
    p = np.percentile(elo_list, y, axis=None, out=None, overwrite_input=False, 
        interpolation='linear')
    print (str(p) + " = " + str(y) + "th percentile")

  elo_sorted_player_list = sorted(player_dictionaries.items(), 
      key=operator.itemgetter(1,0), reverse = True)

  list_of_elos.write(str(elo_sorted_player_list))
  list_of_elos.close()

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

  return (temp_P1_elo, temp_P2_elo)

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

def make_elo_spreadsheet(player_dict_list):
  today = (date.today()).strftime("%y%m%d")
  spreadsheet_name = "EloSpreadSheet_{0}.csv".format(today)
  with open(spreadsheet_name, 'w') as csvfile:
    #header = ['Elos {0}'.format(today)]
    fieldnames = ['tag', 'elo', 'ngames', 'wins','losses','winrate','most_recent_game_time']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    #writer.writer.writerow(header)
    writer.writer.writerow(fieldnames)
    X = [writer.writerow(dict) for dict in player_dict_list]

if __name__ == "__main__":
  main()
