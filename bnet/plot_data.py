import matplotlib.pyplot as plt
from numpy.random import rand
import numpy as np
from scipy import stats
from list_of_players_bnet1_Elo import list_of_players_bnet1_Elo

def main():
  data_list = []

  #make a new list from the old one with each entry in the form
  #[ELO, WR, ngames]
  for x in range (0, len(list_of_players_bnet1_Elo) ):
    data_point = []
    data_point.append(list_of_players_bnet1_Elo[x][1][0])
    data_point.append(float(list_of_players_bnet1_Elo[x][1][4]))
    data_point.append(list_of_players_bnet1_Elo[x][1][1])
    data_list.append(data_point)

  #print(data_list)
  print("number of accounts scored = " + str(len(data_list)) )

  plt.legend()

  (x,y) = make_Elo_WR_lists(data_list, 0, 19)
  make_scatter_plot(x,y,'r','1-19 games, n= ' +str(len(x)))

  (x,y) = make_Elo_WR_lists(data_list, 20, 49)
  make_scatter_plot(x,y,'b','20-49 games, n= ' +str(len(x)))

  (x,y) = make_Elo_WR_lists(data_list, 50, 149)
  make_scatter_plot(x,y,'y','50-149 games, n= ' +str(len(x)))

  (x,y) = make_Elo_WR_lists(data_list, 150, 499)
  make_scatter_plot(x,y,'k','150-499 games, n= ' +str(len(x)))

  (x,y) = make_Elo_WR_lists(data_list, 500, 100000)
  make_scatter_plot(x,y,'c','500+ games, n= ' +str(len(x)))


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

def make_Elo_WR_lists(data_list, min_games_played, max_games_played):
  x = []
  y = []

  for z in range (0, len(data_list)):
  #for z in range (0, n_data_points):
    if data_list[z][2] >= min_games_played and data_list[z][2] < max_games_played:
      x.append(data_list[z][0])
      y.append(data_list[z][1])
    else:
      pass

  return (x,y)

def make_scatter_plot(x, y, color='r', legend_label='', scale=1.0):
  x = np.array(x)
  y = np.array(y)

  #color = 'r'
  #scale = 1.0

  #plt.legend()
  plt.scatter(x,y, s=scale, c=color, marker = ",", lw=0, alpha = 0.5, label = legend_label + ", n= " +str(len(x)))

  # m, b = np.polyfit(x, y, 1)

  slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
  # plt.legend(('data', 'line-regression r={}'.format(r_value)), 'best')
  plt.plot(x, slope*x +intercept, '-', c = color, label = r_value)

if __name__ == "__main__":
  main()
