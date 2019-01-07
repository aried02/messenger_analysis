from fbchat import log, Client
from fbchat.models import *

import re
import time

pwd = input("Password: ")
client = Client("pranavmk98@gmail.com", pwd) # Replace with your Facebook login email
person = input("Person name: ")
thread_id = int(client.searchForUsers(person)[0].uid)
person = client.searchForUsers(person)[0].first_name
me = 100018707857490 # Replace with your own Facebook ID


d = {'Pranav':[0, 0, 0], person:[0, 0, 0]}
author = {thread_id: person, me: 'Pranav'}
time = int(time.time() * 1000)
me_words = ["i", "my", "mine", "me", "im", "i'm", "i'll", "ill"]
you_words = ["u", "you", "ur", "your", "urs", "yours", "you're", "youre", "you'll", "youll", "ull", "u'll", "hbu", "wbu"]

num_batches = 10 # arbitrary - may have to adjust according to how many messages are in your convos

for count in range(num_batches):
    m = client.fetchThreadMessages(thread_id=thread_id, before=time-1, limit=10000)
    for i in m:
        if i.text:
            time = int(i.timestamp)
            message = str(re.sub(r'[^\x00-\x7f]', r' ', str(i.text))).lower().split()
            if message:
                for t in me_words:
                    d[author[int(i.author)]][0] += message.count(t)
                for t in you_words:
                    d[author[int(i.author)]][1] += message.count(t)
                d[author[int(i.author)]][2] += 1
    print("Done with batch {}".format(count+1))

for key in d:
    print("Number of I's for {}: ".format(key), d[key][0])
    print("Number of You's for {}: ".format(key), d[key][1])
    print("I : You ratio for {}: ".format(key), d[key][0] * 1.0 /d[key][1])
    print("Ratio of I to total for {}: ".format(key), d[key][0] * 1.0 /d[key][2])
    print("Ratio of You to total for {}: ".format(key), d[key][1] * 1.0 /d[key][2])
    print("Total messages by {}: ".format(key), d[key][2])
    print()

pa, pb = tuple(d.keys())
print("Total references to {}: ".format(pa), d[pa][0] + d[pb][1])
print("Total references to {}: ".format(pb), d[pb][0] + d[pa][1])
