from app import create_app
from config import ProdConf

from app.models import User, Tarefas


app = create_app(ProdConf)


@app.shell_context_processor
def make_shell_context():
    return {'db': app.db, 'User': User, 'Tarefas': Tarefas}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
