import os
import random

from lich_scrapy_random_useragent.errors import UserAgentError
from lich_scrapy_random_useragent.utils import read


REPLACEMENTS={
    "_":"",
    " ":"",
}

SHORTCUTS = {
    'internet explorer': 'internetexplorer',
    'ie': 'internetexplorer',
    'msie': 'internetexplorer',
    'edge': 'internetexplorer',
    'google': 'chrome',
    'googlechrome': 'chrome',
    'ff': 'firefox',
}

class FakeUserAgent(object):
    def __init__(self, path, groups):
        if not isinstance(groups, dict):
            raise Exception(f"groups mast be dict")
        self.groups=groups
        self.randomize=[]
        if len(groups) is 0 :
            self.load(path)
        else:
            self.__set_randomize()

    def load(self,path):
        if isinstance(path, str) :
            f=path.strip()
            if os.path.isfile(f):
                self.groups = read(f)
                self.__set_randomize()
                return
        raise Exception(f"load user-agent file failed")

    def _get_random_ua(self, type):
        return getattr(self,type)
    
    def __set_randomize(self):
        for key in self.groups:
                    n=len(self.groups[key])
                    while n>0:
                        self.randomize.append(key)
                        n-=1
    def __getitem__(self, attr):
        try:
            for value, replacement in REPLACEMENTS.items():
                attr = attr.replace(value, replacement)
            attr = attr.lower()
            groups=None
            if attr == 'random':
                groups = random.choice(self.randomize)
            else:
                groups = SHORTCUTS.get(attr, attr)
            
            return random.choice(self.groups[groups])
        except (KeyError, IndexError):
            raise UserAgentError(f"getting groups error, ua type: {attr}")