from Player import Player

class Game():
    _date_time = -1
    _stage      = ""
    _type     = -1
    _duration = -1
    
    def __init__(self):
        self._p1 = Player(1)
        self._p2 = Player(2)

    def print_player(self, p_num):
        if (p_num == 1):
            #print("p1:",  vars(self._p1))
            print("p1:")
            for k, v in vars(self._p1).items():
                print (k, '-->', v)
        elif (p_num == 2):
            #print("p2:",  vars(self._p2))
            print("p2:")
            for k, v in vars(self._p2).items():
                print (k, '-->', v)
        else:
            print("Invalid player:", p_num)

    def print_game(self):
        for k, v in vars(self).items():
                print (k, '-->', v)
