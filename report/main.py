#!/usr/bin/python3

import plotly.offline as py
import plotly.graph_objs as go
import data
import datetime
import os
import shutil

RESULT_DIR = './result'


def get_score(data, title, date):
    for item in data:
        if item['title'] == title and item['date'] == date:
            return item['score']
    return None


def format_date(date):
    year = date//10000
    temp = date % 10000
    month = temp//100
    day = temp % 100
    return '{0:04d}/{1:02d}/{2:02d}'.format(year, month, day)


def confirm_dir():
    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)


def main():
    chart_data = data.get_data()
    date_data = set([x['date'] for x in chart_data])
    title_data = set([x['title'] for x in chart_data])
    x_data = sorted(date_data)
    plotly_data = []
    for title in title_data:
        plotly_data.append(go.Scatter(
            x=[format_date(x) for x in x_data],
            y=[get_score(chart_data, title, d) for d in x_data],
            mode='lines',
            name=title
        ))

    confirm_dir()
    now = datetime.datetime.now()
    file_name = os.path.join(
        RESULT_DIR, '{0:04d}{1:02d}{2:02d}.html'.format(now.year, now.month, now.day))
    py.plot(plotly_data,
            filename=file_name)

    latest_file_name = os.path.join(RESULT_DIR, 'latest.html')
    shutil.copy(file_name, latest_file_name)


if __name__ == '__main__':
    main()
