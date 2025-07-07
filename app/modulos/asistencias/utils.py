import qrcode
import io
import base64
import hmac, hashlib
from flask import current_app
from datetime import datetime

def generar_codigo_qr(grupo_id, estudiante_id):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    secreto = current_app.config['SECRET_KEY']
    mensaje = f"{grupo_id}|{estudiante_id}|{timestamp}"
    firma = hmac.new(secreto.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    data = f"{mensaje}|{firma}"

    qr = qrcode.make(data)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return img_base64
