from flask import Flask, jsonify, request, send_file, render_template
from repository.database import db
from models.payment import Payment
from datetime import datetime, timedelta
from utils.money_utils import to_small_unit, from_small_unit
from decimal import Decimal
from payments.pix import Pix
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_12345'
db.init_app(app)
socketio = SocketIO(app)

APP_HOST = 'http://127.0.0.1:5000'

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
    new_payment.qr_code = pix_payment['qr_code']
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

@app.route('/payments/pix/confirmation', methods=['POST'])
def confirm_payment_pix():
  data = request.get_json()
  bank_payment_id = data.get('bank_payment_id')
  if not bank_payment_id or not data.get('amount'):
    return jsonify({"error": "Invalid payment data"}), 400
  try:
    payment = Payment.query.filter_by(bank_payment_id=bank_payment_id).first()
    if not payment or payment.paid:
      return jsonify({"error": "Payment not found"}), 404
    if payment.expiration_date < datetime.now():
      return jsonify({"error": "Payment expired"}), 400
    amount = to_small_unit(Decimal(data.get('amount')))
    if amount != payment.amount:
      return jsonify({"error": "Invalid payment data"}), 400
    payment.paid = True
    db.session.commit()
    socketio.emit(f'payment-confirmed-{payment.id}')
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
  payment = Payment.query.get(payment_id)
  if not payment:
    return render_template('404.html')
  template = 'payment.html' if not payment.paid else 'confirmed_payment.html'
  return render_template(
    template,
    payment_id=payment_id,
    amount=from_small_unit(payment.amount),
    host=APP_HOST,
    qr_code=payment.qr_code,
  )

@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def get_qr_code_image(file_name):
  try:
    return send_file(f'static/img/{file_name}.png', mimetype='image/png')
  except Exception as e:
    return jsonify({"error": str(e)}), 500

@socketio.on('connect')
def handle_connect():
  print('Client connected to the server')

@socketio.on('disconnect')
def handle_disconnect():
  print('Client disconnected from the server')

if __name__ == '__main__':
  socketio.run(app, debug=True)