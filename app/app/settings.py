import os


class Configuration:
    SECRET_KEY = os.getenv('APP_SECRET_KEY')
    MONGODB_SETTINGS = {
        'db': os.getenv('DB_NAME'),
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT'))
    }
