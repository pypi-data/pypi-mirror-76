from fwiffos.core import version
from fwiffos.cli.sudo import LetUs
from fwiffos.read.gsheets import GSheets

class Calculator(object):

    def add(self, x, y):
      return x + y

    def multiply(self, x, y):
      return x * y

class FS(object):

    def __init__(self):
        self.filesystem = {'/': ['README']}

    def ls(self, cwd='/'):
        print(self.filesystem[cwd])

class Commands(object):
    def __init__(self):
        fs = FS()
        calc = Calculator()
        sudo = LetUs()
        gsheets = GSheets()
        self._version = version
        self.__commands = {
            'ls': fs.ls,
            'add': calc.add,
            'mult': calc.multiply,
            'sudo': sudo.letus,
            'letus': sudo.letus,
            'read': gsheets,
        }

    def exec(self):
        return self.__commands

commands = Commands()
