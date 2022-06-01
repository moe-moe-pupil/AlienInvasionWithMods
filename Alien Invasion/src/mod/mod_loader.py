from cefpython3 import cefpython as cef
import os
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("Alien Invasion\\")+len("Alien Invasion\\")]  # 获取myProject，也就是项目的根路径
modPath = os.path.abspath(rootPath + 'mod') # 获取tran.csv文件的路径

class ModLoader():
    def __init__(self, path = modPath):
        self.this_path = path
        self.mod_list = []
        self.mod_name = []
        for i in self.find_all_mod(self.this_path):
            if i.find('__pycache__') == -1:
                self.mod_list.append(i + '\\index.html')
                self.mod_name.append(i.rsplit('\\', 1)[1])

    def find_all_mod(self, path):
        for root, ds, fs in os.walk(path):
            for f in ds:
                mod_name = os.path.join(root, f)
                yield mod_name

    def mod_load(path):
        pass

