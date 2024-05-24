

from bson import ObjectId
from flask import Flask, jsonify, request
from pymongo import MongoClient


app = Flask(__name__)



# MongoDB configuration
connectionString= "mongodb+srv://hrudayatoraskar:gaCf1QSYMYecYkWo@cluster0.jhj01ce.mongodb.net/"
dbClient =  MongoClient(connectionString)
db = dbClient.Library
collection = db.ApplicationSet     


@app.route('/api/get', methods=['GET'])
def getAll():    
    try:
        results = list(collection.find())
        for result in results:
            result['_id'] = str(result['_id'])  # Convert ObjectId to string for JSON serialization

        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/getbyname', methods=['GET'])
def get_data_by_name():
    name = request.args.get('name')
    results = (collection.find_one({'name': name}))
    
    if results:
         results['_id'] = str(results['_id'])  # Convert ObjectId to string for JSON serialization
         
         return jsonify(results),200
         
    else:
        return jsonify({'error': 'Data not found'}), 404
    
@app.route('/api/add_record', methods=['POST'])
def add_record():
    record = request.json
    try:
        result= (collection.insert_one(record))
        return jsonify({'message': 'Record added successfully'}),201
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
    
@app.route('/api/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        data = request.json
        item_object_id = ObjectId(item_id)  # Convert item_id from string to ObjectId

        update_query = {'_id': item_object_id}
        new_values = {"$set": data}

        result = collection.update_one(update_query, new_values) # Perform the update

        if result.matched_count == 1:
            return jsonify({"msg": "Item updated successfully"}), 200
        else:
            return jsonify({"msg": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/delete_record/<record_id>', methods=['DELETE'])
def delete_record(record_id):   
    try:
        item_object_id = ObjectId(record_id)  # Convert item_id from string to ObjectId
        delete_query = {'_id': item_object_id}
        result= (collection.delete_one(delete_query))
        return jsonify({'message': 'Record deleted successfully'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    