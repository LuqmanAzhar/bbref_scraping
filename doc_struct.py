from mongoengine import *


class Team(Document):
    abbreviation = StringField(max_length=3)
    team_name = StringField()
    # todo add more fields which are appropriate to the team
    # current players
    # players who have played a game
    # home wins
    # home losses
    # away wins
    # away losses


class Game(Document):
    meta = {"collection": 'game'}
    bbref_ID = StringField(max_length=12)
    game_time = DateTimeField(required=True)
    season = IntField()
    home_team = StringField()
    away_team = StringField()
    home_score = IntField()
    away_score = IntField()

