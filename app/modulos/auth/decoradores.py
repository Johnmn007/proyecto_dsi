from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps

def rol_requerido(rol):
    def decorador(f):
        @wraps(f)
        def decorado(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión.', 'danger')
                return redirect(url_for('auth.login'))
            if current_user.rol.nombre != rol:
                flash('No tienes permiso para acceder a esta página.', 'warning')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorado
    return decorador
