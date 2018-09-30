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
from dbhelper import DBHelper

db = DBHelper()
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


def sendMessage(text, chatid, replyMarkup=None):
    text = urllib.parse.quote(text)
    URL = url + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chatid)
    if replyMarkup:
        URL += "&reply_markup={}".format(replyMarkup)
    getUrl(URL)

def handleUpdates(updates):
    for update in updates['result']:
        text = update['message']['text']
        ID = update['message']['chat']['id']
        items = db.getItems(ID)
        if text == "/done":
            keyboard = buildKeyboard(items)
            sendMessage("Select an item to delete", ID, keyboard)
        elif text in items:
            db.deleteItem(text, ID)
            items = db.getItems(ID)
            keyboard = buildKeyboard(items)
            sendMessage("Select an item to delete", ID, keyboard)
        elif text == '/start':
            sendMessage("Welcome to your Personal To Do List Manager", ID)
        elif text.startswith("/"):
            continue
        else:
            db.addItem(text, ID)
            items = db.getItems(ID)
            message = "\n".join(item for item in items)
            sendMessage(message, ID)

def buildKeyboard(items):
    keyboard = [[item] for item in items]
    replyMarkup = {"keyboard":keyboard, "one_time_keyboard":True}
    return json.dumps(replyMarkup)


def main():
    db.setup()
    lastUpdateID = None
    while True:
        updates = getUpdates(lastUpdateID)
        if len(updates["result"]) > 0:
            lastUpdateID = getLastUpdateID(updates) + 1
            handleUpdates(updates)
        time.sleep(0.5)



if __name__=='__main__':
    main()
