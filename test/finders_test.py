from crawler.finders import InternalLinkFinder, StaticAssetsFinder
from bs4 import BeautifulSoup


def test_internal_links():
    html = open('test_data/local_website/index.html').read()
    parsed_html = BeautifulSoup(html, 'html.parser')

    link_finder = InternalLinkFinder('samcoope.com')
    links = link_finder.find_all(parsed_html)

    assert links == {'posts/slices', 'about', 'posts/reading-faces', 'index.html', 'posts/making_the_blog'}


def test_static_assets_finder():
    expected = {
        'https://fonts.googleapis.com/css?family=Quicksand:400,700,300',
        'resource/images/me.jpeg',
        'resource/images/favicon.ico',
        'https://fonts.googleapis.com/css?family=VT323',
        'https://fonts.googleapis.com/css?family=Merriweather:400,400italic,300italic,300,700,700italic,900,900italic&subset=latin,latin-ext',  # NOQA
        'resource/styles/main.css'
    }
    html = open('test_data/local_website/index.html').read()
    parsed_html = BeautifulSoup(html, 'html.parser')

    sa_finder = StaticAssetsFinder()
    links = sa_finder.find_all(parsed_html)
    assert links == expected
