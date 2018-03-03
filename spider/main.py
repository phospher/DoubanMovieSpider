#!/usr/bin/python3

import sys
from urllib import request
from parser import DoubanMovieParser
from pymongo import MongoClient
import logging


def check_python_version():
    if sys.version_info.major < 3:
        raise Exception('Must be using Python 3')


def get_web_page_content():
    url = 'https://movie.douban.com/cinema/nowplaying/shenzhen/'
    response = request.urlopen(url)
    return response.read().decode('UTF-8')


def persist_data(data):
    client = MongoClient('phospher-tencentcloud', 27017)
    collection = client.douban.movies
    collection.insert_many(data)


def init_log():
    log_format = '[%(asctime)-15s] %(message)s'
    logging.basicConfig(format=log_format)
    return logging.getLogger()


def main():
    check_python_version()

    logger = init_log()
    logger.setLevel("INFO")

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
