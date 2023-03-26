# The First Test for League API
# Nate Bursch
# endpoints
# https://developer.riotgames.com/apis#match-v5/GET_getMatch

import requests
import json
import time
import threading

import pandas as pd
# daily api key - get a new one at https://developer.riotgames.com/
api_key = "RGAPI-ed3c4252-79fc-4c7a-8363-24f946549e6e"

#a url
base_url = "https://na1.api.riotgames.com"

s_name = "kittykat2532"

region = "AMERICAS"
match_v5_base_URL = f"https://{region}.api.riotgames.com"

headers_api = {"X-Riot-Token": api_key}

def GetSummonerPUUID(s_name,debug=False):
    try:
        get_name = f"/lol/summoner/v4/summoners/by-name/{s_name}"

        response = requests.get(f"{base_url}{get_name}", headers={"X-Riot-Token": api_key})

        data = response.json()

        puuid = data['puuid']

    except:
        puuid = data

    return puuid

def GetSummonerName(puuid, debug=False):
    puuid_endpoint = f"/lol/summoner/v4/summoners/by-puuid/{puuid}"

    if debug: print(f"Attempting to get info of player: {puuid}")
    response = requests.get(f"{base_url}{puuid_endpoint}", headers=headers_api)

    if response.status_code == 200:
        summoner_info = response.json()
        summoner_name = summoner_info["name"]
        if debug: print(f"Retrived Summoner name: {summoner_name}")
        return summoner_name
    else:
        if debug: print("Error getting summoner info")

def GetRecentMatches(s_name,debug=False):
    
    #get puuid of summoner name
    if len(s_name) < 78:
        puuid = GetSummonerPUUID(s_name)
    else: puuid = s_name

    region = 'AMERICAS'

    #endpoint of 
    recent_matches_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"

    if debug: print("Attemping to get recent matches")
    response = requests.get(recent_matches_url, headers={"X-Riot-Token": api_key})

    if response.status_code == 200:
        recent_matches = response.json()
        #retrieves last 20 match IDS
        if debug: print(f"Retrieved Last 20 Matches for {s_name} : {puuid}")
        return recent_matches
    
    else:
        if debug: print("Error getting recent matches")
        return [0]

def GetMatchDetails(match_id,debug=False):
    match_info_url = f"/lol/match/v5/matches/{match_id}"

    if debug: print(f"Attempting to get match info for {match_id}")
    response = requests.get(f"{match_v5_base_URL}{match_info_url}", headers=headers_api )

    if response.status_code == 200:
        if debug: print(f"Retrieved Match: {match_id}")
        data = response.json()
        return data
    else:
        if debug: print("Error getting match data")
        return [0]

def GetPlayerNames(participants,debug=False):
    players = []
    #go through the list of participants and get the names of each along with the puuid
    for player in participants:
        s_name = GetSummonerName(player)
        #create an array containing the s_name and player puuid
        player_info = [s_name,player]
        players.append(player_info)
    
    return players



# try:
#     with open("players.json","r") as f:
#         player_hash = json.load(f)

# except:
#     player_hash = {}

# # print(type(player_hash))

# # player_hash["Fart"]=123816238612
# # print(player_hash["Fart"])

# r_matches = GetRecentMatches(s_name)

# data = GetMatchDetails(r_matches[1])

# players = GetPlayerNames(data["metadata"]['participants'])

# for n in range(len(players)):
#     if players[n][0] not in players:
#         player_hash[players[n][0]] = players[n][1]

# print(type(player_hash))

# with open("players.json", "w") as f:
#     json.dump(player_hash,f)

##################################################
#create a hash of millions of user names
def AddToMotherList(name):
    try:
        with open("players.json","r") as f:
            player_hash = json.load(f)

    except:
        player_hash = {}

    r_matches = GetRecentMatches(name)

    for i in range(10):
    # for i in range(len(r_matches)):
        data = GetMatchDetails(r_matches[i])

        players = GetPlayerNames(data["metadata"]['participants'])
        counter = 0
        for n in range(len(players)):
            if players[n][0] not in player_hash:
                counter += 1
                player_hash[players[n][0]] = players[n][1]
        print(f"{i}: Added {counter} players to mothership")



    with open("players.json", "w") as f:
        json.dump(player_hash,f)
    
    #return a random name to use next
    return players[0][0] if players[0][0] != name else players[1][0]



def GetPlayerNames():

    def input_with_timeout(prompt, timeout):
        print(prompt)
        timer = threading.Timer(timeout, lambda: print("\nTimeout!"))
        timer.start()
        user_input = input()
        timer.cancel()
        return user_input

    run = True
    counter = 0
    name = "Mac3"
    while run:
        print(f"Run: {counter}\tUsing Name: {name}")
        name = AddToMotherList(name)

        # Prompt the user for input with a timeout of 120 seconds  gets around the request limit on riot
        # user_input = input_with_timeout("Enter 'q' to quit: ", 5)
        # if user_input == 'q':
        #     run = False
        counter += 1
        # Pause for 2 minutes
        time.sleep(120)

    # print(f"Run: {counter}\tUsing Name: {name}")
    # name = AddToMotherList(name)
    # print(name)

#27000 games
def GetMatchIDs():
    with open("players.json","r") as f:
        player_hash = json.load(f)

    count = 0
    total_matches = 0
    for player,puuid in player_hash.items():
        try:
            with open("matchIDS.json","r") as p:
                matchids_hash = json.load(p)
        except:
            matchids_hash = {}

        print(f"Getting match details from {player} : {puuid}")
        matches = GetRecentMatches(puuid,False)
        count+=1
        for m in matches:
            if m not in matchids_hash:
                matchids_hash[m] = m
                total_matches+=1
            

        with open("matchIDS.json", "w") as p:
            json.dump(matchids_hash,p)

        if count % 200 == 0:
            print("-"*100,f"\nWait for two minutes\nTotal Matches Found: {total_matches}")
            time.sleep(120)

def SaveJSON(data,name):
    with open(name,"w") as f:
        json.dump(data,f)

1

def GetSingleMatchData(matchID):    
    return GetMatchDetails(matchID)


def GetAllMatchData(match_ids_filename, match_data_filename):
    # number of times a request is made
    request_count = 0
    count = 0

    match_ids = GetJSONdata(match_ids_filename)
    
    # go through each key value pair and request the data
    for key, value in match_ids.items():
        try:
            print(f"{request_count}: Getting data from {key}")
            # get match data of the key - which is the match id
            if (request_count % 100 == 0) and (request_count > 0): time.sleep(120)
            data = GetSingleMatchData(key)
           
            request_count +=1

            # convert JSON to pandas dataframe
            particpants = pd.json_normalize(data['info']["participants"])
            base_info = pd.json_normalize(data['info']).drop("participants",axis=1)

            # duplicating it to match up with the particpants info
            base_info = pd.concat([base_info]*len(particpants),ignore_index=True)

            # ten rows of new info
            result = pd.concat([base_info, particpants], axis=1)
            
            # append to motherload
            with open(match_data_filename, 'a') as m:
                result.to_csv(m,header=False,index=False)
        except KeyboardInterrupt:
            print("Keyboard exit caught - exiting program")
            break
        except:
            print(f"ERROR - getting data from {key}")
        
        count+= 1
        



def CreateFirst():
    # load JSON data
    with open('matchdata.json') as f:
        data = json.load(f)

    # convert JSON to pandas dataframe
    particpants = pd.json_normalize(data['info']["participants"])
    base_info = pd.json_normalize(data['info']).drop("participants",axis=1)

    # duplicating it to match up with the particpants info
    base_info = pd.concat([base_info]*len(particpants),ignore_index=True)

    # ten rows of info
    result = pd.concat([base_info, particpants], axis=1)
        
    # save dataframe to CSV
    result.to_csv('data.csv', index=False)



CreateFirst()
GetAllMatchData("matchIDS.json",'data.csv')