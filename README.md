# Flask Payments API

A RESTful API for handling payment processing built with Flask and SQLAlchemy. Currently supports PIX payments with real-time updates via WebSocket.

## Features

- PIX payment processing
- Real-time payment status updates via WebSocket
- SQLite database integration
- Money handling with proper decimal precision
- Payment expiration management

## Tech Stack

- Flask
- SQLAlchemy
- Flask-SocketIO
- SQLite

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/flask-payments-api.git
cd flask-payments-api
```

2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Initialize database

```bash
flask db init
flask db migrate
flask db upgrade
```

## API Endpoints

### PIX Payments

#### Create PIX Payment

```http
POST /payments/pix
```

Request body:

```json
{
  "amount": 100.5
}
```

Response:

```json
{
  "status": "success",
  "message": "PIX payment created successfully",
  "payment": {
    "id": 1,
    "amount": 100.5,
    "paid": false,
    "bank_payment_id": "pix_123456",
    "qr_code": "qr_code_content",
    "expiration_date": "2025-08-11T14:30:00"
  }
}
```

#### Confirm PIX Payment

```http
POST /payments/pix/confirmation
```

Request body:

```json
{
  "bank_payment_id": "pix_123456",
  "amount": 100.5
}
```

Response:

```json
{
  "status": "success",
  "message": "PIX payment confirmed successfully",
  "payment": {
    "id": 1,
    "amount": 100.5,
    "paid": true,
    "bank_payment_id": "pix_123456",
    "qr_code": "qr_code_content",
    "expiration_date": "2025-08-11T14:30:00"
  }
}
```

#### Get Payment Page

```http
GET /payments/pix/{payment_id}
```

Returns an HTML page displaying the payment details and QR code for scanning. If the payment is already confirmed, it shows a confirmation page instead.

#### Get QR Code Image

```http
GET /payments/pix/qr_code/{file_name}
```

Returns the QR code image for the specified payment.

## Development

Start the development server:

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`

## Environment Variables

- `SQLALCHEMY_DATABASE_URI`: Database connection string (default: sqlite:///database.db)
- `SECRET_KEY`: Flask secret key for session management

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
