

from data.games2015 import games
recent = games
print len(recent),"games imported from 2015."

from data.games2016 import games
recent = games
print len(recent),"games imported from 2016."

from data.games2017 import games
recent = games
print len(recent),"games imported from 2017."

'''
from data.games2017_11 import games
eleven = games
print len(eleven),"games imported from 11."

from data.games2017_10 import games
ten = games
print len(ten),"games imported from 10."

from data.games2017_9 import games
nine = games
print len(nine),"games imported from 9."

from data.games2017_8 import games
eight = games
print len(eight),"games imported from 8."

from data.games2017_7 import games
seven = games
print len(seven),"games imported from 7."

from data.games2017_6 import games
six = games
print len(six),"games imported from 6."

from data.games2017_5 import games
five = games
print len(five),"games imported from 5."

from data.games2017_4 import games
four = games
print len(four),"games imported from 4."

from data.games2017_3 import games
three = games
print len(three),"games imported from 3."

from data.games2017_2 import games
two = games
print len(two),"games imported from 2."

from data.games2017_1 import games
one = games
print len(one),"games imported from 1."

from data.games2017_0 import games
zero = games
print len(zero),"games imported from 0."

merged_list = zero + one
print "merged list 0,1", len(merged_list)

merged_set = [dict(t) for t in set([tuple(d.items()) for d in merged_list])]
print "merged set 0,1", len(merged_set)

merged_set = merged_set + two + three + four
print "merged list 0,1,2,3,4", len(merged_set)

merged_set = [dict(t) for t in set([tuple(d.items()) for d in merged_list])]
print "merged set 0,1,2,3,4", len(merged_set)

merged_set = merged_set + seven + eight
print "merged list 1,2,3,4,5,6,7,8", len(merged_set)

merged_set = [dict(t) for t in set([tuple(d.items()) for d in merged_set])]
print "merged set 1,2,3,4,5,6,7,8", len(merged_set)

merged_set = merged_set + nine
print "merged list 1,2,3,4,5,6,7,8,9", len(merged_set)

merged_set = [dict(t) for t in set([tuple(d.items()) for d in merged_set])]
print "merged set 1,2,3,4,5,6,7,8,9", len(merged_set)

merged_set = merged_set + eleven
print "merged list 1,2,3,4,5,6,7,8,9,10,11", len(merged_set)

merged_set = [dict(t) for t in set([tuple(d.items()) for d in merged_set])]
print "merged set 1,2,3,4,5,6,7,8,9,10,11", len(merged_set)

return_file = open('data/games2017.py', 'w+')
return_file.write("games = " + str(merged_set))
return_file.close()
'''
