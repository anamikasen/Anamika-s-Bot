import json
import requests
from credentials import *
import pprint
import time
pp = pprint.PrettyPrinter(indent=4)
# try:
#     from urllib.parse import urlparse
# except ImportError:
#      from urlparse import urlparse
import six.moves.urllib as urllib

url = "https://api.telegram.org/bot{}/".format(token)

def getUrl(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def getMe(url):
    URL = url+'getme'
    #response gives the response code. the content needs to be retrieved
    content = getUrl(URL)
    return content

def getJsonFromUrl(url):
    content = getUrl(url)
    data = json.loads(content)
    #return pp.pprint(data)
    return data

def getUpdates(offset=None):
    URL = url + 'getUpdates?timeout='
    if offset:
        URL += "&offset={}".format(offset)
    content = getJsonFromUrl(URL)
    return content

def getLastUpdateID(updates):
    updateIDs = []
    for update in updates["result"]:
        updateIDs.append(int(update["update_id"]))
    return max(updateIDs)

def getLastChatIDandText(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def sendMessage(text, chatid):
    text = urllib.parse.quote(text)
    URL = url + "sendMessage?text={}&chat_id={}".format(text, chatid)
    getUrl(URL)

def echoAll(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chatID = update["message"]["chat"]["id"]
            sendMessage(text, chatID)
        except Exception as e:
            print(e)

def main():
    lastUpdateID = None
    while True:
        updates = getUpdates(lastUpdateID)
        if len(updates["result"]) > 0:
            lastUpdateID = getLastUpdateID(updates) + 1
            echoAll(updates)
        time.sleep(0.5)



if __name__=='__main__':
    main()
