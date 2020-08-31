from sqlite3 import connect
from random import randint
import os

class Recommend:

    def RecommendCreate(self):
        recommend = connect('./database/recommend.db')
        cur = recommend.cursor()
        cur.execute('''
        CREATE TABLE RECOMMEND
        (ID INTEGER PRIMARY KEY,
        TAG TEXT NOT NULL,
        COUNT INT DEFAULT(1))
        ''')
        recommend.commit()
        recommend.close()

    def RecommendExist(self,info_tag):
        recommend = connect('./database/recommend.db')
        cur = recommend.cursor()
        tags = cur.execute('''
        SELECT TAG FROM RECOMMEND WHERE TAG LIKE '%s'
        ''' % info_tag)
        res = ((info_tag,) in tags)
        recommend.commit()
        recommend.close()
        return res

    def RecommendUpdate(self,info_tag):
        recommend = connect('./database/recommend.db')
        cur = recommend.cursor()
        if self.RecommendExist(info_tag) == True:
            cur.execute('''
            UPDATE RECOMMEND SET COUNT = COUNT + 1 WHERE TAG LIKE '%s'
            ''' % info_tag)
        else:
            cur.execute('''
            INSERT INTO RECOMMEND (ID, TAG)
            VALUES (NULL, '%s')
            ''' % info_tag)
        recommend.commit()
        recommend.close()

    def RecommendShow(self):
        recommend = connect('./database/recommend.db')
        cur = recommend.cursor()
        tag_list = cur.execute('''
        SELECT ID, TAG, COUNT FROM RECOMMEND
        ''')
        for tag in tag_list:
            print(tag)
        recommend.commit()
        recommend.close()

    def RecommendClear(self):
        recommend = connect('./database/recommend.db')
        cur = recommend.cursor()
        cur.execute('''
        UPDATE RECOMMEND SET COUNT = 0 
        ''')
        recommend.commit()
        recommend.close()

    def RecommendTag(self):
        recommend = connect('./database/recommend.db')
        cur = recommend.cursor()
        info_sum = cur.execute('''
        SELECT SUM(COUNT) AS SUM_COUNT FROM RECOMMEND
        ''')
        for sums in info_sum:
            sum_count = sums[0]
        tag_random = randint(1,sum_count-1)
        tag_list = cur.execute('''
        SELECT TAG, COUNT FROM RECOMMEND ORDER BY COUNT DESC
        ''')
        tag_flag = ''
        for tag in tag_list:
            if tag_random - tag[1] > 0:
                tag_random -= tag[1]
            else:
                tag_flag = tag[0]
        recommend.commit()
        recommend.close()
        return tag_flag

    def RecommendAnime(self):
        tag = self.RecommendTag()
        #print(tag)
        dbsql = connect('./database/anime.db')
        cur = dbsql.cursor()
        anime_list = cur.execute('''
        SELECT TITLE FROM ANIME WHERE TAG LIKE '%%%s%%'
        ''' % tag)
        count = 0
        animes = []
        for anime in anime_list:
            animes.append(anime)
            count += 1
        anime_random = randint(0,count-1)
        res_anime = animes[anime_random][0]
        dbsql.commit()
        dbsql.close()
        return res_anime

if __name__ == '__main__':
    recommend = Recommend()
    if not os.path.exists('./database/recommend.db'):
        recommend.RecommendCreate()
    #recommend.RecommendUpdate('漫画改')
    recommend.RecommendAnime()
    recommend.RecommendShow()