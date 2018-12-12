import GameRecordLineNumberConstants as line_consts

class Player(object):
    def __init__(self, p_num):
        self._num            = p_num
        self._name           = -1
        self._race           = -1
        self._lvl            = -1
        self._exp            = -1
        self._win            = -1
        self._dexp           = -1
        self._scores         = {}
        self._unit_score     = {}
        self._hero_score     = {}
        self._resource_score = {}
        self._h1_name        = -1
        self._h1_lvl         = -1
        self._h2_name        = -1
        self._h2_lvl         = -1
        self._h3_name        = -1
        self._h3_lvl         = -1

        # Line numbers in the game record
        if self._num == 1:
            self._l_name_race      = line_consts.p1_name_race
            self._l_lvl            = line_consts.p1_lvl
            self._l_outcome        = line_consts.p1_outcome
            self._l_scores         = line_consts.p1_scores
            self._l_unit_score     = line_consts.p1_unit_score
            self._l_resource_score = line_consts.p1_resource_score
            self._l_hero_score     = line_consts.p1_hero_score
            self._l_heroes         = line_consts.p1_heroes
        elif self._num == 2:
            self._l_name_race      = line_consts.p2_name_race
            self._l_lvl            = line_consts.p2_lvl
            self._l_outcome        = line_consts.p2_outcome
            self._l_scores         = line_consts.p2_scores
            self._l_unit_score     = line_consts.p2_unit_score
            self._l_resource_score = line_consts.p2_resource_score
            self._l_hero_score     = line_consts.p2_hero_score
            self._l_heroes         = line_consts.p2_heroes
