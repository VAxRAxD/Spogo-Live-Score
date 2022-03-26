import json
import requests

def getLiveMatches():
    print("API Call")
    url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/list"
    querystring = {"matchState":"live"}
    headers = {
	    "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
	    "X-RapidAPI-Key": "0f01899b6bmsh4673c9213d932c8p113a06jsnde06f3400db6"
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
	    "X-RapidAPI-Key": "0f01899b6bmsh4673c9213d932c8p113a06jsnde06f3400db6"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    api = json.loads(response.text)
    return api

"""
API call points table of IPL 2022
Activate if necesssary
Enter the API key in headers
"""
# def getPointsTable(seriesId):
#     print("API Call")
#     url = "https://unofficial-cricbuzz.p.rapidapi.com/series/get-points-table"
#     querystring = {"seriesId":seriesId}
#     headers = {
#         "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
#         "X-RapidAPI-Key": ""
#     }
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     api = json.loads(response.text)
#     return api