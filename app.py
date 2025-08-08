from flask import Flask, jsonify, request, send_file, render_template
from repository.database import db
from models.payment import Payment
from datetime import datetime, timedelta
from utils.money_utils import to_small_unit, from_small_unit
from decimal import Decimal
from payments.pix import Pix

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_12345'
db.init_app(app)

@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
  data = request.get_json()
  if not data or 'amount' not in data:
    return jsonify({"error": "Invalid data"}), 400
  try:
    amount = to_small_unit(Decimal(data['amount']))
    expiration_date = datetime.now() + timedelta(minutes=30)
    new_payment = Payment(amount=amount, expiration_date=expiration_date)
    pix_payment = Pix().create_payment()
    new_payment.bank_payment_id = pix_payment['bank_payment_id']
    new_payment.qr_code = pix_payment['qr_code_path']
    db.session.add(new_payment)
    db.session.commit()
  except Exception as e:
    return jsonify({"error": str(e)}), 500
  else:
    return jsonify({
      "status": "success",
      "message": "PIX payment created successfully",
      "payment": new_payment.to_dict(),
    }), 201

@app.route('/payments/pix/confirmation/<int:payment_id>', methods=['POST'])
def confirm_payment_pix(payment_id):
  if not payment_id:
    return jsonify({"error": "Invalid payment ID"}), 400
  try:
    payment = Payment.query.get(payment_id)
    if not payment:
      return jsonify({"error": "Payment not found"}), 404
    payment.paid = True
    db.session.commit()
  except Exception as e:
    return jsonify({"error": str(e)}), 500
  else:
    return jsonify({
      "status": "success",
      "message": "PIX payment confirmed successfully",
      "payment": payment.to_dict(),
    }), 200

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def get_payment_pix_page(payment_id):
  return render_template('payment.html')

@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def get_qr_code_image(file_name):
  try:
    return send_file(f'static/img/{file_name}.png', mimetype='image/png')
  except Exception as e:
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
  app.run(debug=True)