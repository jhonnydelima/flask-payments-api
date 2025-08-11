import sys
sys.path.append('../')

import pytest
import os
from payments.pix import Pix

def test_pix_create_payment():
  pix = Pix()
  payment_data = pix.create_payment(base_dir='../')
  assert 'bank_payment_id' in payment_data
  assert 'qr_code' in payment_data
  qr_code = payment_data['qr_code']
  assert os.path.isfile(f'../static/img/{qr_code}.png')