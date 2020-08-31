from sqlite3 import connect
from AnimeDataLoad import AnimeData
import os

class Watched:

    def WatchedListCreate(self):
        watched = connect('./database/watched.db')
        cur = watched.cursor()
        cur.execute('''
        CREATE TABLE WATCHED
        (ID INTEGER PRIMARY KEY,
        TITLE TEXT NOT NULL)
        ''')
        watched.commit()
        watched.close()

    def WatchedExist(self, info_title):
        watched = connect('./database/watched.db')
        cur = watched.cursor()
        infos = cur.execute('''
        SELECT TITLE FROM WATCHED WHERE TITLE LIKE '%s'
        ''' % info_title)
        res = ((info_title,) in infos)
        watched.commit()
        watched.close()
        return res

    def WatchedInsert(self,info_dict):
        if self.WatchedExist(info_dict['title']):
            print('番剧已存在.')
            return False
        watched = connect('./database/watched.db')
        cur = watched.cursor()
        cur.execute('''
        INSERT INTO WATCHED (ID,TITLE)
        VALUES (NULL,'%s')
        ''' % info_dict['title'])
        watched.commit()
        watched.close()
        return True

    def WatchedShow(self):
        watched = connect('./database/watched.db')
        cur = watched.cursor()
        infos = cur.execute('''
        SELECT ID,TITLE from WATCHED
        ''')
        for info in infos:
            print(info)
        watched.commit()
        watched.close()

    def WatchedDelete(self,info_title):
        if not self.WatchedExist(info_title):
            print('番剧不存在')
            return False
        watched = connect('./database/watched.db')
        cur = watched.cursor()
        cur.execute('''
        DELETE FROM WATCHED WHERE TITLE LIKE '%s'
        ''' % info_title)
        watched.commit()
        watched.close()
        return True

    def WatchedInAnime(self):
        watched = connect('./database/watched.db')
        anime = AnimeData()
        cur_watched = watched.cursor()
        title_list = cur_watched.execute('''
        SELECT TITLE FROM WATCHED
        ''')
        titles = []
        for title in title_list:
            titles.append(title[0])
        watched.commit()
        watched.close()
        return titles

if __name__ == '__main__':
    watched = Watched()
    if not os.path.exists('./database/watched.db'):
        watched.WatchedListCreate()
    _info_dict_ = {
        'title': '轻音少女 第一季'
    }
    #watched.WatchedInsert(_info_dict_)
    #watched.WatchedShow()
    #watched.WatchedInAnime()