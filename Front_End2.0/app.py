from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_url_path='/static')

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
    app.run(debug=True)

