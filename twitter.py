import tweepy
from datetime import datetime
from operator import itemgetter
import time
import calendar
import json
import sys

def timechange(day):
    time_utc = time.strptime(day, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    s = time.strftime("%Y:%m:%d:%H:%M:%S", time_local)
    sp = s.split(":")
    reday = datetime(int(sp[0]),int(sp[1]),int(sp[2]),int(sp[3]),int(sp[4]),int(sp[5]))

    return reday

def get_twitter(tid, now):
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    ACCESS_TOKEN = ''
    ACCESS_SECRET = ''

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)

    user = api.get_user(tid)
    count = int(user._json['statuses_count'])
    day = timechange(user._json['created_at'])
    katu = (now - day).days
    return count / int(katu)
 

def main():
    with open("id_twitter.txt", "r") as f:
        data = f.readlines()
        now = datetime.now()
        record = []
        for inf in data:
            inf_sp = inf.split(",")
            r = get_twitter(inf_sp[0], now)
            record.append([inf_sp[1],r])

        record.sort(key=itemgetter(1), reverse=True)
    return record
        
if __name__ == "__main__":
    a = main()
    for i in range(20):
        print(i+1, a[i])
