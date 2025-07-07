from app import create_app

# Por convención WSGI
application = create_app()

# También exportar como app, para tu estilo
# app = application