# from flask import render_template
# from . import auth_bp

# @auth_bp.route('/login')
# def login():
#     return render_template('auth/login.html')
# -----------------------------------------------------------------------------------------------

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.models import Usuario
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and check_password_hash(usuario.contrasena, contrasena):
            login_user(usuario)
            flash('Inicio de sesión exitoso.', 'success')

            # Redirige según el rol
            if usuario.rol.nombre == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif usuario.rol.nombre == 'docente':
                return redirect(url_for('docente.home'))
            elif usuario.rol.nombre == 'estudiante':
                return render_template('auth/estudiante_home.html')
            else:
                flash('Rol no reconocido.', 'danger')
                return redirect(url_for('main.index'))

        flash('Correo o contraseña incorrectos.', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('main.index'))
