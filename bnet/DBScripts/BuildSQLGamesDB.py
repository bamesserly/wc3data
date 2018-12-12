import os, sys
sys.path.append("../")
from datetime import datetime
from Player import Player
from Game import Game
from ParseFunctions import *
from Enums import kGameTypes
from DBFunctions import *
import game_rec_info as line_consts
import sqlite3

game_total = 0
game_good = 0
n_short_file = 0
n_zero_min = 0
n_hero_lvl = 0
n_short_file2 = 0

# Generator of input files
def FileGenerator(directory_in_str):
    for entry in os.scandir(directory_in_str):
        # if not entry.name.startswith('.') and not entry.is_dir() and entry.name.startswith("game332015367") and entry.name.endswith(".txt"):
        # if not entry.name.startswith('.') and not entry.is_dir() and entry.name.startswith("game3320153") and entry.name.endswith(".txt"):
        if (
            not entry.name.startswith(".")
            and not entry.is_dir()
            and entry.name.endswith(".txt")
        ):
            yield entry.name


def ParseFile(fp):
    global n_short_file
    global n_zero_min
    global game_good
    g = Game()

    lines = fp.readlines()

    g._duration = parse_duration(lines[line_consts.duration].strip())
    if g._duration == 0:
        n_zero_min += 1
        return

    # Usually (always) means 0 or 1 heroes, and/or 0-minute length
    # TODO we can salvage these games
    if len(lines) < 36:
        n_short_file += 1
        return

    g._date_time = parse_date_time(lines[line_consts.date_time].strip())
    g._stage = parse_stage(lines[line_consts.stage].strip())
    g._type = parse_gametype(lines[line_consts.gametype].strip())

    if g._type is not kGameTypes.kSOLO.value:
        return

    sc = ParsePlayer(g._p1, lines)

    sc = sc and ParsePlayer(g._p2, lines)

    if not sc:
        return
    else:
        game_good += 1
        #g.print_player(2)
        #g.print_game()
        return g


def ParsePlayer(p, lines):
    global n_zero_min
    global n_hero_lvl
    global n_short_file2
    p._name = parse_p_name(lines[p._l_name_race].strip())
    p._race = parse_p_race(lines[p._l_name_race].strip())
    p._lvl = parse_p_lvl(lines[p._l_lvl].strip())
    p._exp = parse_p_exp(lines[p._l_outcome].strip())
    p._win = parse_p_win(lines[p._l_outcome].strip())
    p._dexp = parse_p_dexp(lines[p._l_outcome].strip())
    p._scores = parse_p_scores(lines[p._l_scores].strip())
    p._unit_score = parse_p_unit_score(lines[p._l_unit_score].strip())

    try:
        p._hero_score = parse_p_hero_score(lines[p._l_hero_score].strip())
    except (ValueError, IndexError) as e:
        n_hero_lvl += 1
        return False

    try:
        heroes = parse_p_heroes(lines[p._l_heroes].strip())
    except IndexError:
        n_hero_lvl += 1
        return False

    try:
        (p._h1_name, p._h1_lvl) = heroes[0]
    except IndexError:
        pass
    try:
        (p._h2_name, p._h2_lvl) = heroes[1]
    except IndexError:
        pass
    try:
        (p._h3_name, p._h3_lvl) = heroes[2]
    except IndexError:
        pass

    # some games have fewer lines.
    try:
        p._resource_score = parse_p_resource_score(lines[p._l_resource_score].strip())
    except IndexError:
        n_short_file2 += 1
        return False

    return True


# MAIN
def main():
    global game_total

    connection = sqlite3.connect("bnetGames.db")
    c = connection.cursor()
    c = InitDB(c)  # do we need to return c?

    directory_in_str = "/Users/Ben/Home/wc3data/bnet/originalProject/processedFiles/Solo/"
    #directory_in_str = "/Users/Ben/Home/wc3data/bnet/DBScripts/test_games/"
    files_generator = FileGenerator(directory_in_str)
    for f in files_generator:
        game_total += 1
        fullpath = directory_in_str + f
        print(fullpath)
        with open(fullpath) as fp:
            game_rec = ParseFile(fp)
            if game_rec:
                try:
                    InsertGame(game_rec, connection, c)
                except sqlite3.IntegrityError:
                    print("SQL problem inserting game") #we may have just already inserted the game
                                                        #not necessarily a problem
            else:
                continue

    connection.commit()

    c.close()
    connection.close()

    print("short game files:", n_short_file)
    print("zero min duration:", n_zero_min)
    print("missing hero level:", n_hero_lvl)
    print("missing a few lines:", n_short_file2)
    print("good:", game_good)
    print("total:", game_total)

if __name__ == "__main__":
    main()
