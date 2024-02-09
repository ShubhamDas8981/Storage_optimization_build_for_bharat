from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from scipy.sparse import csr_matrix
import scipy.sparse as sp
import numpy as np


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merchant_data.db'
app.config['SQLALCHEMY_BINDS'] = {
    'buyer': 'sqlite:///buyer_data.db'  # Separate database for buyers
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the database model bharat
class Merchant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.String(50), unique=True, nullable=False)
    merchant_name = db.Column(db.String(100), nullable=False)
    merchant_pass = db.Column(db.String(100), nullable=False)
    non_zero_pincodes = db.Column(db.String(500), nullable=False)
    row_indices = db.Column(db.String(500), nullable=False)
    column_indices = db.Column(db.String(500), nullable=False)
    
    @staticmethod
    def retrieve(pincode):
        counter=0
        merchant_ids=[]
        merchants_data={} # intializing a dictionary
        merchants=Merchant.query.all()
        print(merchants)
        for merchant in merchants:
            merchant_id = merchant.merchant_id
            non_zero_pincodes = list(map(int, merchant.non_zero_pincodes.split(',')))
            row_indices = list(map(int, merchant.row_indices.split(',')))
            column_indices = list(map(int, merchant.column_indices.split(',')))
            print(non_zero_pincodes)
            sparse_matrix_csr=sp.csr_matrix((non_zero_pincodes,(row_indices,column_indices)),shape=(max(row_indices)+1,6))
            dense_matrix=sparse_matrix_csr.toarray()
            count=0
            for x in range(len(dense_matrix)):
                are_equal=np.array_equal(dense_matrix[x],pincode)
                if are_equal:
                    count=1
                    break

            if count==1:
                 merchant_ids.append(merchant_id)
                 counter+=1

        if counter==0:
            return 0
        else:
            return merchant_ids

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

    # Find merchants associated with the provided pincode
    #merchants = Merchant.find_merchants_by_pincode(buyer_pincode)
    buyer_pin=list(map(int, buyer_pincode))
    #print(buyer_pin)
    # Retrieve merchant details using the 'retrieve' function
    merchants_details = Merchant.retrieve(buyer_pin)

    # Process data and prepare a response
    response = {
        "status": "success",
        "message": "Buyer data received successfully!",
        "buyer_id": buyer_id,
        "buyer_pass": buyer_pass,
        "buyer_pincode": buyer_pincode
    }
    #print(merchant_details)
    if merchants_details:
        #print(merchants_details)
        #[merchants_ids.append(merchant_details) for merchant_details in merchants_details]
        response["merchants_found"] = merchants_details
        #print(response["merchants_found"])
        #print(merchant_ids)
    #print(jsonify(response))
    return jsonify(response)

@app.route('/submit_merchant', methods=['POST'])
def submit_merchant():
    data=request.json # retrieve json data
    merchant_name = data.get('merchantName')
    merchant_id = data.get('merchantid')
    merchant_pass = data.get('merchantpass')
    pincode_count = data.get('pincodeCount')
    pincode_list = data.get('pincodeList', [])  # Retrieve the pincodeList directly

    matrix_data = []
    rows = []
    cols = []
    current_row_index = 0
    for pin in pincode_list:
        pin_digits=list(map(int,pin))
        non_zero_indices = [i for i, digit in enumerate(pin_digits) if digit != 0]
        matrix_data.extend([digit for i, digit in enumerate(pin_digits) if i in non_zero_indices])
        rows.extend([current_row_index] * len(non_zero_indices))
        cols.extend([i for i in range(len(pin_digits)) if i in non_zero_indices])
        current_row_index +=1

    csr = csr_matrix((matrix_data, (rows, cols)))

    non_zero = csr.data.tolist()
    row_idx = csr.nonzero()[0].tolist()
    col_idx = csr.nonzero()[1].tolist()

    non_zero_pincodes = ','.join(map(str, non_zero))
    row_indices = ','.join(map(str, row_idx))
    column_indices = ','.join(map(str, col_idx))

    pin_obj = Merchant(non_zero_pincodes=non_zero_pincodes, row_indices=row_indices, column_indices=column_indices)

    print("Merchant Name: ",merchant_name)
    print("Merchant ID: ",merchant_id)
    print("Merchant Password: ",merchant_pass)
    print("Merchant Pincodes: ",pincode_list)
    print("Non-zero pincodes: ",non_zero_pincodes)
    print("Row indices: ",row_indices)
    print("Column indices: ",column_indices)

    # Create a new Merchant object
    new_merchant = Merchant(
        merchant_id=merchant_id,
        merchant_name=merchant_name,
        merchant_pass=merchant_pass,
        non_zero_pincodes=non_zero_pincodes,
        row_indices=row_indices,
        column_indices=column_indices
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
        "pincode_list": pincode_list,
        'success': True
    }

    return jsonify(response)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Drop all existing tables
        #db.create_all(bind=['buyer'])  # Create buyer tables based on models
        db.create_all()  # Create tables based on models
    app.run(debug=True)

