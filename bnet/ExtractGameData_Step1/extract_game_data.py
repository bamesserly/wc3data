# coding: utf-8
#!/usr/bin/python

## Modules
import fileinput
import glob
import datetime
import time

game_fields = ['date_time', 'winning_player',
               'player1_name', 'player1_race', 'player1_level', 
               'player2_name', 'player2_race', 'player2_level']
races = ["Orc","Human","Night","Undead"]

def main():
  good_games = 0
  total_games = 0
  short_games = 0
  bugged_games = 0
  game_list = []

  Wfile = open("list_of_games.py", "w")

  #Loop file lines
  for line in fileinput.input(glob.glob("/Users/Ben/Desktop/Misc_Docs/wcscans/processedFiles/Solo/game*.txt")):
    #print fileinput.filename()

    #Make sure game is greater than zero mins
    if fileinput.filelineno()==5: 
      if "Game Length: 0 minutes" in line:
        #print "Game Length Zero"
        fileinput.nextfile()
        short_games += 1
      if "Game Length: 1 minutes" in line:
        #print "Game Length One"
        fileinput.nextfile()
        short_games += 1

    #Make sure game is solo
    if fileinput.filelineno()==4:
      if "Solo" not in line:
        print "Not Solo"
        fileinput.nextfile()


    if fileinput.isfirstline(): # First line, initialize
      #print fileinput.filename()
      game_info = {}
      game_info.fromkeys(game_fields)
      total_games += 1

    #Get game date/time
    if fileinput.filelineno()==2:
      game_info['date_time'] = get_date_time(line)

    #player names, races, levels, winner
    try:
      if fileinput.filelineno()==7:
        game_info['player1_name'] = get_player_name(line)
        game_info['player1_race'] = get_player_race(line)

      if fileinput.filelineno()==8:
        game_info['player1_level'] = get_player_level(line)

      if fileinput.filelineno()==10:
        game_info['player2_name'] = get_player_name(line)
        game_info['player2_race'] = get_player_race(line)

      if fileinput.filelineno()==11:
        game_info['player2_level'] = get_player_level(line)

      if fileinput.filelineno()==12:
        game_info['winning_player'] = get_winning_player(line, game_info)

    except:
      bugged_games += 1
      fileinput.nextfile()

    #finalize
    if fileinput.filelineno()>12:
      if any (field not in game_info for field in game_fields):
        print "One of the fields for this game is empty, failed to read game."
        fileinput.nextfile()
      else:
        good_games += 1
        game_list.append(game_info)
        if good_games % 1000 == 0:
          print "Scanned over " + str(good_games) + " games"
        fileinput.nextfile()

  print "Short games not counted = " + str(short_games)
  print "Bugged games not counted = " + str(bugged_games)
  print "Good games = " + str(good_games)
  print "Total games = " + str(total_games)
  #print "\n".join(str(v) for v in game_list)
  Wfile.write("list_of_games = " + str(game_list))

def get_player_name(line):
  player = line.split(" ")[0]
  return player

def get_player_level(line):
  return int(line)

def get_player_race(line):
  return [race for race in races if race in line][0]

def get_date_time(line):
  date_time = (" ").join(line.split(" ")[4:7])
  date_time = time.strftime("%d-%m-%Y %H:%M", 
                            time.strptime(date_time,'%m/%d/%Y %I:%M:%S %p'))
  return date_time

def get_winning_player(line, game_info):
  if(line.find("Win")>0):
    return game_info['player2_name']
  elif (line.find("Loss")>0):
    return game_info['player1_name']
  else:
    return None

if __name__ == "__main__":
  main()
