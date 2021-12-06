import os
import copy
import sqlite3
from collections import Counter
from datetime import datetime, timedelta

#此文件用于卡片仓库的创建、连接、写入和读取
#可调用api如下：
#db.get_card_num(uid:int, cid:int) return int 查询某个uid拥有几张卡片id为cid的卡，返回卡片数量，最大为6
#db.add_card(uid:int, cid:int) return int 向数据库中uid = uid 的用户添加一张id为cid的卡，返回添加后的卡片数量，7为超出，实际不会存入
#db.get_cards_num(uid:int) return list 获取uid = uid 的用户的所有卡片和各卡片数量
#db.get_ranking(uid:int) return int 获取uid = uid 的用户的卡片数量加权排名 返回该排名，-1为数据库中无此用户


class CardRecordAS:
    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._create_table()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self.connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS card_record"
                "(uid INT NOT NULL, cid INT NOT NULL, num INT NOT NULL, PRIMARY KEY(uid, cid))"
            )

    def get_card_num(self, uid, cid):
        with self.connect() as conn:
            r = conn.execute(
                "SELECT num FROM card_record WHERE uid=? AND cid=?", (uid, cid)
            ).fetchone()
            return r[0] if r else 0


    def add_card(self, uid, cid):
        num = self.get_card_num(uid, cid)
        if num <= 5:
            num += 1
            with self.connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO card_record (uid, cid, num) VALUES (?, ?, ?)",
                    (uid, cid, num),
                )
            return num
        else:
            return 7

    def get_cards_num(self, uid):
        with self.connect() as conn:
            r = conn.execute(
                "SELECT cid, num FROM card_record WHERE uid=? AND num>0", (uid,)
            ).fetchall()
            
        return {c[0]: c[1] for c in r} if r else {}


    def get_ranking(self, uid):
        with self.connect() as conn:
            user_list = conn.execute(   #获取目前有哪些用户创建了仓库
                "SELECT uid FROM card_record WHERE num>0", ()
            ).fetchall()
            r = conn.execute(  #获取所有用户的R卡
                "SELECT uid FROM card_record WHERE cid < 2000000 AND num>0", ()
            ).fetchall()
            sr = conn.execute(  #获取所有用户的SR卡
                "SELECT uid FROM card_record WHERE cid > 2000000 AND cid < 3000000 AND num>0", ()
            ).fetchall()
            ur = conn.execute(  #获取所有用户的UR卡
                "SELECT uid FROM card_record WHERE cid > 3000000 AND num>0", ()
            ).fetchall()
        if not r and not sr and not ur:
            return -1
        r_num = Counter([s[0] for s in r])
        sr_num = Counter([s[0] for s in sr])
        ur_num = Counter([s[0] for s in ur])
        point = Counter([s[0] for s in user_list])
        for key in point.keys(): #计算卡片权重 可以改为更为复杂的算法
            try:
                point[key] = r_num[key] 
            except:
                point[key] = 0
            try:
                point[key] += sr_num[key] * 5 
            except:
                point[key] += 0
            try:
                point[key] += ur_num[key] * 25
            except:
                point[key] += 0
        if uid not in point:
            return -1
        user_card_num = point[uid]
        return sum(n > user_card_num for n in point.values()) + 1



DB_PATH = os.path.expanduser("~/.hoshino/asgacha.db")
db = CardRecordAS(DB_PATH)

