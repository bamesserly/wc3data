import time
#import GetListOfGames
import GetNewTagsAndGames

def main():
  from data.list_of_existing_players import existing_players
  tags_set_master = Set([existing_players)]

  tags_total = len(tags_set_master)
  print "Starting with ", tags_total, "players..."
  iterations = 0

  # Starting values for our while loop
  current_tags = Set([ existing_players ])
  still_finding_new_players = true     # condition to keep looping
  t0 = time.time()
  t = time.time()

  print "Beginning iterative search for new players/games"
  while(still_finding_new_tags):
    PrintStatus(iterations, t0, t)
    t = time.time()
    iterations++

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
      tags_set_master = tags_set_master.union(new_tags)
      # Make the new_tags into the current tags and loop again
      current_tags = new_tags

    # Or if we didn't find any new tags then we're done!
    else:
      print "Done finding new tags"
      still_finding_new_tags = false

  PrintStatus(iterations, t0, t)

def PrintStatus(iterations, t0, t):
    print "  Iteration # ", iterations, " of building player/game database."
    print "    Time elapsed in last iteration: ", time.time() - t, "."
    print "    Total time elapsed: ", time.time() - t0, "."

if __name__ == "__main__":
  main()
