from flask import Flask, request, jsonify
import mysql.connector
from my_db_package.db_connection import establish_connection
app = Flask(__name__)

# Establishing the connection to MySQL
# Replace 'username', 'password', 'host', and 'database_name' with your credentials
connection = establish_connection()
'''connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='enter_your_password',
    database='pin_code_store'
)'''

if connection.is_connected():
    print("Connected to MySQL database")

# Endpoint to handle pin code retrieval and storing it in the database
@app.route("/retrieve_pincode", methods=["POST"])
def handle_retrieve_pincode():
    pincode = request.json.get("pincode")
    if pincode:
        # Inserting the pincode into the database
        cursor = connection.cursor()
        insert_query = "INSERT INTO pin_codes (pincode) VALUES (%s)"
        data = (pincode,)
        cursor.execute(insert_query, data)
        connection.commit()
        cursor.close()

        return jsonify({"message": f"Pin code {pincode} inserted into the database."})
    else:
        return jsonify({"message": "Please provide a pincode."}), 400

# Endpoint to retrieve pin code from the database
@app.route("/get_pincode", methods=["GET"])
def get_pincode():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pin_codes")
    rows = cursor.fetchall()
    cursor.close()

    return jsonify({"pin_codes": rows})

if __name__ == "__main__":
    app.run(debug=True)
