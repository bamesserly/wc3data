# Given a dict of elos, split into active and retired.
# Also updates active and retired lists.

from datetime import date
import datetime
from dateutil.relativedelta import relativedelta

# Total players
from data.player_info import player_info
# Active players
from data.active_players_dict import active_players
# Retired players
from data.retired_players_dict import retired_players

def LGOR(d):
  g = d['most_recent_game_time']
  return datetime.datetime.strptime(g,'%Y-%m-%d %H:%M')

DEBUG = False
FORCE_RETIREMENT = False

retirement_time = datetime.datetime.today() + relativedelta(months=-6)
#retirement_time = datetime.datetime.strptime(retirement_time, '%Y-%m-%d %H:%M')
print "Retirement cutoff is 6 months prior to today:", retirement_time
print "Force retirement is", FORCE_RETIREMENT

newly_retired_count = 0
reactivated_count   = 0

print "Number of players total:", len(player_info),"\n"
for tag in player_info:
  p = player_info[tag]

  # Retire
  if LGOR(p) < retirement_time:
    if DEBUG:
      print "  Found a tag that should be retired"

    #already retired
    if tag in retired_players:
      if DEBUG:
        print "    Attempted to retire account", tag, "with LGOR", LGOR(p), "but account is already retired. Doing nothing."
      continue
    #newly retired
    else:
      #remove from active
      if tag in active_players:
        #wrongly retired?
        if (not FORCE_RETIREMENT) and (LGOR(p) < LGOR(active_players[tag])):
          print "    WARNING: Account", tag, "has a more recent LGOR in the active_players list."
          print "             Last active time was", LGOR(active_players[tag]),"."
          print "             This account will not be retired."
          print "             Your \'total\' dictionary may not be up-to-date."
          continue
        #rightly retired
        else:
          print "    Removing tag", tag, "from active list"
          del active_players[tag]
          
      #add to retired
      newly_retired_count += 1
      retired_players[tag] = player_info[tag] 
      if DEBUG:
        print "    Retiring tag", tag, "with LGOR", LGOR(p)

  # Active
  else:
    #coming out of retirement
    #remove from retired
    if tag in retired_players:
      reactivated_count += 1
      print "  Account", tag, "coming out of retirement!"
      print "    LGOR was", LGOR(retired_players[tag])
      del retired_players[tag]

    #already active
    if tag in active_players:
      if DEBUG:
        print "  Account", tag, "is already active. Doing nothing."
      continue
    #or add to active
    else:
      active_players[tag] = player_info[tag]
      if DEBUG:
        print "    Account active with LGOR", LGOR(p)

if DEBUG:
  print "\nRetired accounts:", retired_players
  print "Active accounts :", active_players

print "\nNumber of retired accounts", len(retired_players)
print "Number of active accounts", len(active_players)

print "\nNumber of newly retired accounts", newly_retired_count
print "Number of reactivated accounts", reactivated_count

print "\nSaving..."
retired_file = open('data/retired_players_dict.py', 'w+')
retired_file.write("retired_players = " + str(retired_players))
retired_file.close()

active_file = open('data/active_players_dict.py', 'w+')
active_file.write("active_players = " + str(active_players))
active_file.close()
print "Done!"
