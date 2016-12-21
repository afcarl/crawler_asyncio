
from setuptools import setup
from setuptools import find_packages

VERSION = '0.0.1'

additional_args = {
    'zip_safe': False,
    'packages': find_packages(),
    'entry_points': {
        'console_scripts': [
            'crawl = crawler.crawl:main'
        ],
    }
}

setup(
    name='wcrawler',
    version=VERSION,
    author='Sam Coope',
    author_email='sam.j.coope@gmail.com',
    description=('webcrawler using asyncio'),
    long_description=open('README.md').read(),
    license='MIT',
    keywords='asyncio web crawling crawler',
    url='https://github.com/coopie/crawler_asyncio',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
    install_requires=[
        'aiofiles==0.3.0',
        'aiohttp==1.2.0',
        'async-timeout==1.1.0',
        'beautifulsoup4==4.5.1',
        'chardet==2.3.0',
        'docopt==0.6.2',
        'multidict==2.1.4',
        'nose==1.3.7',
        'odict==1.5.2',
        'plumber==1.3.1',
        'py==1.4.32',
        'pytest==3.0.5',
        'pytest-asyncio==0.5.0',
        'requests==2.12.4',
        'yarl==0.8.1',
        'zope.component==4.3.0',
        'zope.deprecation==4.2.0',
        'zope.event==4.2.0',
        'zope.interface==4.3.3',
        'zope.lifecycleevent==4.1.0'
    ],
    **additional_args
)
