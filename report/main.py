#!/usr/bin/python3

from pymongo import MongoClient
import datetime

DAY_DURATION = 5


def getData():
    endDate = datetime.datetime.now()
    startDate = endDate+datetime.timedelta(days=(-1*DAY_DURATION))
    result = []

    with MongoClient('phospher-tencentcloud', 27017) as client:
        collection = client.douban.movies
        pipeline = [
            {
                '$match': {
                    'createdtime': {
                        '$gte': startDate,
                        '$lt': endDate
                    }
                }
            },
            {
                '$group': {
                    '_id': {
                        'title': '$title',
                        'year': {
                            '$year': '$createdtime'
                        },
                        'month': {
                            '$month': '$createdtime'
                        },
                        'day': {
                            '$dayOfMonth': '$createdtime'
                        }
                    },
                    'score': {
                        '$avg': '$socre'
                    }
                }
            }
        ]

        for item in collection.aggregate(pipeline):
            result.append({
                'title': item['_id']['title'],
                'date': item['_id']['year']*10000+item['_id']['month']*100+item['_id']['day'],
                'score': item['score']
            })

    return result


def main():
    print(getData())


if __name__ == '__main__':
    main()
