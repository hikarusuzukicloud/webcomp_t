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

DEVELOPER_KEY = "" 
YOUTUBE_API_SERVICE_NAME = "youtube" 
YOUTUBE_API_VERSION = "v3" 
AIM = "month"

def youtube_search(q, cid, time):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
      developerKey=DEVELOPER_KEY)
    
    search_response = youtube.search().list(
      q=q,
      part="id,snippet",
      maxResults=30,
      publishedAfter = time
    ).execute()

    videos = []
    search_id = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video" and search_result["snippet"]["channelId"] == cid:
            search_id.append(search_result["id"]["videoId"])
  
    video_ids = ','.join(search_id)

    video_response = youtube.videos().list(
        id=video_ids,
        part='snippet, statistics'
    ).execute()
    count = 0
    for video_result in video_response.get('items', []):
        count += int(video_result["statistics"]["viewCount"])

    return count


def nico_search(qu, time):
    qu = qu.replace("\n", "")
    q = urllib.parse.quote_plus(qu, encoding='utf-8')
    u =  urllib.request.urlopen('http://api.search.nicovideo.jp/api/v2/video/contents/search?q='+q+'&targets=tags&fields=contentId,title,viewCounter,startTime&filters[startTime][gte]='+time+'&_sort=-viewCounter&_offset=0&_limit=20&_context=apiguide')
    t = u.read()
    e = json.loads(t)
    count = 0

    for i in e["data"]:
        count += int(i["viewCounter"])

    u.close()
    return count



def main(aim):
    time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    time_list = time.split("-")
    today = datetime.date.today()

    if aim == "week":
        week = today - datetime.timedelta(days = 7)
        week_list = (week.strftime('%Y/%m/%d')).split("/")
        time_aim = week_list[0] + "-" + week_list[1] + "-" + week_list[2] + "T" + time_list[3] + ":" +time_list[4] + ":" + time_list[5] + "Z"

    else:
        month = today - datetime.timedelta(days = 30)
        month_list = (month.strftime('%Y/%m/%d')).split("/")
        time_aim = month_list[0] + "-" + month_list[1] + "-" + month_list[2] + "T" + time_list[3] + ":" +time_list[4] + ":" + time_list[5] + "Z"

    count_list = [0 for i in range(32)]

    with open('q_id.txt', 'r') as fy:
        data = fy.readlines()
        for i in range(32):
            inf = data[i]
            inf_sp = inf.split(",")
            q = inf_sp[0]
            cid = inf_sp[1]
            count = youtube_search(q, cid, time_aim)
            count_list[i] += count

    rank_list = []
    with open('nicotag.txt', 'r') as fn:
        data = fn.readlines()
        for i in range(32):
            q = data[i]
            count = nico_search(q, time_aim)
            count_list[i] += count * 2
            q = q.replace("\n", "")
            rank_list.append([q, count_list[i]])


        rank_list.sort(key=itemgetter(1), reverse=True)
    return rank_list



if __name__ == "__main__":
    a = main(AIM)
    for i in range(10):
        print(a[i])
