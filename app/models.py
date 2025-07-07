from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app import db

# Roles
class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(100))
    usuarios = db.relationship('Usuario', backref='rol', lazy=True)

# Carreras
class Carrera(db.Model):
    __tablename__ = 'carreras'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    usuarios = db.relationship('Usuario', backref='carrera', lazy=True)
    asignaturas = db.relationship('Asignatura', backref='carrera', lazy=True)

# Usuarios
class Usuario(UserMixin,db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    carrera_id = db.Column(db.Integer, db.ForeignKey('carreras.id'))
    fecha_creacion = db.Column(db.Date, default=datetime.utcnow)

# Asignaturas
class Asignatura(db.Model):
    __tablename__ = 'asignaturas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(20), nullable=False)
    carrera_id = db.Column(db.Integer, db.ForeignKey('carreras.id'))
    creditos = db.Column(db.Integer)
    grupos = db.relationship('Grupo', backref='asignatura', lazy=True)

# Periodos académicos
class Periodo(db.Model):
    __tablename__ = 'periodos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    anio = db.Column(db.Integer)
    estado = db.Column(db.String(20))
    grupos = db.relationship('Grupo', backref='periodo', lazy=True)

# Grupos (secciones por curso)
class Grupo(db.Model):
    __tablename__ = 'grupos'
    id = db.Column(db.Integer, primary_key=True)
    asignatura_id = db.Column(db.Integer, db.ForeignKey('asignaturas.id'))
    docente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodos.id'))
    docente = db.relationship('Usuario', foreign_keys=[docente_id])
    horarios = db.relationship('HorarioClase', backref='grupo', lazy=True)
    matriculas = db.relationship('Matricula', backref='grupo', lazy=True)

# Horarios
class HorarioClase(db.Model):
    __tablename__ = 'horarios_clase'
    id = db.Column(db.Integer, primary_key=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'))
    dia_semana = db.Column(db.String(10))  # Ej: lunes, martes
    hora_inicio = db.Column(db.Time)
    hora_fin = db.Column(db.Time)
    aula = db.Column(db.String(20))

# Matrículas
class Matricula(db.Model):
    __tablename__ = 'matriculas'
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'))
    fecha_matricula = db.Column(db.Date, default=datetime.utcnow)
    estudiante = db.relationship('Usuario', foreign_keys=[estudiante_id])

# Calificaciones
class Calificacion(db.Model):
    __tablename__ = 'calificaciones'
    id = db.Column(db.Integer, primary_key=True)
    matricula_id = db.Column(db.Integer, db.ForeignKey('matriculas.id'))
    parcial1 = db.Column(db.Float)
    parcial2 = db.Column(db.Float)
    final = db.Column(db.Float)

# Tramites
class Tramite(db.Model):
    __tablename__ = 'tramites'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    creado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class TramiteSolicitud(db.Model):
    __tablename__ = 'tramites_solicitudes'
    id = db.Column(db.Integer, primary_key=True)
    tramite_id = db.Column(db.Integer, db.ForeignKey('tramites.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    estado = db.Column(db.String(20))
    archivo_subido = db.Column(db.String(255))
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)

# Archivos
class Archivo(db.Model):
    __tablename__ = 'archivos'
    id = db.Column(db.Integer, primary_key=True)
    nombre_original = db.Column(db.String(255))
    ruta_archivo = db.Column(db.String(255))
    subido_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    descripcion = db.Column(db.Text)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)

# Asistencias
class Asistencia(db.Model):
    __tablename__ = 'asistencias'
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=False)
    fecha = db.Column(db.Date, default=datetime.utcnow)
    hora_registro = db.Column(db.Time, default=datetime.utcnow().time)
    estado = db.Column(db.String(20), default='presente')
    qr_token_hash = db.Column(db.String(128), unique=True, nullable=True)

    estudiante = db.relationship('Usuario', foreign_keys=[estudiante_id])
    grupo = db.relationship('Grupo', foreign_keys=[grupo_id])
