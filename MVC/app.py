from flask import Flask, redirect, url_for, jsonify
from flask_cors import CORS
from MVC.controllers.authController import auth_bp
from MVC.controllers.produtorController import produtor_bp
from MVC.controllers.operadorController import operador_bp
from MVC.controllers.mosaiqueiroController import mosaiqueiro_bp
from MVC.controllers.uploadController import upload_bp
from MVC.controllers.statusController import status_bp

# Inicializa o framework e adiciona o direcionamento do UI
app = Flask(__name__,
            template_folder='./view/templates',
            static_folder='./view/static'
            )
CORS(app, supports_credentials=True)

# configurações
app.secret_key = 'chave_secreta_qualquer'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATUS_FOLDER'] = 'status'

# direcionamento para cada funcionalidade do site
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(produtor_bp)
app.register_blueprint(operador_bp)
app.register_blueprint(mosaiqueiro_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(status_bp)

# inicialização
@app.route('/')
def index():
    return redirect('http://localhost:5173/')

if __name__ == '__main__':
    app.run(debug=True)
