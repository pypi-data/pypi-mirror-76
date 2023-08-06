from . import version
from . import arithmetic


filesystem = {'/': ['README']}

def ls(cwd='/'):
    print(filesystem[cwd])

commands = {
    'add' : arithmetic.add,
    'multiply' : arithmetic.multiply,
    'ls' : ls,
    'version' : version,
}
