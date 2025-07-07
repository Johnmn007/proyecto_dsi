# app/auth_loader.py
from app.extensions import login_manager
from app.models import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
