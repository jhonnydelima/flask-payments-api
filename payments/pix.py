from uuid import uuid4
import qrcode

class Pix:
  def __init__(self):
    pass

  def create_payment(self):
    bank_payment_id = str(uuid4())
    hash_payment = f'hash_payment_{bank_payment_id}'
    qr_code = f'qr_code_{bank_payment_id}'
    qrcode_img = qrcode.make(hash_payment)
    qrcode_img.save(f'static/img/{qr_code}.png')

    return {
      "bank_payment_id": bank_payment_id,
      "qr_code": qr_code,
    }