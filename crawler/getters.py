"""
Classes responsible for getting raw html for a given path.
"""

from abc import abstractmethod
from os.path import join as join_path, isfile
import aiofiles
import aiohttp
import asyncio
import async_timeout


class Getter(object):

    @abstractmethod
    async def get(self, uri):
        """
        Get the data at a uri. returns a string of the data retrieved
        """
        pass


class FileGetter(Getter):
    """
    Class used for testing or 'local' webcrawling, for example crawling test_data/local_website.
    """
    def __init__(self, basedir):
        self.basedir = basedir

    async def get(self, uri):
        filepath = safe_join_path(self.basedir, uri)
        if not isfile(filepath):
            filepath = join_path(filepath, 'index.html')

        filedata = await aiofiles.open(filepath)
        filestring = await filedata.read()
        return filestring


class WebGetter(Getter):

    def __init__(self, domain):
        self.domain = domain
        loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=loop)

    async def get(self, path):
        uri = safe_join_path(self.domain, path)
        with async_timeout.timeout(10):
            async with self.session.get(uri) as response:
                return await response.text()

    def __del__(self):
        self.session.close()


def safe_join_path(a, b):
    if b.startswith('/'):
        return join_path(a, b[1:])
    else:
        return join_path(a, b)
