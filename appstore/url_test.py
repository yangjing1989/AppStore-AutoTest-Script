# -*- coding:utf8 -*-
import urllib.request


class UrlTest():

    def __init__(self, url):
        self.url = url

    def get_response_code(self, url):
        response = urllib.request.urlopen(self.url)
        if response.code == 200:
            return True
        else:
            return response.code
