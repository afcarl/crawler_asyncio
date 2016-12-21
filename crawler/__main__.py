import os
import sys

if __package__ == '':
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)


from crawler.crawl import main as crawler_main  # NOQA


if __name__ == '__main__':
    crawler_main()
