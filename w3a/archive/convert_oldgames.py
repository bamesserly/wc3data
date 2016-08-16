import time
from list_of_games_0 import list_of_games

new_list_of_games = open('list_of_games.txt', 'w+')
new_list_of_games.write('list_of_games = [')

n_bugged = 0
for i in list_of_games:
  if i[1] != '1on1':
    print "not a solo game"
    continue
  if i[0] == '' or i[1]=='' or i[2]=='' or i[3]==''or i[4]=='':
    n_bugged +=1
    continue
  P1_name   = i[2]
  winner    = i[0]
  P2_name   = i[3]
  date_time = i[4]
  #print date_time
  #date_time = time.strftime("%m-%d-%Y %H:%M", 
  #                          time.strptime(date_time,'%d-%m-%Y %H:%M'))
  #print date_time
  #dict_string = '{\'player1_name\' : {0}, \'winning_player\' : {1}, \'player2_name\' : {2}, \'date_time\' : {3}}'.format(P1_name, winner, P2_name, date_time)
  game_dict = {'player1_name' : P1_name, 'winning_player' : winner, 'player2_name' : P2_name, 'date_time' : date_time}
  #print dict_string
  new_list_of_games.write(str(game_dict) + ", ")

  #date_time = '08-09-2015 13:50' day-month-year

print n_bugged

new_list_of_games.write("]")
