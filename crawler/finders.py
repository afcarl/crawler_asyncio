"""
Classes responsible retrieving relevant information from parsed html.
"""

from abc import abstractmethod
from urllib.parse import urlparse


class Finder(object):
    @abstractmethod
    def find_all(parsed_html):
        pass


class InternalLinkFinder(Finder):
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def find_all(self, parsed_html):
        links = [urlparse(link.get('href')) for link in parsed_html.find_all('a') if link.get('href') is not None]
        internal_links = [link for link in links if self.__local_link(link)]

        return set([link.path for link in internal_links])

    def __local_link(self, link):
        if link.scheme == '' and link.netloc == '':
            return True
        else:
            return link.netloc == self.baseurl


class StaticAssetsFinder(Finder):
    def find_all(self, parsed_html):
        def get_all(attr, tag):
            return [link.get(attr) for link in parsed_html.find_all(tag) if link.get(attr) is not None]

        other_links = get_all('href', 'link')
        images = get_all('src', 'img')
        scripts = get_all('src', 'script')

        return set(other_links + images + scripts)
