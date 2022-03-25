import json
import requests

def getLiveMatches():
    print("API Call")
    url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/list"
    querystring = {"matchState":"live"}
    headers = {
	    "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
	    "X-RapidAPI-Key": "8371cc6094msh32984b9598aed5ep1731b6jsn14056246b92a"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    api = json.loads(response.text)
    return api

def getScoreCard(matchId):
    print("API Call")
    url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-scorecard"
    querystring = {"matchId":matchId}
    headers = {
	    "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
	    "X-RapidAPI-Key": "8371cc6094msh32984b9598aed5ep1731b6jsn14056246b92a"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    api = json.loads(response.text)
    return api

"""
API call points table of IPL 2022
Activate if necesssary
"""
# def getPointsTable(seriesId):
#     print("API Call")
#     url = "https://unofficial-cricbuzz.p.rapidapi.com/series/get-points-table"
#     querystring = {"seriesId":seriesId}
#     headers = {
#         "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
#         "X-RapidAPI-Key": "8371cc6094msh32984b9598aed5ep1731b6jsn14056246b92a"
#     }
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     api = json.loads(response.text)
#     return api