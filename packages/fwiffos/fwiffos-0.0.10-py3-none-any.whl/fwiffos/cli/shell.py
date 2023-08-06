from fwiffos.core import version

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

    def commands(self):
        return self._commands

class Commands(object):
    def __init__(self):
        fs = FS()
        calc = Calculator()
        self._version = version
        self.__commands = {
            'ls': fs.ls,
            'add': calc.add,
            'mult': calc.multiply,
        }

    def exec(self):
        return self.__commands

commands = Commands()
