import datetime
import urllib.request as req
import bs4
import mysql.connector
import redis
import time

class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def get(self, value):
        return self.redis_client.get(value)

    def set(self, key,vaule, expire_time):
        self.redis_client.setex(key,expire_time,vaule)
        
    def keys(self,pattern="*"):
        return self.redis_client.scan_iter(match=pattern)
    
cache = RedisCache()

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Passw0rd!',
    database='git_action'
)

cursor = conn.cursor()

def insert_data(title, timestamp):
    cursor.execute('INSERT INTO my_table (title, timestamp) VALUES (%s, %s)', (title, timestamp))
    conn.commit()

def getData(url):
    request=req.Request(url, headers={
        "cookie":"over18=1",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    })
    
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")

    root=bs4.BeautifulSoup(data,"html.parser")
    titles=root.find_all("div",class_="title")
    for title in titles:
        if title.a != None:
            title_string = title.a.string
            current_time = datetime.datetime.now()
            name = cache.get(title_string)
            if name:
                name = name.decode('utf-8')
                if name == title_string:
                    pass
                else:
                    print(f"title:{title_string},time:{current_time}")
                    insert_data(title_string, current_time)
            else:
                print(f"title:{title_string},time:{current_time}")
                insert_data(title_string, current_time)
        cache.set(title_string,title_string,4200) #存進redis內進行比對，資料是否有重複
    nextLink=root.find("a", string="‹ 上頁")
    return nextLink["href"]


pageURL="https://www.ptt.cc/bbs/movie/index.html"
count=0
getData(pageURL)
while count<2:
    pageURL="https://www.ptt.cc"+getData(pageURL)
    count+=1
conn.close()