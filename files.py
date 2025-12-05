import os

# Brought to you by @Sunny
# Description: The methods in this file retrieve icons from cache or save downloaded icons to cache to reduce download
dawnBreaker = "/apps/dota2/images/dota_react/heroes/dawnbreaker.png?"
HEROCACHE = "cache/hero"
ITEMCACHE = "cache/item"

def initCache():
    try:
        os.makedirs(HEROCACHE)
        print(f"Cache initialized at ./{HEROCACHE}")
    except FileExistsError:
        print(f"Utilizing existing cache at ./{HEROCACHE}")
    except PermissionError:
        print(f"Failed to initialize cache at ./{HEROCACHE} due to permission")
    except Exception as e:
        print(f"Unexpected error {e} occured")
    
    try:
        os.makedirs(ITEMCACHE)
        print(f"Cache initialized at ./{ITEMCACHE}")
    except FileExistsError:
        print(f"Utilizing existing cache at ./{ITEMCACHE}")
    except PermissionError:
        print(f"Failed to initialize cache at ./{ITEMCACHE} due to permission")
    except Exception as e:
        print(f"Unexpected error {e} occured")

def heroExists(heroImageName):
    if os.path.exists(f"{HEROCACHE}/{heroImageName}.png"):
        return True
    else:
        return False

def cacheHeroIcon(imageByte, imageName):
    with open(f"{HEROCACHE}/{imageName}.png", "wb") as f:
        if f.write(imageByte):
            return True
        else: 
            return False

def itemExists(itemImageName):
    if os.path.exists(f"{ITEMCACHE}/{itemImageName}.png"):
        return True
    else:
        return False

def cacheItemIcon(imageByte, imageName):
    with open(f"{ITEMCACHE}/{imageName}.png", "wb") as f:
        if (f.write(imageByte)):
            return True
        else:
            return False
        
def getHeroIcon():
    # TODO : check if heroIcon is present in cache if not retrieve it and put it there
    pass

def getItemIcon(imageName):
    return f"{ITEMCACHE}/{imageName}.png"


# Testing Area:

