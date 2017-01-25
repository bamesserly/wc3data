import time
from GetNewTagsAndGames import GetNewTagsAndGames

def main():
  from data.list_of_existing_players import existing_players
  tags_set_master = set(existing_players)
  from data.newest_tags import newest_players

  tags_total = len(tags_set_master)
  print "Master list has ", tags_total, "tags..."
  iterations = 0

  # Starting values for our while loop
  #current_tags = set( existing_players )
  current_tags = set( newest_players )
  n_tags_first_iteration = len(current_tags)
  print "Of those", tags_total, ",", n_tags_first_iteration, "are new."
  print "Looping over", n_tags_first_iteration, "."

  still_finding_new_tags = True     # condition to keep looping
  t0 = time.time()
  t = time.time()
  new_tags = set([])

  print "Beginning iterative search for new players/games"
  print "Current time", time.time()
  while(still_finding_new_tags):
    PrintStatus(iterations, t0, t, len(current_tags))
    t = time.time()

    # Get new_tags from current_tags by looping through the games of each
    # current_tag and adding opponent to a set.
    # 
    # This step should take a long time because it takes a long time to
    # access each players' game history.
    # 
    # In the loop over current_tags, GetNewTagsAndGames will also 
    # append each new game it encounters to game data files
    new_tags = GetNewTagsAndGames( current_tags )

    if new_tags:
      # Add the new tags to the master tag list
      #tags_set_master = tags_set_master.union(new_tags) #this actually isn't used. We save in GetNewTagsAndGames.
      # Make the new_tags into the current tags and loop again
      current_tags = new_tags
      iterations = iterations + 1
      #if iterations  >= 3:
      #  print "Stopping search for tags at iteration", iterations
      #  still_finding_new_tags = False

    # Or if we didn't find any new tags then we're done!
    else:
      print "Done finding new tags"
      still_finding_new_tags = False


  PrintStatus(iterations, t0, t, len(current_tags))
  print "Current time", time.time()
  print "...I guess we're all done. Nice."

def PrintStatus(iterations, t0, t, n_tags):
    print "  Iteration # ", iterations, " of building player/game database."
    print "    Time elapsed in last iteration: ", time.time() - t, "."
    print "    Total time elapsed: ", time.time() - t0, "."
    print "    Found", n_tags, "new tags in last iteration."

if __name__ == "__main__":
  main()
