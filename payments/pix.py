from uuid import uuid4
import qrcode

class Pix:
  def __init__(self):
    pass

  def create_payment(self):
    bank_payment_id = uuid4()
    hash_payment = f'hash_payment_{bank_payment_id}'
    qrcode_path = f'static/img/qrcode_{bank_payment_id}'
    qrcode_img = qrcode.make(hash_payment)
    qrcode_img.save(f'{qrcode_path}.png')

    return {
      "bank_payment_id": bank_payment_id,
      "qr_code_path": qrcode_path,
    }