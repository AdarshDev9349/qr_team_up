from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File

def generate_qr_code(admin_input_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'{settings.SITE_URL}/queue/{admin_input_id}/')
    url= f'/queue/{admin_input_id}/'
    print(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    byte_io = BytesIO()
    img.save(byte_io, format='PNG')
    byte_io.seek(0)

    return File(byte_io, name=f'qr_code_{admin_input_id}.png')
