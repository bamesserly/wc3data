import operator
import numpy as np
print("Importing games...")
from list_of_games import list_of_games
list_of_players_Elo_G_P = open('list_of_players_Elo_G_P', 'w+')

#TODO ignore case of letters

# Consolodate all games
# list_of_games.extend(list_of_new_games)
print(str(len(list_of_games)) + " games imported. Refining and sorting by date...")

# Remove duplicates, remove games with a 'missing player', and sort list of games by date
unique_list_of_games = [list(t) for t in set(map(tuple, list_of_games))]
refined_unique_list_of_games = []
for x in range (0, len(unique_list_of_games)):
    if unique_list_of_games[x][2] == ""''"":
        pass
    elif unique_list_of_games[x][3] == ""''"":
        pass
    else:
        refined_unique_list_of_games.append(unique_list_of_games[x])
organized_list_of_games = (sorted(refined_unique_list_of_games, key=lambda x: (x[4][8],x[4][9],x[4][3],x[4][4],x[4][0],x[4][1],x[4][11],x[4][12],x[4][14],x[4][15])))
print(("\n" + str(int(len(list_of_games)) - int(len(unique_list_of_games)))) + " duplicates removed.")
print(str((int(len(unique_list_of_games)) - int(len(refined_unique_list_of_games)))) + " null player games removed.")
print("Dates of games range from: " + organized_list_of_games[0][4] + " to " + organized_list_of_games[-1][4] + "\n\nEvaluating player ELOs...")


player_name = str()
player_ELO = int()
player_game_count = int()
player_dictionary = {}
sorted_player_dictionary = {}



# Construct the evaluator
starting_elo = 1500

for x in range (0, len(organized_list_of_games)):
    evaluator = [organized_list_of_games[x][0], organized_list_of_games[x][2], organized_list_of_games[x][3]]
    winner = (evaluator[0])
    player1 = (evaluator[1])
    player2 = (evaluator[2])
    try:
        player1_ELO = (player_dictionary[player1][0])
    except:
        player1_ELO = starting_elo
        player_dictionary[player1] = [starting_elo, 0, 0, 0, 0.0]
    try:
        player2_ELO = (player_dictionary[player2][0])
    except:
        player2_ELO = starting_elo
        player_dictionary[player2] = [starting_elo, 0, 0, 0, 0.0]
    evaluator.extend([player1_ELO, player2_ELO])
    #print(evaluator)
    quotientA = 10 ** (player1_ELO / 400)
    quotientB = 10 ** (player2_ELO / 400)
    expectationA = quotientA / (quotientA + quotientB)
    expectationB = quotientB / (quotientA + quotientB)


# Manage variable k factor
    k_factor_burst = 100
    k_factor_early = 48
    k_factor_mid = 36
    k_factor_late = 24

    k_factor1 = k_factor_late
    k_factor2 = k_factor_late

    if player_dictionary[player1][0] < 2400:
        k_factor1 = k_factor_mid
    if player_dictionary[player2][0] < 2400:
        k_factor2 = k_factor_mid

    if player_dictionary[player1][1] <= 30 and player_dictionary[player1][0] < 2300:
        k_factor1 = k_factor_early
    if player_dictionary[player2][1] <= 30 and player_dictionary[player1][0] < 2300:
        k_factor2 = k_factor_early

    if player_dictionary[player1][1] <= 5 and player_dictionary[player1][0] < 1800:
        k_factor1 = k_factor_burst
    if player_dictionary[player2][1] <= 5 and player_dictionary[player1][0] < 1800:
        k_factor1 = k_factor_burst

# Adjust Elo
    if winner == player1:
        player1_ELO = player1_ELO + k_factor1 * (1 - expectationA)
    if winner != player1:
        player1_ELO = player1_ELO + k_factor1 * (0 - expectationA)
    player_dictionary[player1][0] = int(player1_ELO)
    player_dictionary[player1][1] += 1
    if winner == player2:
        player2_ELO = player2_ELO + k_factor2 * (1 - expectationB)
    if winner != player2:
        player2_ELO = player2_ELO + k_factor2 * (0 - expectationB)
    player_dictionary[player2][0] = int(player2_ELO)
    player_dictionary[player2][1] += 1
    if winner == player1:
        player_dictionary[player1][2] += 1
        player_dictionary[player2][3] += 1
    if winner == player2:
        player_dictionary[player2][2] += 1
        player_dictionary[player1][3] += 1
    player_dictionary[player1][4] = round((player_dictionary[player1][2] / (player_dictionary[player1][2] + player_dictionary[player1][3]))*100, 2)
    player_dictionary[player2][4] = round((player_dictionary[player2][2] / (player_dictionary[player2][2] + player_dictionary[player2][3]))*100, 2)
#print(player_dictionary)

# Organize and analyze final Elos
elo_sorted_player_list = sorted(player_dictionary.items(), key=operator.itemgetter(1,0), reverse = True)
refined_elo_sorted_player_list = []

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
# print("\n" + str(len(organized_list_of_games)) + " games used to assign "+ str(len(refined_elo_sorted_player_list)) + " players an ELO ranging from " + str(refined_elo_sorted_player_list[0][1][0]) + " to " + str(refined_elo_sorted_player_list[-1][1][0]) + "\n")
#
# elo_list = []
# for x in range (len(refined_elo_sorted_player_list)):
#     elo_list.append(refined_elo_sorted_player_list[x][1][0])
#
# y = int()
# for y in range (100, -1, -10):
#     p = np.percentile(elo_list, y, axis=None, out=None, overwrite_input=False, interpolation='linear')
#     print (str(p) + " = " + str(y) + "th percentile")


list_of_players_Elo_G_P.write(str(elo_sorted_player_list))
list_of_players_Elo_G_P.close()