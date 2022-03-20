from socket import timeout
from argon2 import PasswordHasher
from django.core.cache import cache
from . apicalls import *
import datetime
import pytz
IST = pytz.timezone('Asia/Kolkata')
flag=True

def getMatchDetails():
    data=None
    if not cache.get("match"):
        h,m=(datetime.datetime.now(IST).strftime("%H %M").split(" "))
        if float(h+"."+m)> 6.30:
            print("Its time for match")
            api=getLiveMatches()
            for matches in api["typeMatches"]:
                if matches["matchType"]=="Women":
                    data=matches["seriesAdWrapper"]
            if data==None:
                print("No womens series found")
                return
            matches=None
            for series in data:
                try:
                    if series["seriesMatches"]["seriesId"]==3202: #3482 #3202 #3657
                        matches=series["seriesMatches"]["matches"]
                except:
                    pass
            if matches==None:
                print("No current matches in series")
                return
            live=None
            for match in matches:
                if match["matchInfo"]["state"]!="Upcoming" and match["matchInfo"]["state"]!="Complete":
                    live=match["matchInfo"]
            if live:
                data={
                    "matchId":match["matchInfo"]["matchId"],
                    "team1":match["matchInfo"]["team1"]["teamSName"],
                    "team2":match["matchInfo"]["team2"]["teamSName"]
                }
                cache.set("match",data,None)
            else:
                print("No live matches")
                return

def getStats():
    h,m=(datetime.datetime.now(IST).strftime("%H %M").split(" "))
    if float(h+"."+m)<=6.30:
        return
    print("Call for score")
    live=cache.get("match")
    print("Live match is",live)
    if live:
        details=getScoreCard(live["matchId"])
        if "won by" in details["status"]:
            print("Match Completed and count down intiated")
            if flag:
                cache.delete("match")
                cache.set("match",live,timeout=300)
                flag=False
    else:
        cache.delete("score")
        return
    team1score=None
    team2score=None
    team1wickets=None
    team2wickets=None
    team1overs=None
    team2overs=None
    batsman=dict()
    batsman[live["team1"]]=dict()
    batsman[live["team2"]]=dict()
    allbatters=dict()
    allbatters[live["team1"]]=dict()
    allbatters[live["team2"]]=dict()
    bowler=dict()
    bowler[live["team1"]]=dict()
    bowler[live["team2"]]=dict()
    allbowlers=dict()
    allbowlers[live["team1"]]=dict()
    allbowlers[live["team2"]]=dict()
    scorecard=details["scorecard"]
    for innings in scorecard:
        if innings["batTeamSName"]==live["team1"]:
            try:
                team1score=innings["score"]
            except:
                team1score=0
            try:
                team1wickets=innings["wickets"]
            except:
                team1wickets=0
            try:
                team1overs=innings["overs"]
            except:
                team1overs=0
        else:
            try:
                team2score=innings["score"]
            except:
                team2score=0
            try:
                team2wickets=innings["wickets"]
            except:
                team2wickets=0
            try:
                team2overs=innings["overs"]
            except:
                team2overs=0
        for batter in innings["batsman"]:
            try:
                name=batter["nickName"]
            except:
                name=batter["name"]
            try:
                if batter["outDec"]:
                    try:
                        if batter["runs"]:
                            if batter["outDec"]=="batting":
                                batsman[innings["batTeamSName"]][name]={"runs":batter["runs"]}
                            allbatters[innings["batTeamSName"]][name]={"runs":batter["runs"]}
                    except:
                        if batter["outDec"]=="batting":
                            batsman[innings["batTeamSName"]][name]={"runs":0}
                        allbatters[innings["batTeamSName"]][name]={"runs":0}
                    try:
                        if batter["balls"]:
                            if batter["outDec"]=="batting":
                                batsman[innings["batTeamSName"]][name]["balls"]=batter["balls"]
                            allbatters[innings["batTeamSName"]][name]["balls"]=batter["balls"]
                    except:
                        if batter["outDec"]=="batting":
                            batsman[innings["batTeamSName"]][name]["balls"]=0
                        allbatters[innings["batTeamSName"]][name]["balls"]=0
                    try:
                        allbatters[innings["batTeamSName"]][name]["fours"]=batter["fours"]
                    except:
                        allbatters[innings["batTeamSName"]][name]["fours"]=0
                    try:
                        allbatters[innings["batTeamSName"]][name]["sixes"]=batter["sixes"]
                    except:
                        allbatters[innings["batTeamSName"]][name]["sixes"]=0
                    allbatters[innings["batTeamSName"]][name]["strkRate"]=batter["strkRate"]
                    allbatters[innings["batTeamSName"]][name]["outDec"]=batter["outDec"]
                    
            except:
                allbatters[innings["batTeamSName"]][name]="Yet to Bat"
        for bowlers in innings["bowler"]:
            try:
                name=bowlers["nickName"]
            except:
                name=bowlers["name"]
            if innings["batTeamSName"]==live["team1"]:
                bowlteam=live["team2"]
            else:
                bowlteam=live["team1"]
            try:
                if bowlers["overs"]:
                    if "." in bowlers["overs"]:
                        bowler[bowlteam][name]={"overs":bowlers["overs"]}
                    allbowlers[bowlteam][name]={"overs":bowlers["overs"]}
                    try:
                        if bowlers["runs"]:
                            if "." in bowlers["overs"]:
                                bowler[bowlteam][name]["runs"]=bowlers["runs"]
                            allbowlers[bowlteam][name]["runs"]=bowlers["runs"]
                    except:
                        if "." in bowlers["overs"]:
                            bowler[bowlteam][name]["runs"]=0
                        allbowlers[bowlteam][name]["runs"]=0
                    try:
                        if bowlers["wickets"]:
                            if "." in bowlers["overs"]:
                                bowler[bowlteam][name]["wickets"]=bowlers["wickets"]
                            allbowlers[bowlteam][name]["wickets"]=bowlers["wickets"]
                    except:
                        if "." in bowlers["overs"]:
                            bowler[bowlteam][name]["wickets"]=0
                        allbowlers[bowlteam][name]["wickets"]=0
                    try:
                       allbowlers[bowlteam][name]["economy"]=bowlers["economy"] 
                    except:
                        allbowlers[bowlteam][name]["economy"]=0
            except:
                pass
    if team1score==None and team2score==None:
        data={
            "status":details["status"],
            "team1":{
                "teamName":live["team1"],
                "teamScore":"Yet to Bat",
            },
            "team2":{
                "teamName":live["team2"],
                "teamScore":"Yet to Bat"
            }
        }
        data["team1"]["scorecard"]={"batters":allbatters[live["team1"]]}
        data["team2"]["scorecard"]={"batters":allbatters[live["team2"]]}
        cache.set("score",data,None)
        return
        
    if team1score==None:
        team1score="Yet to bat"
        data={
            "status":details["status"],
            "team1":{
                "teamName":live["team1"],
                "teamScore":team1score
            },
            "team2":{
                "teamName":live["team2"],
                "teamScore":team2score,
                "teamWickets":team2wickets,
                "teamOvers":team2overs,
                "currBatters":batsman[live["team2"]]
            }
        }
        if details["status"]!="Innings Break":
            data["team1"]["currBowler"]=bowler[live["team1"]]
        if details["status"]=="Innings Break":
            data["team2"].pop("currBatters")
        data["team1"]["scorecard"]={"batters":allbatters[live["team1"]]}
        data["team1"]["scorecard"]["bowlers"]=allbowlers[live["team1"]]
        data["team2"]["scorecard"]={"batters":allbatters[live["team2"]]}
        cache.set("score",data,None)
        return

    if team2score==None:
        team2score="Yet to bat"
        team2overs=""
        team2wickets=""
        data={
            "status":details["status"],
            "team1":{
                "teamName":live["team1"],
                "teamScore":team1score,
                "teamWickets":team1wickets,
                "teamOvers":team1overs,
                "currBatters":batsman[live["team1"]]
            },
            "team2":{
                "teamName":live["team2"],
                "teamScore":team2score
            }
        }
        if details["status"]!="Innings Break":
            data["team2"]["currBowler"]=bowler[live["team2"]]
        if details["status"]=="Innings Break":
            data["team1"].pop("currBatters")
        data["team1"]["scorecard"]={"batters":allbatters[live["team1"]]}
        data["team2"]["scorecard"]={"batters":allbatters[live["team2"]]}
        data["team2"]["scorecard"]["bowlers"]=allbowlers[live["team2"]]
        cache.set("score",data,None)
        return

    data={
        "status":details["status"],
        "team1":{
            "teamName":live["team1"],
            "teamScore":team1score,
            "teamWickets":team1wickets,
            "teamOvers":team1overs
        },
        "team2":{
            "teamName":live["team2"],
            "teamScore":team2score,
            "teamWickets":team2wickets,
            "teamOvers":team2overs
        }
    }
    if len(batsman[live["team1"]])>0:
        data["team1"]["currBatters"]=batsman[live["team1"]]
        data["team2"]["currBowler"]=bowler[live["team2"]]
    if len(batsman[live["team2"]])>0:
        data["team2"]["currBatters"]=batsman[live["team2"]]
        data["team1"]["currBowler"]=bowler[live["team1"]]
    data["team1"]["scorecard"]={"batters":allbatters[live["team1"]]}
    data["team1"]["scorecard"]["bowlers"]=allbowlers[live["team1"]]
    data["team2"]["scorecard"]={"batters":allbatters[live["team2"]]}
    data["team2"]["scorecard"]["bowlers"]=allbowlers[live["team2"]]
    cache.set("score",data,None)
    return