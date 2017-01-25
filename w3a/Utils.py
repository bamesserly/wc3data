import time
from importlib import import_module

# Get an object from a file, e.g. tags = [...]
# A la "from file import object" syntax
def load_data(input_file, container):
  module_name = input_file.replace("/", ".") #data/list.py --> data.list.py
  module_name = module_name[:-3]             #data.list.py --> data.list
  module = import_module( module_name )
  ret_obj = list(getattr(module, container))
  return ret_obj

def save_games(new_games, data_file, object_name):
  if not new_games:
    print "      No games for", data_file, "during this iteration."
    return

  old_games = load_data(data_file, object_name)

  # Add the new tags to the master tag list 
  all_games = old_games + new_games

  all_games = remove_duplicates(all_games)

  # Back up the old game list
  back_up(data_file)

  # Save the new comprehensive game list
  updated_games_file = open(data_file, 'w+')
  updated_games_file.write("games = " + str(list_of_games))
  updated_games_file.close()

# Remove dupes (list if dicts so have to be fancy, can't use a set)
def remove_duplicates(list_of_dicts):
  return [dict(t) for t in set([tuple(d.items()) for d in list_of_dicts])]

def back_up(path):
  i = 0
  while (i<100):
    if not os.path.exists(path + '{0}'.format(i)):
      new_backup = path + '{0}'.format(i)
      #print 'Number of player list backups = ', i
      #shutil.copy(path, new_backup)
      copy(path, new_backup)
      break
    i += 1

def print_status(iterations, t0, t, n_tags):
    print "  Finished iteration", iterations, "of building/updating game database"
    print "    Time elapsed in this iteration:", time.time() - t
    print "    Total time elapsed:            ", time.time() - t0
    print "   ", n_tags, "new tags found in this iteration."
