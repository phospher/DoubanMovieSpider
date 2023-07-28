#!/usr/bin/python3

import sys
from urllib import request
from parser import DoubanMovieParser
import logging
import sqlite3
import datetime


def check_python_version():
    if sys.version_info.major < 3:
        raise Exception('Must be using Python 3')


def init_db():
    with sqlite3.connect('douban.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE if not exists movie(id integer PRIMARY KEY AUTOINCREMENT, subject text,
        votecount integer, title text, actors text, director text,
        region text, socre real, createdtime datetime)''')


def get_web_page_content():
    url = 'https://movie.douban.com/cinema/nowplaying/shenzhen/'
    req = request.Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit/537.36 (KHTML,like GeCKO) Chrome/45.0.2454.85 Safari/537.36 115Broswer/6.0.3')
    req.add_header('Referer', 'https://movie.douban.com/')
    req.add_header('Connection', 'keep-alive')
    response = request.urlopen(req)
    return response.read().decode('UTF-8')


def persist_data(data):
    with sqlite3.connect('douban.db') as conn:
        c = conn.cursor()
        for item in data:
            c.execute('''INSERT INTO movie(subject, votecount, title, actors, director, region, socre, createdtime) values(?,?,?,?,?,?,?,?)''',
                      (item['subject'], item['votecount'], item['title'], item['actors'], item['director'], item['region'],
                       item['socre'], item['createdtime']))


def init_log():
    log_format = '[%(asctime)-15s] %(message)s'
    logging.basicConfig(format=log_format)
    return logging.getLogger()


def main():
    check_python_version()

    logger = init_log()
    logger.setLevel("INFO")

    init_db()
    logger.info('init db success...')

    page_content = get_web_page_content()
    logger.info('success getting web page content...')

    par = DoubanMovieParser()
    par.feed(page_content)
    logger.info('success getting data from web page...')

    persist_data(par.get_data())
    logger.info('success persisting data...')

    logger.info('run sucessfully.')


if __name__ == '__main__':
    main()
    endDate = datetime.datetime.now()
    startDate = endDate+datetime.timedelta(days=(-1*6))
    with sqlite3.connect('douban.db') as conn:
        cur = conn.cursor()
        cur.execute(
            "select title, strftime('%Y%m%d', createdtime), avg(socre) from movie where createdtime between ? and ? group by title, strftime('%Y%m%d', createdtime)", (startDate, endDate))
        print(cur.fetchall())
