# The First Test for League API
# Nate Bursch

import requests

# Replace "YOUR_API_KEY" with your actual API key
api_key = "RGAPI-ed3c4252-79fc-4c7a-8363-24f946549e6e"

# Set up the base URL for API requests
base_url = "https://na1.api.riotgames.com"

s_name = "fearfracture"

region = "AMERICAS"
match_v5_base_URL = f"https://{region}.api.riotgames.com"

headers_api = {"X-Riot-Token": api_key}

def GetSummonerPUUID(s_name):
    # Set up the endpoint for retrieving summoner information
    try:
        get_name = f"/lol/summoner/v4/summoners/by-name/{s_name}"

        response = requests.get(f"{base_url}{get_name}", headers={"X-Riot-Token": api_key})

        data = response.json()

        puuid = data['puuid']

    except:
        puuid = data

    return puuid

def GetSummonerName(puuid):
    puuid_endpoint = f"/lol/summoner/v4/summoners/by-puuid/{puuid}"

    print(f"Attempting to get info of player: {puuid}")
    response = requests.get(f"{base_url}{puuid_endpoint}", headers=headers_api)

    if response.status_code == 200:
        summoner_info = response.json()
        summoner_name = summoner_info["name"]
        print(f"Retrived Summoner name: {summoner_name}")
        return summoner_name
    else:
        print("Error getting summoner info")

def GetRecentMatches(s_name):
    
    #get puuid of summoner name
    puuid = GetSummonerPUUID(s_name)
    region = 'AMERICAS'

    #endpoint of 
    recent_matches_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"

    print("Attemping to get recent matches")
    response = requests.get(recent_matches_url, headers={"X-Riot-Token": api_key})

    if response.status_code == 200:
        recent_matches = response.json()
        #retrieves last 20 match IDS
        print(f"Retrieved Last 20 Matches for {s_name} : {puuid}")
        return recent_matches
    
    else:
        print("Error getting recent matches")
        return [0]

def GetMatchDetails(match_id):
    match_info_url = f"/lol/match/v5/matches/{match_id}"

    print(f"Attempting to get match info for {match_id}")
    response = requests.get(f"{match_v5_base_URL}{match_info_url}", headers=headers_api )

    if response.status_code == 200:
        print(f"Retrieved Match: {match_id}")
        data = response.json()
        return data
    else:
        print("Error getting match data")
        return [0]

def GetPlayerNames(participants):
    players = []
    #go through the list of participants and get the names of each along with the puuid
    for player in participants:
        s_name = GetSummonerName(player)
        #create an array containing the s_name and player puuid
        player_info = [s_name,player]
        players.append(player_info)
    
    return players



r_matches = GetRecentMatches(s_name)
# create a hash of millions of user names
players = {}

for i in range(r_matches):
    data = GetMatchDetails(r_matches[0])
    #print(data)
    players = GetPlayerNames(data["metadata"]['participants'])

    for n in range(players):
        if player[0] in 
        




