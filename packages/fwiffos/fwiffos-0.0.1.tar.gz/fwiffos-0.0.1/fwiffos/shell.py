from . import version
from . import arithmetic

commands = {
    'add' : arithmetic.add,
    'multiply' : arithmetic.multiply,
    'version' : version,
}
