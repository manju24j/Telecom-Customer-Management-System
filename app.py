from datetime import datetime
from flask import Flask, request, jsonify,render_template
import json
from flask_cors import CORS ,cross_origin
app = Flask(__name__)

CORS(app)

# Sample data for demonstration purposes
CUSTOMERS_DATA = 'customers.json'


customers = [
    {   "id": 1,
        "name": "John Doe",
        "dob": "1990-01-01",
        "email": "john.doe@example.com",
        "adhar_number": "123456789012",
        "registration_date": "2022-01-01",
        "mobile_number": "1234567890",
        "plan": {
            "name": "Platinum365",
            "cost": 499,
            "validity": 365,
            "status": "Active"
        },
        'renewal_date': '',
        'upgrade_downgrade': ''        
    }
]

@app.route("/")
def index():
    return render_template('home.html')


@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/register_customer", methods=["POST"])
def register_customer():
    try:
        with open(CUSTOMERS_DATA) as f:
            customers = json.load(f)
            print("from file",customers)
        customer_data = request.get_json()
        customer_id = len(customers) + 1
        customer = {
            "id": customer_id,
            "name": customer_data["name"],
            "dob": customer_data["dob"],
            "email": customer_data["email"],
            "adhar_number": customer_data["adhar_number"],
            "registration_date": customer_data["registration_date"],
            "mobile_number": customer_data["mobile_number"],
            "plan": {
                "name": customer_data["plan"]["name"],
                "cost": customer_data["plan"]["cost"],
                "validity": customer_data["plan"]["validity"],
                "status": customer_data["plan"]["status"]
            },
        }
        # print(customer)
        customers.append(customer)
        print (type(customers),customers)
        with open('customers.json', 'w') as f:
            json.dump(customers, f, indent=4)

        return jsonify({"message": "Customer registered successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return redirect(url_for('customer_details', id=customer_data['id']))

@app.route('/customer_details/<int:id>')
def customer_details(id):
    # read customer details from the JSON file
    with open('customers.json', 'r') as f:
        customers = json.load(f)

    customer_data = next((customer for customer in customers if customer['id'] == id), None)
    return jsonify(customer_data)


@app.route("/customers", methods=["GET"])
def get_customers():
    with open('customers.json', 'r') as f:
        customers = json.load(f)
    return render_template('customer_list.html',customers=customers)

    # return jsonify(customers)


@app.route('/display_customer_table', methods=['GET'])
def display_customer_table():
    return render_template('customer_table.html')

@app.route('/display_customer_details/<int:customer_id>', methods=['GET'])
@cross_origin()
def display_customer_details(customer_id):
    print("displaycustomers")
    print(customer_id)
    with open('customers.json', 'r') as f:
        customers = json.load(f)
    customer_data = next((customer for customer in customers if customer['id'] == customer_id), None)
    if customer_data is not None:
        return jsonify(customer_data)
        return render_template('customer_list.html',customers=customer_data)
    else:
        return render_template('customer_table.html')

@app.route('/get_customer_details/<int:customer_id>', methods=['GET'])
@cross_origin()
def get_customer_details(customer_id):
    print("displaycustomers")
    print(customer_id)
    with open('customers.json', 'r') as f:
        customers = json.load(f)
    customer_data = next((customer for customer in customers if customer['id'] == customer_id), None)
    if customer_data is not None:
        return render_template('customer_details.html',customers=customer_data)
    else:
        return render_template('customer_table.html')


@app.route("/renew_plan", methods=["PUT"])
def renew():
    try:
        request_data = request.get_json()
        print(request_data)
        customer_id = request_data["id"]
        renewal_date = datetime.now()
        customer_data = next((customer for customer in customers if customer['id'] == customer_id), None)
        customers[index]["plan"]["status"] = "Active"
        customers[index]["plan"]["renewal_date"] = renewal_date
        return jsonify({"message": "Plan renewed successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)

