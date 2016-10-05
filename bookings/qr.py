import qrcode

def generate_qrcode(text, filepath):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(filepath)
