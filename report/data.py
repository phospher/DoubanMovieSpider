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
            "select subject, title, strftime('%Y/%m/%d', createdtime), avg(socre) from movie where createdtime between ? and ? group by subject, title, strftime('%Y/%m/%d', createdtime)", (startDate, endDate))

        for item in cur.fetchall():
            result.append({
                'subject': item[0],
                'title': item[1],
                'date': item[2],
                'score': item[3]
            })

    return result
