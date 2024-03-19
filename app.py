from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://mongodb:27017/')
db = client['employees']
collection = db['employee_data']

# API routes
@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    employee_id = collection.insert_one(data).inserted_id
    return jsonify({'message': 'Employee created successfully', 'employee_id': str(employee_id)}), 201

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = list(collection.find())
    for emp in employees:
        emp['_id'] = str(emp['_id'])
    return jsonify({'employees': employees}), 200

@app.route('/employees/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.json
    result = collection.update_one({'_id': ObjectId(employee_id)}, {'$set': data})
    if result.modified_count == 1:
        return jsonify({'message': 'Employee updated successfully'}), 200
    else:
        return jsonify({'error': 'Employee not found'}), 404

@app.route('/employees/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    result = collection.delete_one({'_id': ObjectId(employee_id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Employee deleted successfully'}), 200
    else:
        return jsonify({'error': 'Employee not found'}), 404








if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
