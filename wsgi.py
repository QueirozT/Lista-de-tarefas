from app import create_app
from config import ProdConf


app = create_app(ProdConf)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
