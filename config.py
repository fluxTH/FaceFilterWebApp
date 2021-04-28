from os.path import abspath, join

APP_NAME = 'ComEngEss WebApp'

DATABASE_URI = 'sqlite:///database.sqlite3'

PROJECT_PATH = abspath('.')

TEMPLATE_PATH =         join(PROJECT_PATH, 'frontend')
STATIC_PATH =           join(PROJECT_PATH, 'frontend/static')
ORIGINAL_MEDIA_PATH =   join(PROJECT_PATH, 'data/original_images')
PROCESSED_MEDIA_PATH =  join(PROJECT_PATH, 'data/processed_images')
FILTER_PATH =           join(PROJECT_PATH, 'data/filter')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
