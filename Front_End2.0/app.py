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
    buyer_id = request.form.get('buyerId')
    buyer_pass = request.form.get('buyerPass')
    buyer_pincode = request.form.get('buyerPincode')
    print(buyer_id)
    print(buyer_pass)
    print(buyer_pincode)
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
    merchant_name = request.form.get('merchantName')
    merchant_id = request.form.get('merchantid')
    merchant_pass = request.form.get('merchantpass')
    pincode_count = request.form.get('pincodeCount')
    pincode_list = [request.form.get(f'pincode_{i}') for i in range(1, int(pincode_count)+1)]

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

