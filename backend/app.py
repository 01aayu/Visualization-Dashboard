from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['data_visualization']  # Use the database name created
collection = db['data']  # Use the collection name created

@app.route('/data', methods=['GET'])
def get_data():
    filters = request.args
    query = {}

    if 'end_year' in filters and filters['end_year']:
        try:
            query['end_year'] = int(filters['end_year'])
        except ValueError:
            return jsonify({"error": "Invalid end_year filter value"}), 400

    if 'topics' in filters and filters['topics']:
        query['topic'] = filters['topics']
    if 'sector' in filters and filters['sector']:
        query['sector'] = filters['sector']
    if 'region' in filters and filters['region']:
        query['region'] = filters['region']
    if 'pest' in filters and filters['pest']:
        query['pestle'] = filters['pest']
    if 'source' in filters and filters['source']:
        query['source'] = filters['source']
    if 'swot' in filters and filters['swot']:
        query['swot'] = filters['swot']
    if 'country' in filters and filters['country']:
        query['country'] = filters['country']
    if 'city' in filters and filters['city']:
        query['city'] = filters['city']

    data = list(collection.find(query))
    for item in data:
        item['_id'] = str(item['_id'])  # Convert ObjectId to string for JSON serialization
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
