from data.temp_list import existing_players
old_set = set(existing_players)
print "old list len ", len(existing_players)

existing_players = []
print "clearing temp list. len existing_players = ", len(existing_players)

from data.list_of_existing_players_short import existing_players
current_set = set(existing_players)
print "current list len ", len(existing_players)

return_tags = current_set.difference( old_set )
print "return set len ", len(return_tags)

"""
newest_tags_file = open('data/newest_tags.py', 'w+')
newest_tags_file.write("newest_players = " + str(return_tags))
newest_tags_file.close()
"""
