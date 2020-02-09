import mongoengine
from doc_struct import Game

mongoengine.connect("nba")


def updating_game_scores():
    """
    Query The database for games without a home team score and the date is earlier then the current ISO

    Atomic update of the documents score scraping the specific URL

    """
    home_wins = Game.objects().filter()
    for game in home_wins:
        print(home_wins.home_team)

updating_game_scores()
