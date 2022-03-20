import json
import requests

def getLiveMatches():
    url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/list"
    querystring = {"matchState":"live"}
    headers = {
        'x-rapidapi-host': "unofficial-cricbuzz.p.rapidapi.com",
        'x-rapidapi-key': "ddaf3750e1msh9efa2768c242e0cp144c0djsn9fbedd4739d1"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    api = json.loads(response.text)
    return api

def getScoreCard(matchId):
    url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-scorecard"
    querystring = {"matchId":matchId}
    headers = {
        'x-rapidapi-host': "unofficial-cricbuzz.p.rapidapi.com",
        'x-rapidapi-key': "ddaf3750e1msh9efa2768c242e0cp144c0djsn9fbedd4739d1"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    api = json.loads(response.text)
    return api