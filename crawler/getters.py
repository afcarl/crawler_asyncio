from abc import abstractmethod
import aiofiles
from os.path import join as join_path


class Getter(object):

    @abstractmethod
    def get(self, uri):
        """
        Get the data at a uri. returns a string of the data retrieved
        """
        pass


class FileGetter(Getter):
    def __init__(self, basedir):
        self.basedir = basedir

    def get(self, uri):
        async with aiofiles.open(join_path(self.basedir, uri)) as f:
            return f.read()
