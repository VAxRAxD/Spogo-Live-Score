import json
import requests

def getLiveMatches():
    url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/list"
    querystring = {"matchState":"live"}
    headers = {
        'x-rapidapi-host': "unofficial-cricbuzz.p.rapidapi.com",
        'x-rapidapi-key': ""
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    api = json.loads(response.text)
    return api

def getScoreCard(matchId):
    url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-scorecard"
    querystring = {"matchId":matchId}
    headers = {
        'x-rapidapi-host': "unofficial-cricbuzz.p.rapidapi.com",
        'x-rapidapi-key': ""
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    api = json.loads(response.text)
    return api

def getPointsTable(seriesId):
    url = "https://unofficial-cricbuzz.p.rapidapi.com/series/get-points-table"
    querystring = {"seriesId":seriesId}
    headers = {
        'x-rapidapi-host': "unofficial-cricbuzz.p.rapidapi.com",
        'x-rapidapi-key': ""
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    api = json.loads(response.text)
    return api