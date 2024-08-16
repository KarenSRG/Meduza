import os

###################
# DATABASE CONFIG #
###################

DB_NAME = os.environ.get('DB_NAME', 'meduza')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_DRIVER = os.environ.get('DB_DRIVER', 'postgresql+asyncpg')


DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"