from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
  # Here you would implement the logic to create a PIX payment
  # For now, we will return a mock response
  response = {
    "status": "success",
    "message": "PIX payment created successfully"
  }
  return jsonify(response), 201

@app.route('/payments/pix/confirmation', methods=['POST'])
def confirm_payment_pix():
  # Here you would implement the logic to confirm a PIX payment
  # For now, we will return a mock response
  response = {
    "status": "success",
    "message": "PIX payment confirmed successfully"
  }
  return jsonify(response), 200

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def get_payment_pix(payment_id):
  # Here you would implement the logic to retrieve a PIX payment by ID
  # For now, we will return a mock response
  response = {
    "status": "success",
    "message": f"Retrieved PIX payment with ID {payment_id}",
    "data": {
      "payment_id": payment_id,
      "amount": 100.00,
      "currency": "BRL"
    }
  }
  return jsonify(response), 200

if __name__ == '__main__':
  app.run(debug=True)