import requests
from bs4 import BeautifulSoup
import os
import random
import threading
import time




def get_images():
    queries = ["ghost", "fighter+jet", "evil+monster", "dragon", "evil+robot", "alien", "dark+knight",  "necromancer+humanoid", "orc+horde", "shadow+assassin", "skeleton+army", "space+warship", "superpowered+villain", "undead+army"]
    query = random.choice(queries)
    print("Starting query " + query)
    tempURL_list = []
    URL_list = []
    r = requests.get("https://www.google.com/search?q=" + query +"+4k&client=ubuntu-sn&hs=Gpk&channel=fs&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjx_Lz9uYL-AhVyLUQIHQN6ChEQ0pQJegQIAxAC&biw=1846&bih=968&dpr=1#imgrc=hQb-oUtO6irbwM")
    soup = BeautifulSoup(r.content, 'html5lib') 
    pretty_data = soup.prettify()
    lines = pretty_data.split('/url?q=')
    for line in lines:
        line = line.split("\n")
    for line in lines:
        if(("google" not in line) and ("https://" in line)):
            tempURL_list.append(line.split("\"")[0])

    for website in tempURL_list:
        URL_list.append(website.split("&amp")[0])
    manager = threadManager(URL_list, query = query)
    t1 = threading.Thread(manager.makeThreads(), daemon=True)
    t1.start()
    time.sleep(20)
    print("ending webscraper")

class threadManager:
    def __init__(self, URLS_to_do = [], linesDone = 0, URLS_completed = [], threadList = [], query = "", killThreads = False, startTime = int(time.time())):
        self.URLS_to_do = URLS_to_do
        self.linesDone = linesDone
        self.URLS_completed = URLS_completed
        self.threadList = threadList
        self.query = query
        self.killThreads = killThreads
        self.startTime = startTime

    def makeThreads(self):
        for website in self.URLS_to_do:
            t1 = threading.Thread(target=grabDataFromWebsite, args=(website, self.query, self), daemon=True)
            t1.start()
            self.threadList.append(t1)

def grabDataFromWebsite(website, query, threadManager):
    if(website not in threadManager.URLS_completed):
        connected = False
        tries = 0
        r=None
        while(not connected and not threadManager.killThreads):
            try:
                if(tries<3):
                    r = requests.get(website, timeout=1.5)
                    connected = True
                else:
                    break
            except:
                #print("connect failed, trying again")
                tries+=1
        if (r!=None):
            soup = BeautifulSoup(r.content, 'html5lib') 
            pretty_data = soup.prettify()
            lines = pretty_data.split('\n')
            for line in lines:
                if("https" in line and "image" in line):
                    try:
                        image_url = line.split("\"")[1]
                    except:
                        break

                    if "https" in image_url and "slideshare" not in image_url and threadManager.linesDone<150 and threadManager.killThreads == False:
                        threadManager.linesDone+=1
                        try:
                            img_data = requests.get(image_url, timeout=1.5).content
                            with open(os.path.join(os.curdir, "images", query+ str(threadManager.linesDone)+'.jpg'), 'wb') as handler:
                                handler.write(img_data)
                                #print(website)
                                threadManager.URLS_completed.append(website)
                            with open(os.path.join(os.curdir, "images", query+ str(threadManager.linesDone)+'.jpg'), 'r') as handler:
                                text = handler.read()
                                if("js" in text or "return" in text or "css" in text or text == '' or os.path.getsize("./images/"+query+ str(threadManager.linesDone)+'.jpg')<10000000):
                                    os.remove(query+ str(threadManager.linesDone)+'.jpg')
                                else:
                                    break
                                
                        except:
                            pass
        
