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
  seed_tags    = {} #write this fresh every time
  active_tags  = {}
  retired_tags = {}

  retirement_time = (datetime.datetime.today() + 
                                 relativedelta(months=-retirement_cutoff_months))
  seed_time = (datetime.datetime.today() + relativedelta(days=-seed_cutoff_days))

  print "  Retirement cutoff is", retirement_cutoff_months, "months prior to today:", retirement_time
  print "  Force retirement is", force_retirement
  print "  Seed accounts have played a game in the last", seed_cutoff_days, "days:", seed_time

  print "  Number of tags total:", len(all_tags),"\n"
  for tag in all_tags:
    t = all_tags[tag]
    
    # Seed
    if LGOR(t) > seed_time :
      seed_tags[tag] = t

    # Retire
    if LGOR(t) < retirement_time or t['ngames'] < 10:
      if DEBUG:
        print "    Retiring tag", tag, "with LGOR", LGOR(t)

      retired_tags[tag] = t

    # Active
    else:
      if DEBUG:
        print "    Account active with LGOR", LGOR(t)
      active_tags[tag] = t

  if DEBUG:
    print "\n  Retired accounts:", retired_tags
    print "\n  Active accounts :", active_tags
    print "\n  Seed accounts   :", seed_tags

  print "\n  Number of retired accounts", len(retired_tags)
  print "  Number of active accounts", len(active_tags)
  print "  Number of seed accounts", len(seed_tags)

  print "\n  Saving..."
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
