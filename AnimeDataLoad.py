import json
import os
from sqlite3 import connect
from AnimeRecommend import Recommend

class AnimeData:
    Data = []

    def __init__(self):
        self.path = './data'

    def DataInit(self):
        page = 1
        file_name = '/data_'+str(page)+'.json'
        file_path = self.path + file_name
        while os.path.exists(file_path):
            with open(file_path,'r') as fp:
                self.Data.extend(json.load(fp))
            page += 1
            file_name = '/data_' + str(page) + '.json'
            file_path = self.path + file_name

    def DataPrint(self):
        dbsql = connect('./database/anime.db')
        cur = dbsql.cursor()
        cursor = cur.execute("SELECT TITLE, ORDER_TEXT, INTRO, INDEX_SHOW, TAG, VIP from ANIME")
        for row in cursor:
            if row[5] == 1:
                vip = 'TRUE'
            else:
                vip = 'FALSE'
            print('-----------Info------------')
            print('TITLE: %s' % row[0])
            print('ORDERS: %s' % row[1])
            print('Intro:')
            print(row[2])
            print('Index_show: [%s]' % row[3])
            print('Tags: [%s]' % row[4])
            print('VIP: [%s]' % vip)
            print('------------End------------\n')

    def SqliteTableCreate(self):
        dbsql = connect('./database/anime.db')
        cur = dbsql.cursor()
        cur.execute('''
            CREATE TABLE ANIME
            (ID INTEGER PRIMARY KEY,
            TITLE TEXT           NOT NULL,
            ORDERS FLOAT,
            ORDER_TEXT TEXT,
            INTRO TEXT           NOT NULL,
            INDEX_SHOW TEXT      NOT NULL,
            TAG TEXT             NOT NULL,
            VIP INT              NOT NULL,
            LINK TEXT            NOT NULL,
            COVER TEXT           NOT NULL,
            FINISH INT           NOT NULL);
            ''')
        dbsql.commit()
        dbsql.close()

    def SqliteInfoInsert(self):
        dbsql = connect('./database/anime.db')
        cur = dbsql.cursor()
        for dt in self.Data:
            tags = ''
            for tag in dt['tags']:
                tags += tag+' '
            tags = tags.strip()
            index_show = ''
            for index in dt['index_show']:
                index_show += index+' '
            index_show = index_show.strip()
            title = dt['title']
            title = title.replace("'","")
            intro = dt['intro']
            intro = intro.replace("'","")
            order_text = dt['order']
            if '万' in order_text:
                order = float(order_text[:-1])*10000
            elif order_text == '':
                order = float(0)
            else:
                order = float(order_text)
            vip_text = dt['badge']
            if vip_text == '':
                vip = 0
            else:
                vip = 1
            link = dt['link']
            cover = dt['cover']
            finish = dt['is_finish']
            sql_syn = '''
            INSERT INTO ANIME (ID,TITLE,ORDERS,ORDER_TEXT,INTRO,INDEX_SHOW,TAG,VIP,LINK,COVER,FINISH)
            VALUES (NULL, '%s', %f, '%s', '%s', '%s', '%s', %d, '%s', '%s', %d)
             ''' % (title, order,order_text, intro, index_show, tags, vip, link, cover, finish)
            cur.execute(sql_syn)
        dbsql.commit()
        dbsql.close()

    def SqliteInfoSelect(self):
        dbsql = connect('./database/anime.db')
        cur = dbsql.cursor()
        cursor = cur.execute("SELECT TITLE from ANIME")
        init_info = []
        for title in cursor:
            init_info.append(title)
        dbsql.commit()
        dbsql.close()
        return init_info

    def SqliteInfoSearch(self,dicts):
        if not dicts:
            return []
        dbsql = connect('./database/anime.db')
        cur = dbsql.cursor()
        flag = False
        tag_flag = False
        info_list = "SELECT TITLE, ORDER_TEXT, INTRO, INDEX_SHOW, TAG, VIP, COVER, LINK from ANIME where "
        tag_list = " "
        for type,info in dicts.items():
            if type.upper() == 'TITLE':
                if flag == False:
                    info_list += " TITLE LIKE '%%%s%%' " % info
                else:
                    info_list += " AND TITLE LIKE '%%%s%%' " % info
                flag = True
            elif type.upper() == 'INDEX_SHOW':
                if flag == False:
                    info_list += " INDEX_SHOW LIKE '%%%s%%' " % info
                else:
                    info_list += " AND INDEX_SHOW LIKE '%%%s%%' " % info
                flag = True
            elif type.upper() == 'TAG':
                for tag in info:
                    if tag_flag == False:
                        tag_list += " TAG LIKE '%%%s%%' " % tag
                        tag_flag = True
                    else:
                        tag_list += " OR TAG LIKE '%%%s%%'" % tag
                    recommend = Recommend()
                    recommend.RecommendUpdate(tag)
            elif type.upper() == 'ORDER':
                if flag == False:
                    info_list += " ORDERS >= %f " % info
                else:
                    info_list += " AND ORDERS >= %f " % info
                flag = True
            elif type.upper() == 'FINISH':
                if flag == False:
                    info_list += " FINISH LIKE %d " % info
                else:
                    info_list += " AND FINISH LIKE %d " % info
                flag = True
            elif type.upper() == 'VIP':
                if flag == False:
                    info_list += " VIP LIKE %d " % info
                else:
                    info_list += " AND VIP LIKE %d " % info
                flag = True
        if flag == True and tag_list != " ":
            tag_list = " AND (" + tag_list + ") "
        #print(info_list + tag_list)
        cursor = cur.execute(info_list+tag_list)
        infos = []
        for cur in cursor:
            infos.append(cur)
        dbsql.commit()
        dbsql.close()
        return infos

if __name__ == '__main__':
    Anime = AnimeData()
    Anime.DataInit()
    #print(Anime.Data)
    if not os.path.exists('./database/anime.db'):
        Anime.SqliteTableCreate()
        Anime.SqliteInfoInsert()
    #Anime.DataPrint()
    dicts = {
        'order': 5000000,
        'tag': ['恋爱','校园'],
        'vip': 1,
    }
    Anime.SqliteInfoSearch(dicts)
    #Anime.SqliteInfoSelect()