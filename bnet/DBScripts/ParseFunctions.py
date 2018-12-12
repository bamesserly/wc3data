from Enums import kHeroes, kStages, kRaces, kGameTypes
import string  # whitespace independent str compare
import re
from dateutil.parser import parse
import datetime
import pytz

Races = ["Orc", "Human", "Night Elf", "Undead"]
GameTypes = ["Solo", "FFA", "Tournament"]
kScores = ["Unit", "Heroes", "Resource", "Total"]
kUnitScores = [
    "UnitsProduced",
    "UnitsKilled",
    "BuildingsProduced",
    "BuildingsRazed",
    "LargestArmy",
]
kHeroScores = [
    "HeroesUsed",
    "HeroesKilled",
    "ItemsObtained",
    "MercenariesHired",
    "ExperienceGained",
]
kResourceScores = [
    "GoldMined",
    "LumberHarvested",
    "ResourcesTraded",
    "TechPercentage",
    "GoldLosttoUpkeep",
]

################################################################################
# Helper Functions
################################################################################

# Remove whitespace compare
# "demonhunter" is in  "FOO demon hunter BAR"
def compare(s1, s2):
    remove = string.whitespace  # + string.punctuation
    ttable = str.maketrans(dict.fromkeys(remove))  # make a translation "table"
    return s1.translate(ttable) in s2.translate(ttable)
    # return s1.translate(ttable) == s2.translate(ttable)


def string_to_int(s):
    return int(s.replace(",", ""))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_hero_from_string(hero_str):
    hero = ""
    for name, member in kHeroes.__members__.items():  # loop our hero enum, h
        if compare(name, hero_str):  # if h is in this str
            hero = member.value  # add it to list
    return hero


def get_race_from_string(race_str):
    if race_str == "NightElf":
        return kRaces.kNIGHTELF.value
    elif race_str == "Human":
        return kRaces.kHUMAN.value
    elif race_str == "Orc":
        return kRaces.kORC.value
    elif race_str == "Undead":
        return kRaces.kUNDEAD.value
    if race_str == "Random_NightElf":
        return kRaces.kRANDOM_N.value
    elif race_str == "Random_Human":
        return kRaces.kRANDOM_H.value
    elif race_str == "Random_Orc":
        return kRaces.kRANDOM_O.value
    elif race_str == "Random_Undead":
        return kRaces.kRANDOM_U.value
    else:
        print("Unkown Race")
        raise Exception

def get_gametype_from_string(type_str):
    if type_str == "Solo":
        return kGameTypes.kSOLO.value
    elif type_str == "FFA":
        return kGameTypes.kFFA.value
    elif type_str == "Tournament":
        return kGameTypes.kTOURNAMENT.value
    else:
        print("Unkown Game Type")
        raise Exception

################################################################################
# Parse Line Functions
################################################################################

# TODO this would be better with pyparse
# [TEXT] -- [NUM] -- [TEXT] -- [NUM] -- [TEXT] -- [NUM]
# This way, we could easily catch the POTM/KOTG problem
def parse_p_heroes(line):
    heroes = []
    line = line.upper()
    line_split = re.split("(\D+)", line)  # separate heroes from their levels
    line_split = list(filter(None, line_split))  # remove '' strings
    line_split = [i.strip(" ") for i in line_split]  # remove whitespace paddings
    for i in range(0, len(line_split), 2):
        hero = get_hero_from_string(line_split[i])
        lvl = int(line_split[i + 1])
        heroes.append((hero, lvl))
    return heroes


def parse_p_name(line):
    return line.split()[0]


# bugged races
def parse_p_race(line):
    line = line.split(" ", 1)[-1]  # remove the player name
    random = "Random" in line  # random?
    try:
        race = [r for r in Races if r in line][0]  # ultimate race
    except IndexError:
        return "BUGGED"
    if random:
        race = "Random_" + race
    race = race.replace(" ", "")  # remove white space (for N E)
    return get_race_from_string(race)


# TODO add other gametypes
def parse_gametype(line):
    gt = [t for t in GameTypes if t in line][0]
    return get_gametype_from_string(gt)


def parse_p_lvl(line):
    return int(line)


# TODO pyparse, rather than split
def parse_duration(line):
    return string_to_int(line.split()[2])


def parse_date_time(line):
    line = line.split(":", 1)  # everything after first colon
    line = "".join(line[1:])  # make it a string
    line = line.strip()  # remove leading whitespace
    hrs = 3600
    tzinfos = {
        "EST": -5 * hrs,
        "EDT": -4 * hrs,
        "WEDT": +1 * hrs,
        "WET": +0 * hrs,
        "KST": +9 * hrs,
        "PST": -8 * hrs,
        "PDT": -7 * hrs,
    }
    date_time = parse(line, tzinfos=tzinfos)
    date_time = date_time.astimezone(pytz.utc).isoformat()
    return str(date_time)


# TODO pyparse, everything after colon
def parse_stage(line):
    line = "".join(line.split()[1:]).upper()
    for name, member in kStages.__members__.items():
        if name == line:
            return member.value


def parse_p_exp(line):
    exp = line.split()[0]
    exp = string_to_int(exp)
    return exp


def parse_p_win(line):
    win = line.split()[1].upper()
    if win == "WIN":
        return 1
    elif win == "LOSS":
        return 0
    else:
        return -1


def parse_p_dexp(line):
    dexp = line.split()[2]
    dexp = string_to_int(dexp)
    return dexp


def parse_p_scores(line):
    scores = line.split()
    scores_dict = {}
    scores_dict.fromkeys(kScores)
    scores_dict["Unit"]     = string_to_int(scores[-4])
    scores_dict["Heroes"]   = string_to_int(scores[-3])
    scores_dict["Resource"] = string_to_int(scores[-2])
    scores_dict["Total"]    = string_to_int(scores[-1])
    return scores_dict


def parse_p_unit_score(line):
    units = line.split()
    units_dict = {}
    units_dict.fromkeys(kUnitScores)
    # TODO reverse loop... for i in range(-1, -len(kUnit),  -1):
    # for i in range(-1, len(kUnit)):
    units_dict["UnitsProduced"]     = string_to_int(units[-5])
    units_dict["UnitsKilled"]       = string_to_int(units[-4])
    units_dict["BuildingsProduced"] = string_to_int(units[-3])
    units_dict["BuildingsRazed"]    = string_to_int(units[-2])
    units_dict["LargestArmy"]       = string_to_int(units[-1])
    return units_dict


def parse_p_resource_score(line):
    resources = line.split()
    resources_dict = {}
    resources_dict.fromkeys(kResourceScores)
    # S.isalnum()
    # TODO reverse loop... for i in range(-1, -len(kUnit),  -1):
    # for i in range(-1, len(kUnit)):
    resources_dict["GoldMined"]        = string_to_int(resources[-8])
    resources_dict["LumberHarvested"]  = string_to_int(resources[-7])
    resources_dict["ResourcesTraded"]  = (
        string_to_int(resources[-6]),
        string_to_int(resources[-4]),
    )
    resources_dict["TechPercentage"]   = string_to_int(resources[-3])
    resources_dict["GoldLosttoUpkeep"] = string_to_int(resources[-1])
    return resources_dict


def parse_p_hero_score(line):
    heroes = line.split()
    if len(heroes) == 1:
        raise IndexError
    heroes_dict = {}
    heroes_dict.fromkeys(kHeroScores)
    # S.isalnum()
    # TODO reverse loop... for i in range(-1, -len(kUnit),  -1):
    # for i in range(-1, len(kUnit)):
    heroes_dict["HeroesKilled"]     = string_to_int(heroes[-4])
    heroes_dict["ItemsObtained"]    = string_to_int(heroes[-3])
    heroes_dict["MercenariesHired"] = string_to_int(heroes[-2])
    heroes_dict["ExperienceGained"] = string_to_int(heroes[-1])
    return heroes_dict
