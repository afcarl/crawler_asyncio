"""
Very simple searcher functions which look for keywords in raw text.
"""

# NOQA taken from https://stackoverflow.com/questions/3873361/finding-multiple-occurrences-of-a-string-within-a-string-in-python
def findall(sub, string):
    """
    >>> text = "Allowed Hello Hollow"
    >>> tuple(findall('ll', text))
    (1, 10, 16)
    """
    index = 0 - len(sub)
    try:
        while True:
            index = string.index(sub, index + len(sub))
            yield index
    except ValueError:
        pass
