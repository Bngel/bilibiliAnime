import requests
from bs4 import BeautifulSoup
import json
import time
from ipSpider import ipSpider
import random
import os

cookie = {
    "cookie" : "_uuid=4707015A-6239-E2B5-1105-A7EC0490724E61173infoc; LIVE_BUVID=AUTO7215653620642257; sid=b7h3xr9a; CURRENT_FNVAL=16; stardustvideo=1; rpdid=|(u))kJkJ)m~0J'ulYlR)~|l); im_notify_type_4994557=0; fts=1565960360; im_seqno_4994557=1864; im_local_unread_4994557=0; LIVE_PLAYER_TYPE=2; DedeUserID=4994557; DedeUserID__ckMd5=3aab3cf3c49c42ea; buvid3=05D51662-8C76-4D40-8204-3512F65F4851155805infoc; CURRENT_QUALITY=120; SESSDATA=24d541a1%2C1609984517%2C492bb*71; bili_jct=78b0e1b040b22abd8bf075537194b49d; bp_t_offset_4994557=411369115756191650; bp_video_offset_4994557=411389362234201844"
}

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                 '78.0.3904.97 Safari/537.36'
}

class Anime:
    def __init__(self,url,proxies,page):
        self.base_url = url
        self.proxies = proxies
        self.params = {
        'season_version': -1,
        'area': -1,
        'is_finish': -1,
        'copyright': -1,
        'season_status': -1,
        'season_month': -1,
        'year': -1,
        'style_id': -1,
        'order': 3,
        'st': 1,
        'sort': 0,
        'page': page,
        'season_type': 1,
        'pagesize': 20,
        'type': 1
        }
        self.page = page

    def get_data(self):
        try:
            url = self.base_url
            response = requests.get(url,headers=headers,params=self.params,proxies=self.proxies).text
            data = json.loads(response)
            return data['data']['has_next'],data['data']['list']
        except Exception:
            print(response)
            return -1,None

    def get_url(self,url):
        try:
            response = requests.get(url, headers=headers,proxies=self.proxies)
            soup = BeautifulSoup(response.text, 'lxml')
            target = soup.find('div', {'class', 'media-right'}).find('a').get('href')
            target_url = 'https:' + target
            target_html = requests.get(target_url,  headers=headers,proxies=self.proxies).text
            soup = BeautifulSoup(target_html, 'lxml')
            return soup
        except AttributeError:
            print('url Error')


    def get_tags(self,url):
        soup = self.get_url(url)
        tag_list = soup.find('span',{'class','media-tags'}).find_all('span',{'class','media-tag'})
        tags = []
        for tag in tag_list:
            tags.append(tag.text)
        return tags

    def get_times(self,url):
        soup = self.get_url(url)
        time = soup.find('div',{'class','media-info-time'}).find_all('span')
        times = []
        for t in time:
            times.append(t.text)
        return times

    def get_intro(self,url):
        response = requests.get(url,  headers=headers,proxies=self.proxies)
        soup = BeautifulSoup(response.text, 'lxml')
        intro = soup.find('span',{'class','absolute'}).get_text()
        return intro

    def get_order(self, url):
        soup = self.get_url(url)
        order = soup.find('span', {'class', 'media-info-count-item media-info-count-item-fans'}).find('em').text
        return order

    def url_parser(self):
        if os.path.exists('./data/data_'+str(self.page)+'.json'):
            print(str(self.page)+' has inited')
            return 1
        else:
            flag,data = self.get_data()
            if flag == -1:
                return 0
            for anime in data:
                    p_url = anime['link']
                    try:
                        tags = self.get_tags(p_url)
                    except AttributeError as e:
                        anime['tags']=[]
                    else:
                        anime['tags']=tags
                    try:
                        times = self.get_times(p_url)
                    except AttributeError as e:
                        pass
                    else:
                        anime['index_show']=times
                    try:
                        intro = self.get_intro(p_url)
                    except AttributeError as e:
                        anime['intro']=''
                    else:
                        anime['intro']=intro
                    try:
                        order = self.get_order(p_url)
                    except AttributeError as e:
                        anime['order']= ''
                    else:
                        anime['order']= order
            if not os.path.exists('./data'):
                os.makedirs('./data')
            with open('./data/data_'+str(self.page)+'.json','w+') as db:
                db.write(json.dumps(data))
            return flag

if __name__ == '__main__':
    ip = ipSpider()
    ips = ip.get_ips()
    page = 158
    while True:
        try:
            proxies = ips[random.randint(0, len(ips) - 1)]
        except ValueError as ve:
            ips = ip.get_ips()
            continue
        print(proxies)
        url = 'https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page=' \
              + str(page) + '&season_type=1&pagesize=20&type=1'
        try:
            anime = Anime(url,proxies,page)
            end = anime.url_parser()
        except requests.exceptions.ProxyError as pxy:
            ips = ip.get_ips()
            continue
        print('page:%d ending' % page)
        page += 1
        if end == 0:
            break

    print('\nending')