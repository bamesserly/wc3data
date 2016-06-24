import matplotlib.pyplot as plt
from numpy.random import rand
import numpy as np
from scipy import stats
from list_of_players_bnet1_Elo import list_of_players_bnet1_Elo

#make a new list from the old one with each entry in the form
#[ELO, WR, ngames]
data_list = []

for x in range (0, len(list_of_players_bnet1_Elo) ):
    data_point = []
    data_point.append(list_of_players_bnet1_Elo[x][1][0])
    data_point.append(float(list_of_players_bnet1_Elo[x][1][4]))
    data_point.append(list_of_players_bnet1_Elo[x][1][1])
    data_list.append(data_point)

print(data_list)
print(len(data_list))

#####################################################################################
# make lists of ELO (x) and WR (y), plot them
# accounts with fewer than 20 games
x = []
y = []

#for z in range (0, len(data_list)):
for z in range (0, 5):
    if data_list[z][2] >= 0 and data_list[z][2] < 20:
        x.append(data_list[z][0])
        y.append(data_list[z][1])
    else:
        pass

x = np.array(x)
y = np.array(y)

color = 'r'
scale = 1.0

plt.legend()
plt.scatter(x,y, s=scale, c=color, marker = ",", lw=0, alpha = 0.5, label = '1-19 games' + ", n= " +str(len(x)))

# m, b = np.polyfit(x, y, 1)

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
plt.plot(x, slope*x +intercept, '-', c = color, label = r_value)
# plt.legend(('data', 'line-regression r={}'.format(r_value)), 'best')

#############################################################################
# make lists of ELO (x) and WR (y), plot them
# accounts with 20-49 games

x = []
y = []

for z in range (0, len(data_list)):
    if data_list[z][2] >= 20 and data_list[z][2] < 50:
        x.append(data_list[z][0])
        y.append(data_list[z][1])
    else:
        pass

x = np.array(x)
y = np.array(y)

color = 'y'
scale = 1.0


plt.scatter(x,y, s=scale, c=color, marker = ",", lw=0, alpha = 1.0, label = '20-49 games' + ", n= " +str(len(x)))

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
plt.plot(x, slope*x +intercept, '-', c = color, label = r_value)
# plt.legend(('data', 'line-regression r={}'.format(r_value)), 'best')

#########################################################################
# make lists of ELO (x) and WR (y), plot them
# accounts with 50-149 games

x = []
y = []

for z in range (0, len(data_list)):
    if data_list[z][2] >= 50 and data_list[z][2] < 150:
        x.append(data_list[z][0])
        y.append(data_list[z][1])
    else:
        pass

x = np.array(x)
y = np.array(y)

color = 'c'
scale = 1.0



plt.scatter(x,y, s=scale, c=color, marker = ",", lw=0, alpha = 1.0, label = '50-149 games' + ", n= " +str(len(x)))

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
plt.plot(x, slope*x +intercept, '-', c = color, label = r_value)

##########################################################################
# make lists of ELO (x) and WR (y), plot them
# accounts with 150-500 games


x = []
y = []

for z in range (0, len(data_list)):
    if data_list[z][2] >= 150 and data_list[z][2] < 500:
        x.append(data_list[z][0])
        y.append(data_list[z][1])
    else:
        pass

x = np.array(x)
y = np.array(y)

color = 'b'
scale = 1.0



plt.scatter(x,y, s=scale, c=color, marker = ",", lw=0, alpha = 0.5, label = '150-499 games' + ", n= " +str(len(x)))

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
plt.plot(x, slope*x +intercept, '-', c = color, label = r_value)

##########################################################################
# make lists of ELO (x) and WR (y), plot them
# accounts with 500 or more games

x = []
y = []

for z in range (0, len(data_list)):
    if data_list[z][2] >= 500:
        x.append(data_list[z][0])
        y.append(data_list[z][1])
    else:
        pass

x = np.array(x)
y = np.array(y)

color = 'k'
scale = 1.0


plt.scatter(x,y, s=scale, c=color, marker = ",", lw=0, label = '500+ games' + ", n= " +str(len(x)))

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
plt.plot(x, slope*x +intercept, '-', c = color, label = r_value)

###############################################


plt.xlabel('Elo (skill rating)')
plt.ylabel('Win%')
plt.title("Elo vs Win%")

# slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

# plt.legend()
leg = plt.legend(loc = 2, ncol = 2, prop = {'size':11}, markerscale = 2.5, fancybox = True)
leg.get_frame().set_alpha(10.0)
# ('data', 'line-regression r={}'.format(r_value)), 'best')

plt.grid(True)
plt.show()

#TODO determine r values, re-order the items in the legend, clean up axes lables and size
