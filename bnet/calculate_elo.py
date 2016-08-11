import operator
import numpy as np
#print("Importing games...")

#player_fields = ['elo','ngames','wins','losses','winrate']

def main():
  #from list_of_games import list_of_games
  from list_of_games import list_of_games

  list_of_elos = open('list_of_elos', 'w+')

  #TODO ignore case of letters

  # Consolodate all games
  # list_of_games.extend(list_of_new_games)
  print(str(len(list_of_games)) + " games imported. Refining and sorting by date...")

  # Remove duplicates, remove games with a 'missing player', and sort list of games by date
  list_of_games = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in list_of_games)]
  #print list_of_games
  list_of_games = sorted(list_of_games, key=lambda k: k['date_time'])  
  #print "\n"
  #print list_of_games
  
  #print("\nDates of games range from: " + list_of_games[0]['date_time'] + " to " + list_of_games[-1]['date_time'] + "\n\nEvaluating player elos...")


  player_name = str()
  player_elo = int()
  player_game_count = int()
  player_dictionary = {}
  sorted_player_dictionary = {}

  # Construct the evaluator

  """
  game_n: check if key exists for player. If not, make an exmpty one. If so, update its entries
  """
  player_dictionaries = {}
  #for x in range (0, len(list_of_games)):
  for x in list_of_games:
    starting_elo = 1500.
    winner = x['winning_player']
    player1 = x['player1_name']
    player2 = x['player2_name']

    #player_dictionaries = {'playerXname': player_dictionary, 'playerYname' : player_dictionary}

    if player1 in player_dictionaries:
      temp_player1_elo = player_dictionaries[player1]['elo']
    else:
      player_dictionaries[player1] = {'elo': starting_elo,'ngames':0,'wins':0,'losses':0,'winrate':0.}
      temp_player1_elo = player_dictionaries[player1]['elo']

    if player2 in player_dictionaries:
      temp_player2_elo = player_dictionaries[player2]['elo']
    else:
      player_dictionaries[player2] = {'elo': starting_elo,'ngames':0,'wins':0,'losses':0,'winrate':0.}
      temp_player2_elo = player_dictionaries[player2]['elo']

    #evaluator.extend([player1_elo, player2_elo])
    #print(evaluator)

    quotientA = 10 ** (temp_player1_elo / 400)
    quotientB = 10 ** (temp_player2_elo / 400)
    expectationA = quotientA / (quotientA + quotientB)
    expectationB = quotientB / (quotientA + quotientB)

    # Manage variable k factor
    k_factor_burst = 100
    k_factor_early = 48
    k_factor_mid = 36
    k_factor_late = 24

    k_factor1 = k_factor_late
    k_factor2 = k_factor_late

    if player_dictionaries[player1]['elo'] < 2400:
      k_factor1 = k_factor_mid
    if player_dictionaries[player2]['elo'] < 2400:
      k_factor2 = k_factor_mid

    if player_dictionaries[player1]['ngames'] <= 30 and player_dictionaries[player1]['elo'] < 2300:
      k_factor1 = k_factor_early
    if player_dictionaries[player2]['ngames'] <= 30 and player_dictionaries[player2]['elo'] < 2300:
      k_factor2 = k_factor_early

    if player_dictionaries[player1]['ngames'] <= 5 and player_dictionaries[player1]['elo'] < 1800:
      k_factor1 = k_factor_burst
    if player_dictionaries[player2]['ngames'] <= 5 and player_dictionaries[player1]['elo'] < 1800:
      k_factor1 = k_factor_burst

    # Adjust Elo
    if winner == player1:
      temp_player1_elo = temp_player1_elo + k_factor1 * (1 - expectationA)
      temp_player2_elo = temp_player2_elo + k_factor2 * (0 - expectationB)
      #print player1 + " beat " + player2 + " on " + x['date_time']
    elif winner == player2:
      temp_player1_elo = temp_player1_elo + k_factor1 * (0 - expectationA)
      temp_player2_elo = temp_player2_elo + k_factor2 * (1 - expectationB)
      #print player2 + " beat " + player1 + " on " + x['date_time']
    player_dictionaries[player1]['elo'] = round((temp_player1_elo),2)
    player_dictionaries[player2]['elo'] = round((temp_player2_elo),2)

    # Adjust W/L/WR
    player_dictionaries[player1]['ngames'] += 1
    player_dictionaries[player2]['ngames'] += 1
    if winner == player1:
      player_dictionaries[player1]['wins'] += 1
      player_dictionaries[player2]['losses'] += 1
      player_dictionaries[player1]['winrate'] = (player_dictionaries[player1]['wins'] / float(player_dictionaries[player1]['wins'] + player_dictionaries[player1]['losses']))*100
      player_dictionaries[player2]['winrate'] = (player_dictionaries[player2]['wins'] / float(player_dictionaries[player2]['wins'] + player_dictionaries[player2]['losses']))*100
    if winner == player2:
      player_dictionaries[player2]['wins'] += 1
      player_dictionaries[player1]['losses'] += 1
      player_dictionaries[player1]['winrate'] = (player_dictionaries[player1]['wins'] / float(player_dictionaries[player1]['wins'] + player_dictionaries[player1]['losses']))*100
      player_dictionaries[player2]['winrate'] = (player_dictionaries[player2]['wins'] / float(player_dictionaries[player2]['wins'] + player_dictionaries[player2]['losses']))*100


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


  """
  list_of_elos.write(str(elo_list))
  list_of_players_Elo_G_P.close()


  #print player_dictionaries

  #for i in player_dictionaries:
  #  print str(i) + str(player_dictionaries[i])
  #print "\n".join(str(w) for v,w in player_dictionaries[v][w])

  #print(player_dictionary)

  # Organize and analyze final Elos

  for x in range (0, len(elo_sorted_player_list)):
    try:
      if str(elo_sorted_player_list[x][1][1]) == "1" or str(elo_sorted_player_list[x][1][1]) == "2" or str(elo_sorted_player_list[x][1][1]) == "3" or str(elo_sorted_player_list[x][1][1]) == "4" or str(elo_sorted_player_list[x][1][1]) == "5" or str(elo_sorted_player_list[x][1][1]) == "6" or str(elo_sorted_player_list[x][1][1]) == "7" or str(elo_sorted_player_list[x][1][1]) == "8" or str(elo_sorted_player_list[x][1][1]) == "9":
        # print(elo_sorted_player_list[x])
        pass
      else:
        refined_elo_sorted_player_list.append(elo_sorted_player_list[x])
    except:
      pass

  print(elo_sorted_player_list)

  # for x in range(0, len(refined_elo_sorted_player_list)):
  #     print(str(refined_elo_sorted_player_list[x][1][0]) + "  " + str(refined_elo_sorted_player_list[x][0]) + " (" + str(refined_elo_sorted_player_list[x][1][1]) + " games played)")
  #
  # print("\n" + str(len(list_of_games)) + " games used to assign "+ str(len(refined_elo_sorted_player_list)) + " players an elo ranging from " + str(refined_elo_sorted_player_list[0][1][0]) + " to " + str(refined_elo_sorted_player_list[-1][1][0]) + "\n")
  #
  # elo_list = []
  # for x in range (len(refined_elo_sorted_player_list)):
  #     elo_list.append(refined_elo_sorted_player_list[x][1][0])
  #
  # y = int()
  # for y in range (100, -1, -10):
  #     p = np.percentile(elo_list, y, axis=None, out=None, overwrite_input=False, interpolation='linear')
  #     print (str(p) + " = " + str(y) + "th percentile")


  """

if __name__ == "__main__":
  main()
