import datetime
DEBUG = False

# Update the games and tags, don't build from scratch
update = True
build  = not update


# GetGames/LoopTags consts
# To lessen the load on W3A servers (seconds per account).
query_delay = 0.25
# When extracting games with Beautiful Soup.
game_fields = ['date_time', 'winning_player','player1_name','player2_name']
earliest_time = '01-01-2015 00:00'
earliest_time = datetime.datetime.strptime(earliest_time,'%d-%m-%Y %H:%M')

# UpdateInactiveAccounts consts
force_retirement = False
retirement_cutoff_months = 3
seed_cutoff_days = 20

######################################
# File locations and container names #
######################################
# Tags
all_tags_file           = "data/all_tags_info.py"
all_tags_list_file      = "data/all_tags.py"
active_tags_file        = "data/active_tags_info.py"
retired_tags_file       = "data/retired_tags_info.py"
seed_tags_file          = "data/seed_tags_info.py"

all_tags_container      = "all_tags"
all_tags_list_container = "all_tags_list"
active_tags_container   = "active_tags"
retired_tags_container  = "retired_tags"
seed_tags_container     = "seed_tags"

# Games
all_games_file          = "data/all_games.py"
games2015_file          = "data/games2015.py"
games2016_file          = "data/games2016.py"
games2017_file          = "data/games2017.py"

all_games_container     = "all_games"
games_container         = "games"


######################################
# Elo calculation constants          #
######################################
K_FACTOR_BURST          = 100
K_FACTOR_EARLY          = 48
K_FACTOR_MID            = 36
K_FACTOR_LATE           = 24
STARTING_ELO_CONST      = 1000.
