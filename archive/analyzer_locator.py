from list_of_players import list_of_new_players
# from list_of_games import list_of_games

for x in range (0, len(list_of_new_players)):
    if str(list_of_new_players[x][0]) == "ZaMeS":
        print("ZaMeS " + str(x) +"th position")
    else:
        pass
print(len(list_of_new_players))

# for x in range (0, len(list_of_games)):
#     if str(list_of_games[x][2]) == "faceorc":
#         if str(list_of_games[x][3]) == "GuessWho":
#             print(list_of_games[x])
#     if str(list_of_games[x][3]) == "faceorc":
#         if str(list_of_games[x][2]) == "GuessWho":
#             print(list_of_games[x])
