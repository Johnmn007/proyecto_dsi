from flask import render_template
from app.modulos.main import main_bp

@main_bp.route('/')
def login():
    return render_template('main/index.html')
