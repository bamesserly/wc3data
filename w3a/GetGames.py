import time
import Utils
from GetNewTagsAndGames import LoopTags

#input
input_file = "data/active_tags_info.py"
container  = "active_tags"               # Can be list or dict of tags
tags_are_active = True                   # Begin with confirmed active tags

# Build:  ignore any existing tag info and get ALL games
# Update: refer to existing tag info to only get new games.
update = True
build = not update

def main():
  # Input tags
  tags = Utils.load_data(input_file, container)
  tags = set(tags) #remove dupes
  master_tags_set = tags

  # Output games
  output_games = []

  # Recursive search
  new_tags = tags    # Keep searching until no new_tags found

  iterations = 0
  t0 = time.time()
  t  = time.time()
  print "Beginning iterative search for new games. Using", len(new_tags), "seed tags."
  print "Current time", time.time()

  while(new_tags):
    iterations += 1
    t = time.time()

    # Loop tags: retrieve games, opponents
    new_games, new_tags = LoopTags(new_tags, tags_are_active, update)
    tags_are_active = False

    # Manage new tags
    new_tags = new_tags.difference(master_tags_set) # only newest tags for next loop
    master_tags_set.update(new_tags)                # add them to the master

    # Manage new games
    output_games.extend(new_games)
    output_games = Utils.remove_duplicates(output_games)  
                                                    # will be many dupes so
                                                    # remove for each iteration 

    Utils.print_status(iterations, t0, t, len(new_tags))

  print "Current time", time.time()
  print "All done iteratively looping tags."

  ##################################################
  # Finalize: Save games to their respective files #
  ##################################################
  output_games = Utils.remove_duplicates(output_games)    # doesn't hurt?
  games2015 = []
  games2016 = []
  games2017 = []
  for g in output_games:
    gtime = datetime.datetime.strptime(g['date_time'], "%d-%m-%Y %H:%M")
    year = gtime.year
    if   year <= 2015:
      games2015.append(g)
    elif year == 2016:
      games2016.append(g)
    elif year == 2017:
      games2017.append(g)
    else:
      print "Time to create a 2018 games list!"

  '''
  Utils.save_games(games2015, "data/games2015.py", "games")
  Utils.save_games(games2016, "data/games2016.py", "games")
  Utils.save_games(games2017, "data/games2017.py", "games")
  '''
if __name__ == "__main__":
  main()
