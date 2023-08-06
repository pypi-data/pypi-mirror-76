from . import version

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
        self._fs = FS()
        self._calc = Calculator()
        self.version = version
        self._commands = {
            'ls': self._fs.ls,
            'add': self._calc.add,
            'mult': self._calc.multiply,
        }

    def exec(self):
        return self._commands
