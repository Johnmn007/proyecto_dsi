from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .extensions import login_manager
from dotenv import load_dotenv
import os

# Carga el archivo .env
load_dotenv()

# Inicializa SQLAlchemy sin app (se une con init_app)
db = SQLAlchemy()

#agregamos las migraciones de flask-migrate
migrate = Migrate()

def create_app(config_name=None): 
    
    # Paso 1: Importar config después de cargar dotenv
    from .config import config_by_name

    # Paso 2: Detectar automáticamente el entorno si no se pasa manualmente
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    # Paso 3: Validar que el entorno exista
    if config_name not in config_by_name:
        raise ValueError(f"Configuración desconocida: '{config_name}'")

    # Paso 4: Crear la app Flask con la config adecuada
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    #le paso la configuracion para que funcione migrate
    from app.config import Config
    app.config.from_object(Config)

    # Paso 5: Inicializar extensiones
    db.init_app(app)
    
    migrate.init_app(app, db)  # ← Aquí conectamos Migrate
      
    #esto funciona para login en auth, para las sesiones
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # nombre del endpoint de login
    login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
    
    from app import auth_loader
    
    # Paso 6: Registrar Blueprints
    from .routes import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)
        
#  -------------------------------en estos prints se ve en que modo estas trabajando----------------------   
# .----------.--.-.-.-.-.-.-.-.-.-.-.--.-.-.-.-.-.-.-.-.-ヾ▽.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-..-  
# ----------------------------------------------------------------------------------------------------------  
        
    print(f"FLASK_ENV detectado: {config_name}")
    print(f"Conectando a: {app.config['SQLALCHEMY_DATABASE_URI']}")


    return app
