from fbchat import log, Client
from Crypto.Cipher import AES
from fbchat.models import *

import re
import time

pwd = input("Enter password: ")
client = Client("pranavmk98@gmail.com", pwd) # Replace with your login email
group = input("Enter group name: ")
thread_id = int(client.searchForGroups(group)[0].uid)
print("Found group")

me = 100018707857490 # Replace with your own Facebook ID


d = {'Pranav':[0, 0, 0]}
author = {me: 'Pranav'}
time = int(time.time() * 1000)
me_words = ["i", "my", "mine", "me", "im", "i'm", "i'll", "ill"]
you_words = ["u", "you", "ur", "your", "urs", "yours", "you're", "youre", "you'll", "youll", "ull", "u'll", "hbu", "wbu"]

num_batches = 10 # arbitrary - may have to adjust according to how many messages are in your convos

for count in range(num_batches):
    m = client.fetchThreadMessages(thread_id=thread_id, before=time-1, limit=10000)
    for i in m:
        if i.text:
            uid = i.author
            if int(uid) not in author:
                user_name = client.fetchUserInfo(uid)[uid].first_name
                d[user_name] = [0, 0, 0]
                author[int(uid)] = user_name
                print("Found user {}".format(user_name))
            time = int(i.timestamp)
            message = str(re.sub(r'[^\x00-\x7f]', r' ', str(i.text))).lower().split()
            if message:
                # print(message)
                for t in me_words:
                    d[author[int(uid)]][0] += message.count(t)
                for t in you_words:
                    d[author[int(uid)]][1] += message.count(t)
                d[author[int(uid)]][2] += 1
    print("Done with batch {}".format(count+1))


# All the I/You stats are commented out for group chats, because they're pretty meaningless
# (I guess the I stats could be useful but the You ones probably aren't)

for key in d:
    # print("Number of I's for {}: ".format(key), d[key][0])
    # print("Number of You's for {}: ".format(key), d[key][1])
    # print("I : You ratio for {}: ".format(key), d[key][0] * 1.0 /d[key][1])
    # print("Ratio of I to total for {}: ".format(key), d[key][0] * 1.0 /d[key][2])
    # print("Ratio of You to total for {}: ".format(key), d[key][1] * 1.0 /d[key][2])
    print("Total messages by {}: ".format(key), d[key][2])
    # print()

