from os import path

from logbook import Logger, FileHandler

log_filename = 'battleship.log'
log_path = path.join(path.expanduser('~'), log_filename)
log_handler = FileHandler(log_filename)
logger = Logger('BattleShip logger')
#log_handler = FileHandler(log_path)

__version__ = '0.1a'
__version__tuple = (0, 1)
