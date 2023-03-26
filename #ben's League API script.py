#ben's League API script

import requests
import json

api_key = "?api_key=RGAPI-00767a03-e6d5-4dd3-94f8-2ab79d1faf8c"

def GetJSONdata(name):
    with open(name,"r") as f:
        return json.load(f)
    
playersData = GetJSONdata("players.json")
size = len(playersData)
#print(size)
firstPlayer = list(playersData.values())[0]



def getSummonerID(puuid):
    url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" + puuid + api_key
    response = requests.get(url)
    return response.json()


#get the player ID of every player
for i in range(size):
    playerPUUID = list(playersData.values())[i]

    playerID = getSummonerID(playerPUUID)
    

    playerID = playerID['id']

    id_url = ("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/" +
              playerID +
              "?api_key=RGAPI-00767a03-e6d5-4dd3-94f8-2ab79d1faf8c")

    response = requests.get(id_url)
    id_data = response.json()

    print(id_data)
    try:
        tier = id_data[1]['tier']
        rank = id_data[1]['rank']

        print(tier)
        print(rank + "\n")
    except:
        print("Problem getting a rank")

    



    #playerID = player["accountId"]
    #print(playerID)
    #print(getSummonerID(player))


#index each rank as an int