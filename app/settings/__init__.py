import os
import ConfigParser

from unipath import FSPath

PROJECT_DIR = FSPath(__file__).absolute().ancestor(3)
default_config_dir = os.sep.join((PROJECT_DIR, 'configuration'))


def config_parse(section, application_dict):
    if not config.has_section(section):
        print '------ Using default {} settings'.format(section)
        return

    for option in config.options(section):
        application_dict[option.upper()] = config.get(section, option.upper())

#
# Environment Settings
#
SETTINGS_FILE_NAME = os.sep.join((default_config_dir, 'environment.ini'))

if not os.path.isfile(SETTINGS_FILE_NAME):
    raise Exception("Environment settings file '%s' not found."
                    % SETTINGS_FILE_NAME)

config = ConfigParser.RawConfigParser()
config.read(SETTINGS_FILE_NAME)

# Configure snack-web keys according to environment
DEBUG = (config.get('system', 'DEBUG') == 'True')
HAS_FTP = (config.get('system', 'HAS_FTP') == 'True')
PRE_INIT_CAMERA = (config.get('system', 'PRE_INIT_CAMERA') == 'True')
USE_WEB_CAMERA = (config.get('system', 'USE_WEB_CAMERA') == 'True')
USE_MOTION_CAMERA = (config.get('system', 'USE_MOTION_CAMERA') == 'True')

MOTION_CAMERA_SNAPSHOT = config.get('system', 'MOTION_CAMERA_SNAPSHOT')
CROP_IMAGE_BORDERS = eval(config.get('system', 'CROP_IMAGE_BORDERS'))
SHOW_REMOVED_SNACKS = (config.get('system', 'SHOW_REMOVED_SNACKS') == 'True')

HOST = config.get('system', 'HOST')
PORT = int(config.get('system', 'PORT'))
USE_COLOR_DISTANCE_FOR_BACKGROUND = (config.get('system', 'USE_COLOR_DISTANCE_FOR_BACKGROUND') == 'True')
BACKGROUND_MASK_THRESHOLD = int(config.get('system', 'BACKGROUND_MASK_THRESHOLD'))
BACKGROUND_AUTO_CALIBRATE = (config.get('system', 'BACKGROUND_AUTO_CALIBRATE') == 'True')

DB_CONNECT_STRING = config.get('database', 'DB_CONNECT_STRING')
DB = config.get('database', 'DB')

USE_CLASSIFIER = (config.get('classifier', 'USE_CLASSIFIER') == 'True')
CLASSIFIER_URL = config.get('classifier', 'CLASSIFIER_URL')

FTP_HOST = config.get('ftp', 'FTP_HOST')
FTP_PORT = config.get('ftp', 'FTP_PORT')
HTTP_PORT = config.get('ftp', 'HTTP_PORT')
FTP_USER = config.get('ftp', 'FTP_USER')
FTP_PASS = config.get('ftp', 'FTP_PASS')
