from argon2 import PasswordHasher
from django.core.cache import cache
from . apicalls import *
import datetime
import pytz
IST = pytz.timezone('Asia/Kolkata')
flag=True
post=False
nobat="Yet to bat"

def getMatchDetails():
    data=None
    if not cache.get("match"):
        h,m=(datetime.datetime.now(IST).strftime("%H %M").split(" "))
        # if 15.20<float(h+"."+m)<18.30 or 19.20<float(h+"."+m)<23.00:
        if 16.20<float(h+"."+m)<20.00:
            print("Its time for match")
            api=getLiveMatches()
            for matches in api["typeMatches"]:
                if matches["matchType"]=="International":
                    data=matches["seriesAdWrapper"]
            if data==None:
                print("No womens series found")
                return
            matches=None
            for series in data:
                try:
                    if series["seriesMatches"]["seriesId"]==0000: #3482 #3202 *#3657 #3863
                        matches=series["seriesMatches"]["matches"]
                except:
                    pass
            if matches==None:
                print("No current matches in series")
                return
            live=None
            for match in matches:
                # if match["matchInfo"]["matchId"]==38436:
                if match["matchInfo"]["state"]!="Upcoming" and match["matchInfo"]["state"]!="Complete":
                    live=match["matchInfo"]
                    break
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
    global flag,nobat
    h,m=(datetime.datetime.now(IST).strftime("%H %M").split(" "))
    if float(h+"."+m)<=16.25:
        return
    print("Call for score")
    live=cache.get("match")
    print("Live match is",live)
    if live:
        print("API call")
        details=getScoreCard(live["matchId"])
        if "won by" in details["status"] or "Match drawn" in details["status"]:
            if "super over" in details["status"]:
                if flag:
                    print("Match in super over")
                    cache.delete("match")
                    cache.set("match",live,timeout=1800)
                    flag=False
            if flag:
                print("Match Completed and count down intiated")
                cache.delete("match")
                cache.set("match",live,timeout=300)
                flag=False
                nobat="Did not bat"
    else:
        cache.delete("score")
        flag=True
        return
    team1score=dict()
    team2score=dict()
    team1wickets=dict()
    team2wickets=dict()
    team1overs=dict()
    team2overs=dict()
    batsman=dict()
    batsman[live["team1"]]=dict()
    batsman[live["team2"]]=dict()
    allbatters=dict()
    bowler=dict()
    bowler[live["team1"]]=dict()
    bowler[live["team2"]]=dict()
    allbowlers=dict()
    scorecard=details["scorecard"]
    for innings in scorecard:
        if innings["batTeamSName"]==live["team1"]:
            try:
                if team1score:
                    team1score["2"]=str(innings["score"])
                else:
                    team1score["1"]=str(innings["score"])
            except:
                if team1score:
                    team1score["2"]="0"
                else:
                    team1score["1"]="0"
            try:
                if team1wickets:
                    team1wickets["2"]=innings["wickets"]
                else:
                    team1wickets["1"]=innings["wickets"]
            except:
                if team1wickets:
                    team1wickets["2"]="0"
                else:
                    team1wickets["1"]="0"
            try:
                if team1overs:
                    team1overs["2"]=innings["overs"]
                else:
                    team1overs["1"]=innings["overs"]
            except:
                if team1overs:
                    team1overs["2"]="0"
                else:
                    team1overs["1"]="0"
        else:
            try:
                if team2score:
                    team2score["2"]=str(innings["score"])
                else:
                    team2score["1"]=str(innings["score"])
            except:
                if team2score:
                    team2score["2"]="0"
                else:
                    team2score["1"]="0"
            try:
                if team2wickets:
                    team2wickets["2"]=innings["wickets"]
                else:
                    team2wickets["1"]=innings["wickets"]
            except:
                if team2wickets:
                    team2wickets["2"]="0"
                else:
                    team2wickets["1"]="0"
            try:
                if team2overs:
                    team2overs["2"]=innings["overs"]
                else:
                    team2overs["1"]=innings["overs"]
            except:
                if team2overs:
                    team2overs["2"]="0"
                else:
                    team2overs["1"]="0"
        if innings["batTeamSName"] in allbatters:
            inning="2"
        else:
            inning="1"
            allbatters[innings["batTeamSName"]]=dict()
        allbatters[innings["batTeamSName"]][inning]=dict()
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
                            allbatters[innings["batTeamSName"]][inning][name]={"runs":batter["runs"]}
                    except:
                        if batter["outDec"]=="batting":
                            batsman[innings["batTeamSName"]][name]={"runs":0}
                        allbatters[innings["batTeamSName"]][inning][name]={"runs":0}
                    try:
                        if batter["balls"]:
                            if batter["outDec"]=="batting":
                                batsman[innings["batTeamSName"]][name]["balls"]=batter["balls"]
                            allbatters[innings["batTeamSName"]][inning][name]["balls"]=batter["balls"]
                    except:
                        if batter["outDec"]=="batting":
                            batsman[innings["batTeamSName"]][name]["balls"]=0
                        allbatters[innings["batTeamSName"]][inning][name]["balls"]=0
                    try:
                        allbatters[innings["batTeamSName"]][inning][name]["fours"]=batter["fours"]
                    except:
                        allbatters[innings["batTeamSName"]][inning][name]["fours"]=0
                    try:
                        allbatters[innings["batTeamSName"]][inning][name]["sixes"]=batter["sixes"]
                    except:
                        allbatters[innings["batTeamSName"]][inning][name]["sixes"]=0
                    allbatters[innings["batTeamSName"]][inning][name]["strkRate"]=batter["strkRate"]
                    allbatters[innings["batTeamSName"]][inning][name]["outDec"]=batter["outDec"]
                    
            except:
                allbatters[innings["batTeamSName"]][inning][name]=nobat
        if innings["batTeamSName"]==live["team1"]:
            bowlteam=live["team2"]
        else:
            bowlteam=live["team1"]
        if bowlteam in allbowlers:
            inning="2"
        else:
            inning="1"
            allbowlers[bowlteam]=dict()
        allbowlers[bowlteam][inning]=dict()
        for bowlers in innings["bowler"]:
            try:
                name=bowlers["nickName"]
            except:
                name=bowlers["name"]
            try:
                if bowlers["overs"]:
                    if "." in bowlers["overs"]:
                        bowler[bowlteam][name]={"overs":bowlers["overs"]}
                    allbowlers[bowlteam][inning][name]={"overs":bowlers["overs"]}
                    try:
                        if bowlers["runs"]:
                            if "." in bowlers["overs"]:
                                bowler[bowlteam][name]["runs"]=bowlers["runs"]
                            allbowlers[bowlteam][inning][name]["runs"]=bowlers["runs"]
                    except:
                        if "." in bowlers["overs"]:
                            bowler[bowlteam][name]["runs"]=0
                        allbowlers[bowlteam][inning][name]["runs"]=0
                    try:
                        if bowlers["wickets"]:
                            if "." in bowlers["overs"]:
                                bowler[bowlteam][name]["wickets"]=bowlers["wickets"]
                            allbowlers[bowlteam][inning][name]["wickets"]=bowlers["wickets"]
                    except:
                        if "." in bowlers["overs"]:
                            bowler[bowlteam][name]["wickets"]=0
                        allbowlers[bowlteam][inning][name]["wickets"]=0
                    try:
                       allbowlers[bowlteam][inning][name]["economy"]=bowlers["economy"] 
                    except:
                        allbowlers[bowlteam][inning][name]["economy"]=0
            except:
                pass
    if len(team1score)==0 and len(team2score)==0:
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
        
    if len(team1score)==0:
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

    if len(team2score)==0:
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

def getPoints():
    h,m=(datetime.datetime.now(IST).strftime("%H %M").split(" "))
    if 19.00<float(h+"."+m)<19.30 or 23.00<float(h+"."+m)<23.59:
        # table=getPointsTable(3472)
        table={}
        data=dict()
        for team in table["pointsTable"][0]["pointsTableInfo"]:
            data[team["teamName"]]=dict()
            try:
                data[team["teamName"]]["matchesPlayed"]=team["matchesPlayed"]
            except:
                data[team["teamName"]]["matchesPlayed"]=0
            try:
                data[team["teamName"]]["matchesWon"]=team["matchesWon"]
            except:
                data[team["teamName"]]["matchesWon"]=0
            try:
                data[team["teamName"]]["matchesLost"]=team["matchesLost"]
            except:
                data[team["teamName"]]["matchesLost"]=0
            try:
                data[team["teamName"]]["points"]=team["points"]
            except:
                data[team["teamName"]]["points"]=0
            data[team["teamName"]]["nrr"]=team["nrr"]
        cache.set("points",data,None)
    return