# app/routes.py
from app.modulos.auth import auth_bp
from app.modulos.main import main_bp
from app.modulos.asistencias import asistencias_bp

blueprints = [
    auth_bp,
    main_bp,
    asistencias_bp
    
]
