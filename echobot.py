
# coding: utf-8

# In[80]:


# As usual - IMPORTS
import json
import requests
from credentials import * 
import pprint
import time
pp = pprint.PrettyPrinter(indent=4)
import urllib


# In[56]:


url = "https://api.telegram.org/bot{}/".format(token)


# In[57]:


def getUrl(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


# In[58]:


def getMe(url):
    URL = url+'getme'
    #response gives the response code. the content needs to be retrieved
    content = getUrl(URL)
    return content


# In[97]:


def getJsonFromUrl(url):
    content = getUrl(url)
    data = json.loads(content)
    #return pp.pprint(data)
    return data


# In[94]:


def getUpdates(offset=None):
    URL = url + 'getUpdates?timeout=100'
    if offset:
        URL += '&=offset={}'.format(offset)
    content = getJsonFromUrl(URL)
    return content

def getLastUpdateID(updates):
    update_ids = []
    for update in updates['result']:
        update_ids.append(int(update['update_id']))
    return max(update_ids)


# In[89]:


def getChatIDandText(updates):
    num_updates = len(updates['result'])
    last_update = num_updates - 1
    text = updates['result'][last_update]['message']['text']
    chat_id = updates['result'][last_update]['message']['chat']['id']
    return(text, chat_id)


# In[91]:


def send_message(text, chat_id):
    text = urllib.quote_plus(text)
    URL = url + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    getUrl(URL)



def echoAll(updates):
    for update in updates['result']:
        try:
            text = update['message']['text']
            ID = update['message']['chat']['id']
            send_message(text, ID)
        except Exception as e:
            print(e)


def main():
    # lastTextID = (None, None)
    # while True:
    #     text, id = getChatIDandText(getUpdates())
    #     if(text, id)!=lastTextID:
    #         send_message(text, id)
    #         lastTextID = (text, id)
    #     time.sleep(0.5)
    lastUpdateID = None
    while True:
        print('dafuq')
        updates = getUpdates(lastUpdateID)
        if len(updates['result']) > 0:
            lastUpdateID = getLastUpdateID(updates)+1
            echoAll(updates)

        time.sleep(0.5)


if __name__ == '__main__':
    main()



