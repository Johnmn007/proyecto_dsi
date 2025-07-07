from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import asistencias_bp
from datetime import datetime
from app.models import Matricula, Grupo, HorarioClase, Asignatura  # Ajusta a tus imports

@asistencias_bp.route('/asistencias')
@login_required
def mis_clases_hoy():
    if current_user.rol.nombre != 'estudiante':
        flash('Solo los estudiantes pueden generar asistencia', 'warning')
        return redirect(url_for('main.index'))

    dia_actual = datetime.now().strftime('%A').lower()

    # Buscar los grupos en los que está matriculado
    clases = Grupo.query \
        .join(Matricula, Grupo.id == Matricula.grupo_id) \
        .join(HorarioClase, Grupo.id == HorarioClase.grupo_id) \
        .filter(
            Matricula.estudiante_id == current_user.id,
            HorarioClase.dia_semana == dia_actual
        ).all()

    return render_template('asistencias/asistencias.html',clases=clases)


from .utils import generar_codigo_qr

@asistencias_bp.route('/generar-qr/<int:grupo_id>')
@login_required
def generar_qr(grupo_id):
    if current_user.rol.nombre != 'estudiante':
        flash('Solo estudiantes pueden generar QR', 'danger')
        return redirect(url_for('main.index'))

    qr_img = generar_codigo_qr(grupo_id, current_user.id)
    return render_template('asistencias/qr_generado.html', qr_img=qr_img)
