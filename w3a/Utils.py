import time
import os
from importlib import import_module
from shutil import copy
top                     = "/Users/Ben/Home/wc3data/w3a/"

###########################################################################
# Load data -- Get an object from a file, e.g. tags = [...]               #
#              A la "from file import object" syntax                      #
#              @TODO this behaves badly with the way backup works. If     #
#              data file itself isn't present, uses first backup. Bad!    #
#              This has been causing major bugs.                          #
###########################################################################
def load_data(input_file, container):
  module_name = input_file.replace("/", ".") #data/list.py --> data.list.py
  module_name = module_name[:-3]             #data.list.py --> data.list
  module = import_module( module_name )
  ret_obj = getattr(module, container)
  return ret_obj

#############################################################
# Update File -- Updates the object in a data file          #
#                Accepts only lists, sets and dicts         #
#                MERGES containers                          #
#############################################################
def update_file(data_file, obj_name, new_obj, container_type):
  if not new_obj:
    print "      No", obj_name, "to save for", data_file
    return

  old_obj = load_data(data_file, obj_name)
  old_size = len(old_obj)

  if container_type is "l":
    new_obj = set(new_obj)
    old_obj = set(old_obj) 

    updated_obj = old_obj
    updated_obj.update(new_obj)

  elif container_type is "d":
    updated_obj = old_obj
    updated_obj.update(new_obj)

  elif container_type is "l_d":
    updated_obj = old_obj + new_obj
    updated_obj = remove_duplicates(updated_obj)

  else:
    print "ERROR, wrong container type"

  updated_size = len(updated_obj)

  print "\nupdate_file()      old size = ", old_size
  print "\nupdate_file()      new size = ", updated_size
  print "\nupdate_file()      old - new size of", obj_name, "=", updated_size-old_size

  # Save the new comprehensive game list
  updated_file = open(top + data_file, 'w+')
  updated_file.write(obj_name + " = " + str(updated_obj))
  updated_file.close()

#############################################################
# Overwrite File -- Overwrite the object in a data file     #
#                   OVERWRITE containers                    #
#############################################################
def overwrite_file(data_file, obj_name, obj):
  f = open(top + data_file, 'w')
  f.write(obj_name + " = " + str(obj))
  f.close()
  return

#############################################################
# Remove Duplicates -- Specifically for lists of dicts      #
#                      Can't use a set (see "hashable")     #
#############################################################
def remove_duplicates(list_of_dicts):
  return [dict(t) for t in set([tuple(d.items()) for d in list_of_dicts])]

#############################################################
# Back up -- Takes a file and makes a copy with an integer  #
#            on the end e.g. test.py --> test.py + test.py0 #
#############################################################
def back_up(path):
  path = top + path
  i = 0
  while (i<100):
    if not os.path.exists(path + '{0}'.format(i)):
      new_backup = path + '{0}'.format(i)
      copy(path, new_backup)
      break
    i += 1
