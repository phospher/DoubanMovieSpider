import datetime
import sqlite3

DAY_DURATION = 6


def get_data():
    endDate = datetime.datetime.now()
    startDate = endDate+datetime.timedelta(days=(-1*DAY_DURATION))
    result = []

    with sqlite3.connect('douban.db') as conn:
        cur = conn.cursor()
        cur.execute(
            "select title, strftime('%Y/%m/%d', createdtime), avg(socre) from movie where createdtime between ? and ? group by title, strftime('%Y/%m/%d', createdtime)", (startDate, endDate))

        for item in cur.fetchall():
            result.append({
                'title': item[0],
                'date': item[1],
                'score': item[2]
            })

    return result
