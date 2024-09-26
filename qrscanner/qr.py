# qr.py
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File

def generate_qr_code(admin_input_id):
    # Create a QR code for the frontend URL, where users can join the queue
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Assuming your frontend URL for the join queue page is structured like this:
    frontend_url = f'https://adarshdev9349.github.io/Qr_frontend/?admin_input_id={admin_input_id}'
    qr.add_data(frontend_url)
    
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    byte_io = BytesIO()
    img.save(byte_io, format='PNG')
    byte_io.seek(0)

    return File(byte_io, name=f'qr_code_{admin_input_id}.png')
