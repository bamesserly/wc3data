from enum import Enum, auto

class kRaces(Enum):
    kNIGHTELF = auto()
    kHUMAN = auto()
    kORC = auto()
    kUNDEAD = auto()
    kRANDOM_N = auto()
    kRANDOM_H = auto()
    kRANDOM_O = auto()
    kRANDOM_U = auto()


class kHeroes(Enum):
    DEMONHUNTER = auto()
    KEEPEROFTHE = auto()
    PRIESTESSOFTHE = auto()
    WARDEN = auto()

    ARCHMAGE = auto()
    BLOODMAGE = auto()
    MOUNTAINKING = auto()
    PALADIN = auto()

    BLADEMASTER = auto()
    FARSEER = auto()
    SHADOWHUNTER = auto()
    TAURENCHIEFTAIN = auto()

    CRYPTLORD = auto()
    DEATHKNIGHT = auto()
    DREADLORD = auto()
    LICH = auto()

    BEASTMASTER = auto()
    DARKRANGER = auto()
    FIRELORD = auto()
    GOBLINALCHEMIST = auto()
    GOBLINTINKER = auto()
    NAGASEAWITCH = auto()
    PANDAREN = auto()
    PITLORD = auto()


class kStages(Enum):
    CENTAURGROVE = auto()
    ECHOISLES = auto()
    FROSTSABRE = auto()
    GNOLLWOOD = auto()
    LEGENDS = auto()
    LOSTTEMPLE = auto()
    MELTINGVALLEY = auto()
    MOONGLADE = auto()
    PLUNDERISLE = auto()
    SECRETVALLEY = auto()
    SCORCHEDBASIN = auto()
    TERENASSTAND = auto()
    THETWORIVERS = auto()
    TIDEWATERGLADES = auto()
    TRANQUILPATHS = auto()
    TURTLEROCK = auto()
    TWISTEDMEADOWS = auto()
    WETLANDS = auto()


class kGameTypes(Enum):
    kSOLO = auto()
    kFFA = auto()
    kTOURNAMENT = auto()
