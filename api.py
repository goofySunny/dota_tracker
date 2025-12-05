import requests, os, files

# Brought to you by @Sunny
# Description: This class interacts with the opendota API and retrieves data for display in the application

CDNURL = "https://cdn.cloudflare.steamstatic.com"
APIBASE = "https://api.opendota.com"
RESPONSENOTOK = "API Response was not OK!"
NOTFOUND = "API Responded with 404 Not Found!"
HEROES = {}
ITEM_BY_ID = {}

print(f"Hello {os.getlogin()} Welcome!")
    
def getHeroes():
    response = requests.get(f"{APIBASE}/api/constants/heroes")
    
    HEROES = response.json()
    return response.json()

def getTopPlayers():
    response = requests.get(f"{APIBASE}/api/topPlayers")
    
    list = []
    
    for obj in response.json():
        print(f"Player : {obj} \n")
        list.append(obj)
    return list

def getMatchById(id):
    response = requests.get(f"{APIBASE}/api/players/{id}")
    
    return response.json()

def getWinLoseByPlayerId(id):
    
    response = requests(f"{APIBASE}/api/players/{id}/wl")

    return response.json()

def getRecentMatchesByPlayerId(id):
    response = requests.get(f"{APIBASE}/api/players/{id}/recentMatches")
    
    return response.json()

def getHeroStatsByPlayerId(id):
    
    response = requests.get(f"{APIBASE}/api/players/{id}/heroes")

    list = []
    
    for hero in response.json():
        list.append(hero)
    return list

def itemPopularityByHeroId(id):
    response = requests.get(f"{APIBASE}/api/heroes/{id}/itemPopularity")
    
    return response.json()

def getAllItems():
    response = requests.get(f"{APIBASE}/api/constants/items")
    
    items = response.json()
    
    global ITEM_BY_ID
    
    ITEM_BY_ID = { str(item["id"]): item for item in items.values() }
    
    return response.json()

def getHeroImage(imageURL):


    response = requests.get(f"{CDNURL}/{imageURL}")
    
    if response.status_code == 404:
        raise Exception(NOTFOUND)
    elif response.status_code != 200:
        raise Exception(RESPONSENOTOK)
    else:
        return response.content

def getItemImage(imageURL, imageName):
    
    if not files.itemExists(imageName):
        response = requests.get(f"{CDNURL}/{imageURL}")
        if response.status_code == 404:
            raise Exception(NOTFOUND)
        elif response.status_code != 200:
            raise Exception(RESPONSENOTOK)
        else:
            files.cacheItemIcon(response.content, imageName)
            return files.getItemIcon(imageName)
    else:
        return files.getItemIcon(imageName)

