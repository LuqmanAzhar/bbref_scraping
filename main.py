import mongoengine
import doc_struct
from bbref import *  # todo consider not using the * command and create classes or importing specific functions

mongoengine.connect("nba")



count = 0

for team_extension in find_active_teams(2020):
    home_game_list = find_list_of_home_games(team_extension)
    count += len(home_game_list)
    for game in home_game_list:
        db_game = doc_struct.Game(
            bbref_ID=game[0],
            game_time=game[1],
            season=game[2],
            home_team=game[3],
            away_team=game[4],
            home_score=game[5],
            away_score=game[6],
        )
        db_game.save()

print(count)
