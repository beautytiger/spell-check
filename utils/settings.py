from configparser import ConfigParser
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


config_file = 'project.ini'

config = ConfigParser()
config.read(config_file)

# config.sections()

# config['default']['cncf']

# print(BASE_DIR)
print(config.sections())
# print(config['default']['cncf'])
