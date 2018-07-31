#!/usr/bin/python

import datetime
from operator import itemgetter

import apiclient.discovery
import apiclient.errors
from googleapiclient.discovery import build
from oauth2client.tools import argparser
import urllib.request
import json
from collections import OrderedDict
import pprint

AIM = "a"

def nico_search(qu, time, con, view):
    qu = qu.replace("\n", "")
    q = urllib.parse.quote_plus(qu, encoding='utf-8')
    u =  urllib.request.urlopen('http://api.search.nicovideo.jp/api/v2/video/contents/search?q='+q+'&targets=tags&fields=contentId,title,viewCounter,startTime&filters[startTime][gte]='+time+'&_sort=-viewCounter&_offset=0&_limit=20&_context=apiguide')
    t = u.read()
    e = json.loads(t)
    youso = []
    count = 0

    for i in e["data"]:
        count += int(i["viewCounter"])
        if i["contentId"] not in con:
            youso.append([qu, i["title"], i["contentId"], int(i["viewCounter"]), i["startTime"]])
            con.append(i["contentId"])
    view.append(count)
    u.close()
    return youso, view

def main(aim):
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    now_list = now.split("-")
    today = datetime.date.today()

    if aim == "week":
        time = today - datetime.timedelta(days = 7)
    elif aim == "month":
        time = today - datetime.timedelta(days = 30)
    else:
        time = today - datetime.timedelta(days = 90)

    time_list = (time.strftime('%Y/%m/%d')).split("/")
    time_aim = time_list[0] + "-" + time_list[1] + "-" + time_list[2] + "T" + now_list[3] + ":" +now_list[4]

    with open('nicotag.txt', 'r') as fr:
        data = fr.readlines()
        record_list = []
        con = []
        view = []
        for q in data:
            record, view = nico_search(q, time_aim, con, view)
            record_list+=record
            #print(q)
        record_list.sort(key=itemgetter(3), reverse=True)
        #print(view)
        return record_list

if __name__ == "__main__":
    a = main(AIM)
    for i in range(10):
        print(i+1, a[i])
