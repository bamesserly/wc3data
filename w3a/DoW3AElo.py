import datetime
from datetime import date
from time import sleep 

from GetGames         import GetGames
from CalculateElo     import CalculateElo
from UpdateActiveTags import UpdateActiveTags
from MakeSpreadsheets import MakeSpreadsheets
from UploadToDropbox  import UploadToDropbox

from Utils            import load_data
from Constants        import active_tags_file, active_tags_container
from Constants        import all_tags_file,    all_tags_container
from Constants        import seed_tags_file,   seed_tags_container

def main():
  print "###########################################################################################################"
  print "                BEGINNING DO W3A ELO for", datetime.datetime.today()
  print "###########################################################################################################"
  UpdateActiveTags() # Retire inactive accounts.
                     # input:  all_tags_info.py
                     # output: active_tags_info.py and inactive_tags_info.py

  GetGames()         # Get new games played since the last update
                     # input:  active_tags_info.py
                     # output: all_games.py

  CalculateElo()     # Calculate the Elo of all tags
                     # input:  all_games.py
                     # output: all_tags_info.py

  UpdateActiveTags() # Retire inactive accounts.
                     # input:  all_tags_info.py
                     # output: active_tags_info.py and inactive_tags_info.py

  seed_tags = load_data(seed_tags_file, seed_tags_container)
  MakeSpreadsheets(seed_tags, "ThisWeek") 
  UploadToDropbox("EloSpread_ThisWeek.csv")  # Upload (at least) the active account to dropbox

  sleep(60)

  active_tags = load_data(active_tags_file, active_tags_container)
  MakeSpreadsheets(active_tags, "Active") 
  UploadToDropbox("EloSpread_Active.csv")  # Upload (at least) the active account to dropbox

  sleep(60)

  all_tags = load_data(all_tags_file, all_tags_container)
  MakeSpreadsheets(all_tags, "All") 
                     # Make spreadsheets for active and for all accounts
                     # input:  all_tags_info.py, active_tags_info.py
                     # output: EloSpreadsheet_all.csv, EloSpreadsheet_active.csv
  UploadToDropbox("EloSpread_All.csv")  # Upload (at least) the active account to dropbox
  
if __name__ == "__main__":
  main()
