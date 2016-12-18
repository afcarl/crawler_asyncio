
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
        'docopt'
    ],
    **additional_args
)
