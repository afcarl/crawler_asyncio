import pytest
from crawler.getters import FileGetter


@pytest.mark.asyncio
async def test_basic_file_retrieval(event_loop, tmpdir, unused_tcp_port):

    getter = FileGetter('test_data')
    contents = await getter.get('simplefile.txt')
    assert contents == open('test_data/simplefile.txt').read()
