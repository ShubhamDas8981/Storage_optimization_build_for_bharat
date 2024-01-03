from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from scipy.sparse import csr_matrix
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pincodes.db'
db = SQLAlchemy(app)

class Pincode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    non_zero_values = db.Column(db.String, nullable=False)
    row_indices = db.Column(db.String, nullable=False)
    col_indices = db.Column(db.String, nullable=False)
'''
@app.route('/process_pincodes', methods=['POST'])
def process_pincodes():
    data = request.get_json()
    pincodes = data.get('pincodes', [])

    matrix_data = []
    rows = []
    cols = []

    for pin in pincodes:
        matrix_data.extend(list(map(int, pin)))
        rows.extend([len(rows)] * len(pin))
        cols.extend(range(len(pin)))

    csr = csr_matrix((matrix_data, (rows, cols)))

    non_zero = csr.data.tolist()
    row_idx = csr.nonzero()[0].tolist()
    col_idx = csr.nonzero()[1].tolist()

    non_zero_str = ','.join(map(str, non_zero))
    row_idx_str = ','.join(map(str, row_idx))
    col_idx_str = ','.join(map(str, col_idx))

    pin_obj = Pincode(non_zero_values=non_zero_str, row_indices=row_idx_str, col_indices=col_idx_str)
    db.session.add(pin_obj)
    db.session.commit()

    return jsonify({'success': True})
'''
@app.route('/process_pincodes', methods=['POST'])
def process_pincodes():
    data = request.get_json()
    pincodes = data.get('pincodes', [])

    matrix_data = []
    rows = []
    cols = []
    current_row_index = 0
    for pin in pincodes:
        pin_digits = list(map(int, pin))
        non_zero_indices = [i for i, digit in enumerate(pin_digits) if digit != 0]
        matrix_data.extend([digit for i, digit in enumerate(pin_digits) if i in non_zero_indices])
        #rows.extend([len(rows)] * len(non_zero_indices))
        rows.extend([current_row_index] * len(non_zero_indices))
        cols.extend([i for i in range(len(pin_digits)) if i in non_zero_indices])
        current_row_index +=1

    csr = csr_matrix((matrix_data, (rows, cols)))

    non_zero = csr.data.tolist()
    row_idx = csr.nonzero()[0].tolist()
    col_idx = csr.nonzero()[1].tolist()

    non_zero_str = ','.join(map(str, non_zero))
    row_idx_str = ','.join(map(str, row_idx))
    col_idx_str = ','.join(map(str, col_idx))

    pin_obj = Pincode(non_zero_values=non_zero_str, row_indices=row_idx_str, col_indices=col_idx_str)
    db.session.add(pin_obj)
    db.session.commit()

    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=True)









