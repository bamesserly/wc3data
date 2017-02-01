import time
import Utils
from LoopTags import LoopTags
from Constants import update, build, DEBUG

#from Constants import active_tags_file, active_tags_container #input
from Constants import seed_tags_file,    seed_tags_container  #input
from Constants import all_games_file,    all_games_container  #output

def GetGames():
  print "Entering GetGames()" 
    
  ##################################################################
  # INPUT: seed_tags are seed from which we search for new games   #
  ##################################################################
  tags = Utils.load_data(seed_tags_file, seed_tags_container)

  if DEBUG:
    tags = list(tags)
    del tags[5:]

  tags = set(tags) #remove dupes
  
  ##################################################################
  # Master tag list: as we collect tags, check them against this
  # list, keeping only the new ones as seeds for the next iteration
  ##################################################################
  # master list
  master_tags_set = tags
  #all_tags = Utils.load_data(all_tags_file, all_tags_container)

  ##################################################################
  # OUTPUT: new games, a list of dicts
  ##################################################################
  output_games = []

  ##################################################################
  # Recursive loop to find new games
  ##################################################################

  new_tags = tags
  iterations = 0
  t0 = t = time.time()
  print "  Beginning iterative search for new games. Using", len(new_tags), "seed tags."
  print "  Current time", time.time()
  new_games = True

  while(new_tags and new_games):
    iterations += 1
    t = time.time()

    # Loop tags: retrieve games, opponents
    new_games, new_tags = LoopTags(new_tags, build)

    # Manage new tags
    new_tags = new_tags.difference(master_tags_set) # only newest tags for next loop
    master_tags_set.update(new_tags)                # add them to the master

    # Manage new games
    output_games.extend(new_games)
    output_games = Utils.remove_duplicates(output_games)
                                                    # will be many dupes so
                                                    # remove for each iteration 

    print_status(iterations, t0, t, len(new_tags))
    
    if DEBUG:
      break

  print "  Current time", time.time()
  print "  All done iteratively looping tags."

  # if we're updating, save now. If building, we already saved in the loop
  #if update:
  #  output_games = Utils.remove_duplicates(output_games)
  #  Utils.update_file(all_games_file, all_games_container, output_games, 'l_d')

  print "Exiting GetGames()"

def print_status(iterations, t0, t, n_tags):
    print "  Finished iteration", iterations, "of building/updating game database"
    print "    Time elapsed in this iteration:", time.time() - t
    print "    Total time elapsed:            ", time.time() - t0
    print "   ", n_tags, "new tags found in this iteration."

if __name__ == "__main__":
  GetGames()
