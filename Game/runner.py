from os import system
from threading import Thread
from time import sleep
while True:
    print("starting runner")
    try:
        webscraper_runner = Thread(target = system, args = ("python3 webscraper.py"))
        webscraper_runner.start()
        sleep(5)
    except:
        pass
    print("ending runner")