import operator
import numpy as np

K_FACTOR_BURST = 100
K_FACTOR_EARLY = 48
K_FACTOR_MID   = 36
K_FACTOR_LATE  = 24

# player_dictionary format: 
# {'playerXname': player_dictionary, 'playerYname' : player_dictionary, ...}

def main():
  #from list_of_games_short import list_of_games
  from list_of_games import list_of_games

  #list_of_elos = open('list_of_elos', 'w+')
  list_of_elos = open('cache.txt', 'w+')

  # Consolodate all games
  print(str(len(list_of_games)) + " games imported. Refining and sorting by date...")

  # Remove duplicates, remove games with a 'missing player'
  # sort list of games by date
  list_of_games = [ dict(tupleized) for tupleized in set(
                              tuple(item.items()) for item in list_of_games)]
  list_of_games = sorted(list_of_games, key=lambda k: k['date_time'])  

  #print list_of_games
  
  player_name = str()
  player_elo = int()
  player_game_count = int()
  player_dictionary = {}
  sorted_player_dictionary = {}

  """
  game_n: check if key exists for player. If not, make an empty one. If so, update its entries.
  """
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
    elif max((player_dictionaries[player1]['most_recent_game_time'],game_date_time)) is not game_date_time:
      print "WARNING P1'S MOST RECENT GAME AFTER CURRENT GAME"

    if not player2 in player_dictionaries:
      player_dictionaries[player2] = {'tag':player2, 'elo':starting_elo,
                                      'ngames':0,'wins':0,'losses':0,'winrate':0.,
                                      'most_recent_game_time': game_date_time}
    elif max((player_dictionaries[player2]['most_recent_game_time'],game_date_time)) is not game_date_time:
      print "WARNING P2'S MOST RECENT GAME AFTER CURRENT GAME"

    (new_player1_elo, new_player2_elo) = update_elos(player_dictionaries[player1],
                                                   player_dictionaries[player2],
                                                   winner)

    print new_player1_elo
    print new_player2_elo

    player_dictionaries[player1]['elo'] = round((new_player1_elo),2)
    player_dictionaries[player2]['elo'] = round((new_player2_elo),2)

  elo_list = []
  for x in player_dictionaries:
    elo_list.append(player_dictionaries[x]['elo'])
    
  y = int()
  for y in range (100, -1, -10):
    p = np.percentile(elo_list, y, axis=None, out=None, overwrite_input=False, interpolation='linear')
    print (str(p) + " = " + str(y) + "th percentile")

  elo_sorted_player_list = sorted(player_dictionaries.items(), key=operator.itemgetter(1,0), reverse = True)

  list_of_elos.write(str(elo_sorted_player_list))
  list_of_elos.close()

def update_elos(P1dict, P2dict, winner):
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

def adjust_W_L():
  # Adjust W/L/WR
  player1dict['ngames'] += 1
  player2dict['ngames'] += 1
  if winner == player1:
    player1dict['wins'] += 1
    player2dict['losses'] += 1
    player1dict['winrate'] = (player1dict['wins'] / float(player1dict['wins'] + player1dict['losses']))*100
    player2dict['winrate'] = (player2dict['wins'] / float(player2dict['wins'] + player2dict['losses']))*100
  if winner == player2:
    player2dict['wins'] += 1
    player1dict['losses'] += 1
    player1dict['winrate'] = (player1dict['wins'] / float(player1dict['wins'] + player1dict['losses']))*100
    player2dict['winrate'] = (player2dict['wins'] / float(player2dict['wins'] + player2dict['losses']))*100

def set_k_factor(elo, ngames):
  k_factor = K_FACTOR_LATE
  if elo < 2400:
    k_factor = K_FACTOR_MID

  if ngames <= 30 and elo < 2300:
    k_factor1 = K_FACTOR_EARLY

  if ngames <= 5 and elo < 1800:
    k_factor1 = K_FACTOR_BURST

  return k_factor

if __name__ == "__main__":
  main()
