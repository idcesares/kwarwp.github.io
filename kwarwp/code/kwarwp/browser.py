from unittest.mock import MagicMock

class MMock(MagicMock):
    def __le__(self, _):
        return MagicMock()

class dom(dict):
    head = MMock()
    pass
    def __le__(self, _):
        return MagicMock()


class html:
    DIV = MMock()
    def __init__(self, *_, **__):
        self.value = ""
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
window = win = timer = ajax = MMock()
html.__le__ = MagicMock()
window = win
document = dom(pydiv= dom())
document.head = dom()
html.DIV = html.STYLE = html.IMG = html.bind = html.H1 = html.H2 = html.A = html.CODE = html.PRE = html
html.style = MMock()

