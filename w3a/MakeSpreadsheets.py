import csv
from datetime import date
from Constants import active_tags_file, active_tags_container #input
import Utils


def MakeSpreadsheets(tags, suffix):
  print "Entering MakeSpreadsheets()"

  dict_list = []
  for t in tags:
    dict_list.append(tags[t])

  dict_list = sorted(dict_list, key=lambda k: k['elo'], reverse = True)

  #today = (date.today()).strftime("%y%m%d")
  #spreadsheet_name = "EloSpreadSheet_{0}.csv".format(today)
  spreadsheet_name = Utils.top + "EloSpread_{0}.csv".format(suffix)
  with open(spreadsheet_name, 'w+') as csvfile:
    fieldnames = ['tag', 'elo', 'ngames', 'wins','losses','winrate','most_recent_game_time']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writer.writerow(fieldnames)
    X = [writer.writerow(dict) for dict in dict_list]

  print "Exiting MakeSpreadsheets()"

if __name__ == "__main__":
  MakeSpreadSheets(active_tags)
