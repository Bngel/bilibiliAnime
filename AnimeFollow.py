from sqlite3 import connect
import os
from AnimeDataLoad import AnimeData

class Follow:

    def FollowCreate(self):
        follow = connect('./database/follow.db')
        cur = follow.cursor()
        cur.execute('''
        CREATE TABLE FOLLOW
        (ID INTEGER PRIMARY KEY,
        TITLE TEXT NOT NULL)
         ''')
        follow.commit()
        follow.close()

    def FollowExist(self,info_title):
        follow = connect('./database/follow.db')
        cur = follow.cursor()
        infos = cur.execute('''
        SELECT TITLE FROM FOLLOW WHERE TITLE LIKE '%s'
        ''' % info_title)
        res = ((info_title,) in infos)
        follow.commit()
        follow.close()
        return res

    def FollowInsert(self,info_dict):
        if self.FollowExist(info_dict['title']):
            print('番剧已存在.')
            return False
        follow = connect('./database/follow.db')
        cur = follow.cursor()
        cur.execute('''
        INSERT INTO FOLLOW (ID,TITLE)
        VALUES (NULL,'%s')
        ''' % info_dict['title'])
        follow.commit()
        follow.close()
        return True

    def FollowShow(self):
        follow = connect('./database/follow.db')
        cur = follow.cursor()
        infos = cur.execute('''
        SELECT ID,TITLE from FOLLOW
        ''')
        for info in infos:
            print(info)
        follow.commit()
        follow.close()

    def FollowDelete(self,info_title):
        if not self.FollowExist(info_title):
            print('番剧不存在.')
            return False
        follow = connect('./database/follow.db')
        cur = follow.cursor()
        cur.execute('''
        DELETE FROM FOLLOW WHERE TITLE LIKE '%s'
        ''' % info_title)
        follow.commit()
        follow.close()
        return True

    def FollowInAnime(self):
        follow = connect('./database/follow.db')
        anime = AnimeData()
        cur_follow = follow.cursor()
        title_list = cur_follow.execute('''
        SELECT TITLE FROM FOLLOW
        ''')
        titles = []
        for title in title_list:
            titles.append(title[0])
        follow.commit()
        follow.close()
        return titles

if __name__ == '__main__':
    follow = Follow()
    if not os.path.exists('./database/follow.db'):
        follow.FollowCreate()
    _info_test_ = {
        'title': '轻音少女 第一季'
    }
    #follow.FollowInsert(_info_test_)
    #follow.FollowDelete('鬼灭之刃')
    #follow.FollowShow()
    follow.FollowInAnime()
