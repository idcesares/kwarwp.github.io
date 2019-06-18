from unittest.mock import MagicMock

class MMock(MagicMock):
    def __le__(self, _):
        return MagicMock()

class dom:
    pass
    def __le__(self, _):
        return MagicMock()
'''
class html:
    pass

class win:
    pass

class timer:
    pass

class ajax:
    pass
'''
window = win = timer = ajax = html = MMock()
html.__le__ = MagicMock()
window = win
document = {"pydiv": dom()}
document.head = MMock()

