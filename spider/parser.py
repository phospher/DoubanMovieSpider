from html.parser import HTMLParser
from datetime import datetime


class DoubanMovieParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reaching_target_div = False
        self.start_reading = False
        self.data = []

    def _get_attr_value_by_name(self, attrs, name):
        for attr in attrs:
            if attr[0] == name:
                return attr[1]

        return None

    def _get_id(self, attrs):
        return self._get_attr_value_by_name(attrs, 'id')

    def _get_class(self, attrs):
        return self._get_attr_value_by_name(attrs, 'class')

    def _add_data(self, attrs):
        self.data.append({
            'subject': self._get_attr_value_by_name(attrs, 'data-subject'),
            'votecount': int(self._get_attr_value_by_name(attrs, 'data-votecount')),
            'title': self._get_attr_value_by_name(attrs, 'data-title'),
            'actors': self._get_attr_value_by_name(attrs, 'data-actors'),
            'director': self._get_attr_value_by_name(attrs, 'data-director'),
            'region': self._get_attr_value_by_name(attrs, 'data-region'),
            'socre': float(self._get_attr_value_by_name(attrs, 'data-score')),
            'createdtime': datetime.now()
        })

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            id = self._get_id(attrs)
            if id != None:
                if id == 'nowplaying':
                    self.reaching_target_div = True
                elif id == 'upcoming':
                    self.start_reading = False
                    self.reaching_target_div = False
        elif self.reaching_target_div and tag == 'ul':
            class_value = self._get_class(attrs)
            if class_value != None and class_value == 'lists':
                self.start_reading = True
        elif self.start_reading and tag == 'li':
            class_value = self._get_class(attrs)
            if class_value != None and (class_value == 'list-item' or class_value == 'list-item hidden'):
                self._add_data(attrs)

    def get_data(self):
        return self.data
