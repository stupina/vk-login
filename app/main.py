from app.app import create_app
from app.settings import Configuration


if __name__ == '__main__':
    app = create_app(configuration=Configuration)
    app.run(host='0.0.0.0')
