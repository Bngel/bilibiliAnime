from bs4 import BeautifulSoup
import requests
from sqlite3 import connect

class Version:
    base_url = 'https://github.com/Bngel/bilibiliAnime/blob/master/README.md'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }

    def __init__(self):
        dbsql = connect('./database/anime.db')
        cur = dbsql.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS VERSION
        (ID INTEGER PRIMARY KEY,
        VER TEXT NOT NULL,
        LINK TEXT NOT NULL);
        ''')
        ver = cur.execute('''
        SELECT VER, LINK FROM VERSION WHERE ID LIKE (SELECT MAX(ID) FROM VERSION)
        ''')
        for v in ver:
            self.cur_version = v[0]
            self.cur_link = v[1]

    def get_url(self):
        response = requests.get(self.base_url,headers=self.headers).text
        soup = BeautifulSoup(response,'lxml')
        return soup

    def get_version(self):
        soup = self.get_url()
        data_text = soup.find('article',{'class','markdown-body entry-content container-lg'}).find_all('p')
        version = data_text[1].text
        download_link = data_text[2].find('a').get('href')
        return version,download_link

    def judge_version(self):
        version,link = self.get_version()
        if version != self.cur_version:
            print('数据库版本已过期,请自行下载新数据库.')
            self.cur_link = link
            return False
        else:
            print('数据库为最新版本,无需更新')
            return True

    def DefaultInsert(self):
        dbsql = connect('./database/anime.db')
        cur = dbsql.cursor()
        cur.execute('''
        INSERT INTO VERSION (ID,VER,LINK)
        VALUES (NULL,'Anime Version:1.0','https://1drv.ms/u/s!AqWuZaQC1dE6hg8QEzEA0apK87M0?e=6YsLFh')
        ''')
        dbsql.commit()
        dbsql.close()

if __name__ == '__main__':
    version = Version()
    version.judge_version()