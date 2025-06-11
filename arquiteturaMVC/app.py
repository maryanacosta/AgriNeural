from flask import Flask, redirect, url_for
from controllers.authController import auth_bp
from controllers.produtorController import produtor_bp
from controllers.operadorController import operador_bp
from controllers.mosaiqueiroController import mosaiqueiro_bp
from controllers.uploadController import upload_bp
from controllers.statusController import status_bp

# Inicializa o framework e adiciona o direcionamento do UI
app = Flask(__name__,
            template_folder='./ui/templates',
            static_folder='./ui/static'
            )

# configurações
app.secret_key = 'chave_secreta_qualquer'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATUS_FOLDER'] = 'status'

# direcionamento para cada funcionalidade do site
app.register_blueprint(auth_bp)
app.register_blueprint(produtor_bp)
app.register_blueprint(operador_bp)
app.register_blueprint(mosaiqueiro_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(status_bp)

# inicialização
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
