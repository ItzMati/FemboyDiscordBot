import requests
import json
from pprint import pprint
import sys
import requests
import random

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
sub=''
waba = 0
imagelist= []


client_id = 'uHaDpx5N5mQ-IpXQ3W-fkw'
secret_key = 'x8AyniGBIGSPXKUsIVxnmFRdnWZWlg'

auth = requests.auth.HTTPBasicAuth(client_id, secret_key)
    
data = {
    'grant_type': 'password',
    'username': 'glubstergluber',
    'password': 'haslomati1234'
    }

headers = {'User-Agent': 'MyAPI/0.0.1'}


res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)
res.json()

token=res.json()['access_token']

headers['Authorization'] = f'bearer {token}'

def function(feed, subreddit):
    global waba
    global sub
    global imagelist

    sub=subreddit
    
    print("imagegetter."+sub)
    
    link= 'https://oauth.reddit.com/r/'+sub+'/'+feed
    
    print("imagegetter."+link)

    bruh = requests.get(link, headers=headers)
    
    for post in bruh.json()['data']['children']:
        idk = (str(post['data']['url']).translate(non_bmp_map))
        if 'comments' in idk:
            waba +=1
        else:
            imagelist.append(idk)


    for i in range(1):
        item = random.choice(imagelist)
        img_data = requests.get(item).content
        with open('image_name'+str(i)+'.jpg', 'wb') as handler:
            handler.write(img_data)

    sub=''
    imagelist=[]

#function("top", "femboy")
