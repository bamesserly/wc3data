# Given a dict of elos, split into active and retired.
# Also updates active and retired lists.
from datetime import date
from dateutil.relativedelta import relativedelta
import datetime
import Utils

from Constants import force_retirement, DEBUG
from Constants import seed_cutoff_days,  retirement_cutoff_months
from Constants import all_tags_file,     all_tags_container
from Constants import active_tags_file,  active_tags_container
from Constants import retired_tags_file, retired_tags_container
from Constants import seed_tags_file,    seed_tags_container

def UpdateActiveTags():
  print "Entering UpdateActiveTags()"
  all_tags     = Utils.load_data(all_tags_file,     all_tags_container)
  active_tags  = Utils.load_data(active_tags_file,  active_tags_container)
  retired_tags = Utils.load_data(retired_tags_file, retired_tags_container)
  seed_tags    = {} #write this fresh every time

  retirement_time = (datetime.datetime.today() + 
                                 relativedelta(months=-retirement_cutoff_months))
  seed_time = (datetime.datetime.today() + relativedelta(days=-seed_cutoff_days))

  print "  Retirement cutoff is", retirement_cutoff_months, "months prior to today:", retirement_time
  print "  Force retirement is", force_retirement
  print "  Seed accounts have played a game in the last", seed_cutoff_days, "days:", seed_time

  newly_retired_count = 0
  reactivated_count   = 0
  LGOR_tot = 0

  print "  Number of tags total:", len(all_tags),"\n"
  for tag in all_tags:
    t = all_tags[tag]
    
    # Seed
    if LGOR(t) > seed_time:
      seed_tags[tag] = t

    # Retire
    if LGOR(t) < retirement_time:
      if DEBUG:
        print "  Found a tag that should be retired"

      #already retired
      if tag in retired_tags:
        if DEBUG:
          print "    Attempted to retire account", tag, "with LGOR", LGOR(t), "but account is already retired. Doing nothing."
        continue
      #newly retired
      else:
        #remove from active
        if tag in active_tags:
          #wrongly retired?
          if (not force_retirement) and (LGOR(t) < LGOR(active_tags[tag])):
            print "    WARNING: Account", tag, "has a more recent LGOR in the active_tags list."
            print "             Last active time was", LGOR(active_tags[tag])
            print "             This account will not be retired."
            print "             Your \'total\' dictionary may not be up-to-date."
            continue
          #rightly retired
          else:
            print "    Removing tag", tag, "from active list"
            del active_tags[tag]
            
        #add to retired
        newly_retired_count += 1
        retired_tags[tag] = t
        if DEBUG:
          print "    Retiring tag", tag, "with LGOR", LGOR(t)

    # Active
    else:
      #coming out of retirement
      #remove from retired
      if tag in retired_tags:
        reactivated_count += 1
        print "  Account", tag, "coming out of retirement!"
        print "    LGOR was", LGOR(retired_tags[tag])
        del retired_tags[tag]

      #already active
      if tag in active_tags:
        if DEBUG:
          print "  Account", tag, "is already active. Doing nothing."
        continue
      #or add to active
      else:
        #active_tags[tag] = all_tags[tag]
        active_tags[tag] = t
        if DEBUG:
          print "    Account active with LGOR", LGOR(t)

  if DEBUG:
    print "\n  Retired accounts:", retired_tags
    print "\n  Active accounts :", active_tags
    print "\n  Seed accounts   :", seed_tags

  print "\n  Number of retired accounts", len(retired_tags)
  print "  Number of active accounts", len(active_tags)
  print "  Number of seed accounts", len(seed_tags)

  print "\n  Number of newly retired accounts", newly_retired_count
  print "  Number of reactivated accounts", reactivated_count

  print "\n  Saving..."
  #Utils.back_up(active_tags_file)
  #Utils.back_up(retired_tags_file)
  #Utils.update_file(active_tags_file,  active_tags_container,  active_tags,  'd')
  #Utils.update_file(retired_tags_file, retired_tags_container, retired_tags, 'd')
  Utils.overwrite_file(active_tags_file, active_tags_container, active_tags)
  Utils.overwrite_file(retired_tags_file, retired_tags_container, retired_tags)
  Utils.overwrite_file(seed_tags_file, seed_tags_container, seed_tags)

  print "  Done."

  print "Exiting UpdateActiveTags()"

def LGOR(d):
  g = d['most_recent_game_time']
  return datetime.datetime.strptime(g,'%Y-%m-%d %H:%M')

if __name__ == "__main__":
  UpdateActiveTags() 
