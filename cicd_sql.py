from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup as bs
import requests as req
import mysql.connector

def get_sql_connect():
    conn = mysql.connector.connect(
        host='35.201.205.128',
        user='root',
        password='d]a)Qf8=moJ"YiOU',
        database = 'gitaction',
    )
    return conn

def check_data(cursor,title):
    cursor.execute("SELECT * FROM test WHERE title = %s",(title,))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False
    
def insert_data(conn,cursor,title, timestamp):
    cursor.execute('INSERT INTO test (title, timestamp) VALUES (%s, %s)', (title, timestamp))
    conn.commit()
    
def update_data(conn,cursor,title, timestamp):
    cursor.execute('UPDATE test SET timestamp = %s WHERE title = %s', (timestamp, title))
    conn.commit()

def convert_utc_to_taiwan(utc_time):
    taiwan_timezone = timezone(timedelta(hours=8))
    return utc_time.astimezone(taiwan_timezone)

def getData(url):
    conn = get_sql_connect()
    cursor = conn.cursor()
    request=req.get(url, headers={
        "cookie":"over18=1",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    })
    root=bs(request.text,"html.parser")
    titles=root.find_all("div",class_="title")
    for title in titles:
        if title.a != None:
            title_string = title.a.string
            current_time = convert_utc_to_taiwan(datetime.now())
            if check_data(cursor,title_string):
                update_data(conn,cursor,title_string, current_time)
            else:
                insert_data(conn,cursor,title_string, current_time)
    nextLink=root.find("a", string="‹ 上頁")
    conn.close()
    return nextLink["href"]


pageURL="https://www.ptt.cc/bbs/movie/index.html"
count=0
getData(pageURL)
while count<2:
    pageURL="https://www.ptt.cc"+getData(pageURL)
    count+=1
