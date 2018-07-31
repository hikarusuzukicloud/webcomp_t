#!/usr/bin/python

import datetime
from operator import itemgetter

import apiclient.discovery
import apiclient.errors
from googleapiclient.discovery import build
from oauth2client.tools import argparser

DEVELOPER_KEY = "" 
YOUTUBE_API_SERVICE_NAME = "youtube" 
YOUTUBE_API_VERSION = "v3" 
AIM = "week"

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
    record = []
    for video_result in video_response.get('items', []):
        record.append((video_result["snippet"]["channelTitle"], 
                        video_result["snippet"]["publishedAt"],
                        video_result["snippet"]["title"],
                        int(video_result["statistics"]["viewCount"])))
    return record

def main(aim):
    time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    time_list = time.split("-")
    time_now = time_list[0] + "-" + time_list[1] + "-" + time_list[2] + "T" + time_list[3] + ":" +time_list[4] + ":" + time_list[5] + "Z"
    today = datetime.date.today()

    if aim == "day":
        day = today - datetime.timedelta(days = 1)
        day_list = (day.strftime('%Y/%m/%d')).split("/")
        time_aim = day_list[0] + "-" + day_list[1] + "-" + day_list[2] + "T" + time_list[3] + ":" +time_list[4] + ":" + time_list[5] + "Z"

    elif aim == "week":
        week = today - datetime.timedelta(days = 7)
        week_list = (week.strftime('%Y/%m/%d')).split("/")
        time_aim = week_list[0] + "-" + week_list[1] + "-" + week_list[2] + "T" + time_list[3] + ":" +time_list[4] + ":" + time_list[5] + "Z"

    else:
        month = today - datetime.timedelta(days = 30)
        month_list = (month.strftime('%Y/%m/%d')).split("/")
        time_aim = month_list[0] + "-" + month_list[1] + "-" + month_list[2] + "T" + time_list[3] + ":" +time_list[4] + ":" + time_list[5] + "Z"

    with open('q_id_next.txt', 'r') as fr:
        data = fr.readlines()
        record_list = []
        for inf in data:
            inf_sp = inf.split(",")
            q = inf_sp[0]
            cid = inf_sp[1]
            record = youtube_search(q, cid, time_aim)
            record_list+=record

        record_list.sort(key=itemgetter(3), reverse=True)

        return record_list

if __name__ == "__main__":
    a = main(AIM)
    for i in range(20):
        print(i+1, a[i])

