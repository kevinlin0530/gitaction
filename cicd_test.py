import datetime
import requests as req
from bs4 import BeautifulSoup as bs
import mysql.connector
import redis
import time

class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis(host='0.0.0.0', port=6379, db=0)

    def get(self, value):
        return self.redis_client.get(value)

    def set(self, key,vaule, expire_time):
        self.redis_client.setex(key,expire_time,vaule)
        
    def keys(self,pattern="*"):
        return self.redis_client.scan_iter(match=pattern)
    
cache = RedisCache()

# def get_sql_connect():
#     conn = mysql.connector.connect(
#         host='35.201.205.128',
#         user='root',
#         password='d]a)Qf8=moJ"YiOU',
#         database = 'gitaction',
#     )
#     return conn

def insert_data(conn,cursor,title, timestamp):
    cursor.execute('INSERT INTO test (title, timestamp) VALUES (%s, %s)', (title, timestamp))
    conn.commit()

def getData(url):
    # conn = get_sql_connect()
    # cursor = conn.cursor()
    request=req.get(url, headers={
        "cookie":"over18=1",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    })
    
    root=bs(request.text,"html.parser")
    titles=root.find_all("div",class_="title")
    for title in titles:
        if title.a != None:
            title_string = title.a.string
            current_time = datetime.datetime.now()
            name = cache.get(title_string)
            if name:
                name = name.decode('utf-8')
                pass
            else:
                print(f"title:{title_string},time:{current_time}")
                # insert_data(conn,cursor,title_string, current_time)
            cache.set(title_string,title_string,4200) #存進redis內進行比對，資料是否有重複
    nextLink=root.find("a", string="‹ 上頁")
    # conn.close()
    if nextLink["href"]:
        return nextLink["href"]
    else:
        return None

pageURL="https://www.ptt.cc/bbs/movie/index.html"
count=0
getData(pageURL)
while count<2:
    pageURL="https://www.ptt.cc"+getData(pageURL)
    count+=1