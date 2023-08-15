import requests
from bs4 import BeautifulSoup
import base64
import os
from PIL import Image
from english_dictionary.scripts.read_pickle import get_dict
import random
from PIL import Image
import os

def get_image():
    english_dict = get_dict()
    queries = []
    while(len(queries) < 1):
        definition = ""
        while(definition[2:4] != "a "):
            word, definition = random.choice(list(english_dict.items()))
            # print(definition[2:4])
            # print(word, definition)
        queries.append(word)
    print(queries)
    #queries = ["lemon", "orange", "banana", "peach", "house", "flower", "meadow", "kitten", "mouse"]
    for query in queries:
        print("Working query " + query)
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

        i=0
        linesDone = 0
        URLS_completed = []
        for website in URL_list:
            #if("html" in website):
            if(website not in URLS_completed):
                connected = False
                tries = 0
                #print(website)
                #input("continue?")
                while(not connected):
                    try:
                        if(tries<3):
                            r = requests.get(website, timeout=0.5)
                            connected = True
                        else:
                            break
                    except:
                        print("connect failed, trying again")
                        tries+=1
                soup = BeautifulSoup(r.content, 'html5lib') 
                pretty_data = soup.prettify()
                lines = pretty_data.split('\n')
                linesWithJpeg = []
                for line in lines:
                    #print(line)
                    if("https" in line and "image" in line):
                        #print(line.split("\"")[1])
                        try:
                            image_url = line.split("\"")[1]
                        except:
                            break

                        if "https" in image_url and "slideshare" not in image_url and "dobe" not in image_url and "almart" not in image_url and linesDone<150:
                            for file in os.listdir("./images"):
                                os.remove("./images/" + file)
                            linesDone+=1
                            try:
                                img_data = requests.get(image_url).content
                                with open("./images/"+query+ str(linesDone)+'.jpg', 'wb') as handler:
                                    handler.write(img_data)
                                    print(website)
                                    URLS_completed.append(website)                                    
                            except:
                                pass
                            try:
                                with open("./images/"+query+ str(linesDone)+'.jpg', 'r') as handler:
                                        try:
                                            text = handler.read()
                                            os.remove("./images/"+query+ str(linesDone)+'.jpg')
                                            print("removed" + query+ str(linesDone)+'.jpg')
                                        except:
                                            if(os.path.getsize("./images/"+ os.listdir("./images")[0]) > 100000 and Image.verify()):
                                                return
                            except:
                                pass