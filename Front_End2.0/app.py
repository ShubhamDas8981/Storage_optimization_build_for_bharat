from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merchant_data.db'
app.config['SQLALCHEMY_BINDS'] = {
    'buyer': 'sqlite:///buyer_data.db'  # Separate database for buyers
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the database model
class Merchant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.String(50), unique=True, nullable=False)
    merchant_name = db.Column(db.String(100), nullable=False)
    merchant_pass = db.Column(db.String(100), nullable=False)
    pincode_list = db.Column(db.String(500), nullable=False)

class Buyer(db.Model):
    __bind_key__ = 'buyer'  # Use the 'buyer' database
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.String(50), unique=True, nullable=False)
    buyer_pass = db.Column(db.String(100), nullable=False)
    buyer_pincode = db.Column(db.String(500), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_buyer', methods=['POST'])
def submit_buyer():
    data=request.json #retrieve JSON data
    buyer_id = data.get('buyerId')
    buyer_pass = data.get('buyerPass')
    buyer_pincode = data.get('buyerPincode')
    print("Buyer ID: ",buyer_id)
    print("Buyer Password: ",buyer_pass)
    print("Buyer Searching Pin code: ",buyer_pincode)

    # Create a new Buyer object
    new_buyer = Buyer(
        buyer_id=buyer_id,
        buyer_pass=buyer_pass,
        buyer_pincode=','.join(buyer_pincode)  # Convert pincode list to string for storage
    )

    # Add the new buyer to the database
    db.session.add(new_buyer)  # Specify the bind to use 'buyer' database
    db.session.commit()

    # Process data and prepare a response
    response = {
        "status": "success",
        "message": "Buyer data received successfully!",
        "buyer_id": buyer_id,
        "buyer_pass": buyer_pass,
        "buyer_pincode": buyer_pincode
    }

    return jsonify(response)

@app.route('/submit_merchant', methods=['POST'])
def submit_merchant():
    data=request.json # retrieve json data
    merchant_name = data.get('merchantName')
    merchant_id = data.get('merchantid')
    merchant_pass = data.get('merchantpass')
    pincode_count = data.get('pincodeCount')
    #pincode_list = [data.get(f'pincode_{i}') for i in range(1, int(pincode_count)+1)]
    pincode_list = data.get('pincodeList', [])  # Retrieve the pincodeList directly
    print("Merchant Name: ",merchant_name)
    print("Merchant ID: ",merchant_id)
    print("Merchant Password: ",merchant_pass)
    print("Merchant Pincodes: ",pincode_list)

    # Create a new Merchant object
    new_merchant = Merchant(
        merchant_id=merchant_id,
        merchant_name=merchant_name,
        merchant_pass=merchant_pass,
        pincode_list=','.join(pincode_list)  # Convert pincode list to string for storage
    )

    # Add the new merchant to the database
    db.session.add(new_merchant)
    db.session.commit()

    # Process data and prepare a response
    response = {
        "status": "success",
        "message": "Merchant data received successfully!",
        "merchant_name": merchant_name,
        "merchant_id": merchant_id,
        "merchant_pass": merchant_pass,
        "pincode_count": pincode_count,
        "pincode_list": pincode_list
    }

    return jsonify(response)

if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()  # Drop all existing tables
        #db.create_all(bind=['buyer'])  # Create buyer tables based on models
        db.create_all()  # Create tables based on models
    app.run(debug=True)

