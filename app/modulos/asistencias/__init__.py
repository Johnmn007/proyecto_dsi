from flask import Blueprint

asistencias_bp=Blueprint('asistencias',__name__,
                         url_prefix='/asistencias',
                         template_folder='../../templates/asistencias')

from . import routes