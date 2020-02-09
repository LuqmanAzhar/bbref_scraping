from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import pytz
import requests

BBREF_URL = "https://www.basketball-reference.com"

BBREF_TIMEZONE = timezone("US/Eastern")


def find_active_teams(season):
    season = str(season)

    teams_html = requests.get(BBREF_URL + "/leagues/NBA_" + season + ".html")

    team_soup = BeautifulSoup(teams_html.content, "html.parser")

    eastern_conf_urls = a_tags_in_table_id(team_soup, "confs_standings_E")

    western_conf_urls = a_tags_in_table_id(team_soup, "confs_standings_W")

    return eastern_conf_urls + western_conf_urls


def a_tags_in_table_id(soup, table_id):
    active_teams = soup.find("table", attrs={"id": table_id})

    list_of_teams_url = []

    for child in active_teams.find_all("a"):
        list_of_teams_url.append(child["href"])

    return list_of_teams_url


def find_list_of_home_games(team_base_extension):
    team_season_extension = team_base_extension[:-5] + "_games" + team_base_extension[-5:]

    season = team_base_extension[-9:-5]

    season_url = BBREF_URL + team_season_extension

    season_html = requests.get(season_url)

    schedule_soup = BeautifulSoup(season_html.content, "html.parser")

    team_name = schedule_soup.find_all("span", attrs={"itemprop": "name"})[1]

    team_abbreviation = team_season_extension[7:10]

    list_of_home_games = []

    for row in schedule_soup.find_all("tr", attrs={"class": None})[1:]:
        num = row.find("td", attrs={"data-stat": "game_location"})

        if not num.string:
            parent = num.parent
            list_of_home_games.append(row_to_document(parent, team_abbreviation, team_name.string, season))

    return list_of_home_games


def row_to_document(row, team_abbreviation, team_name, season):
    date = row.find("td", attrs={"data-stat": "date_game"})["csk"]
    time = row.find("td", attrs={"data-stat": "game_start_time"}).string
    year, month, day = [int(i) for i in date.split("-")]
    hours, minutes = [int(i) for i in time[:-1].split(':')]
    if time[-1] == 'p':
        hours += 12
        if hours == 24:
            hours = 0
    game_datetime = datetime(year, month, day, hours, minutes)  # gets the naive datetime
    game_datetime = BBREF_TIMEZONE.localize(game_datetime)  # converts the naive datetime into aware BB REF DT aware
    game_datetime = game_datetime.astimezone(pytz.UTC)  # converted datetime to UTC for storage in database

    away_team = row.find("td", attrs={"data-stat": "opp_name"}).string
    bbref_id = f"{year}{month}{day}0{team_abbreviation}"
    if row.find("td", attrs={"data-stat": "pts"}).string:
        home_points = int(row.find("td", attrs={"data-stat": "pts"}).string)
        away_points = int(row.find("td", attrs={"data-stat": "opp_pts"}).string)

        return bbref_id, game_datetime, season, team_name, away_team, home_points, away_points
    else:
        return bbref_id, game_datetime, season, team_name, away_team, None, None


