# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import datetime

import ranking
import nicovideo_ranking as nico
import sougou_ranking as sougou
import you_next_ranking as nextr
import twitter as tw

app = Flask(__name__)

# Main
# Routing
@app.route('/')
def index():
    title = "Vtuberランキング！！"
    message = "ランキングを選んでください"
    return render_template('index.html',
                           message=message, title=title)

@app.route('/post', methods=['POST', 'GET'])
def post():
    time = datetime.datetime.today().strftime("%H:%M:%S")
    message = ""
    if request.method == 'POST':
        result = []
        if 'you_d' in request.form:
            title = "Vtuber-日間youtube動画ランキング！！"
            r = ranking.main("day")
            for i in range(10):
                result += ["{}位".format(i+1), r[i]]
        elif 'you_w' in request.form:
            title = "Vtuber週間youtube動画ランキング！！"
            r = ranking.main("week")
            for i in range(30):
                result += ["{}位".format(i+1), r[i]]
        elif 'you_m' in request.form:
            title = "Vtuber月間youtube動画ランキング！！"
            r = ranking.main("month")
            for i in range(30):
                result += ["{}位".format(i+1), r[i]]

        elif 'nico_w' in request.form:
            title = "Vtuber週間ニコニコ動画ランキング！！"
            r = nico.main("week")
            for i in range(30):
                result += ["{}位".format(i+1), r[i]]

        elif 'nico_m' in request.form:
            title = "Vtuber月間ニコニコ動画ランキング！！"
            r = nico.main("month")
            for i in range(30):
                result += ["{}位".format(i+1), r[i]]

        elif 'nico_3m' in request.form:
            title = "Vtuber四半期ニコニコ動画ランキング！！"
            r = nico.main("3m")
            for i in range(30):
                result += ["{}位".format(i+1), r[i]]

        elif 'sou_w' in request.form:
            title = "Vtuber週間総合動画ランキング！！"
            r = sougou.main("week")
            for i in range(30):
                t = r[i][0] + ", " + str(r[i][1]) + "ポイント"
                result += ["{}位".format(i+1), t]

        elif 'sou_m' in request.form:
            title = "Vtuber月間総合動画ランキング！！"
            r = sougou.main("month")
            for i in range(30):
                t = r[i][0] + ", " + str(r[i][1]) + "ポイント"
                result += ["{}位".format(i+1), t]

        elif 'next_w' in request.form:
            title = "次世代Vtuber週間youtube動画ランキング！！"
            r = nextr.main("week")
            for i in range(30):
                result += ["{}位".format(i+1), r[i]]
        elif 'next_m' in request.form:
            title = "次世代Vtuber月間youtube動画ランキング！！"
            r = nextr.main("month")
            for i in range(30):
                result += ["{}位".format(i+1), r[i]]

        elif 'tw' in request.form:
            title = "twitter活発度ランキング！！"
            r = tw.main()
            for i in range(30):
                t = r[i][0] + ", " + str(int(r[i][1])) + "ポイント"
                result += ["{}位".format(i+1), t]

        return render_template('index.html',
                               result=result, title=title,
                               time=time)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
