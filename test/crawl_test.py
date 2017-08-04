import pytest
from crawler.crawl import crawl

@pytest.mark.skip(reason='blog website has changed')
@pytest.mark.asyncio
async def test_crawl_is_same():
    map1 = await crawl('', 'test_data/local_website', True)
    map2 = await crawl('http://samcoope.com', '', False)

    # these both fail to find any html on these pages, but for different reasons, so dicts would be different.
    map1.pop('resource/misc/Palpitate-Presentation.pdf')
    map2.pop('resource/misc/Palpitate-Presentation.pdf')
    assert map1 == map2
