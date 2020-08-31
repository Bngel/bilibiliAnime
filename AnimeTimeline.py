import requests
import json

class TimeLine:

    def get_url(self):
        url = 'https://bangumi.bilibili.com/web_api/timeline_global'
        response = requests.get(url).text
        timeline = json.loads(response)
        return timeline

    def get_today_anime(self):
        timeline = self.get_url()
        today = {}
        for time in timeline['result']:
            if time['is_today'] == 1:
                today = time
                break
        #print(today)
        anime_titles = []
        for anime in today['seasons']:
            anime_titles.append(anime['pub_time'] + ' ' + anime['title'] + ' ' + anime['pub_index'])
        return anime_titles

    def get_week_anime(self):
        timeline = self.get_url()
        this_week = False
        week_animes = []
        for time in timeline['result']:
            if time['is_today'] == 1:
                this_week = True
            if this_week:
                week_animes.append(time)
        return week_animes

if __name__ == '__main__':
    bili = TimeLine()
    bili.get_week_anime()