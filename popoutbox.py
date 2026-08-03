from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage for different categories
data_store = {
    "timetable": [],
    "time": [],
    "events": []
}

@app.route('/api/save', methods=['POST'])
def save_data():
    data = request.json
    category = data.get("category")

    if category in data_store:
        data_store[category].append(data)
        print(f"Saved to '{category}':", data)
        return jsonify({
            "status": "success",
            "message": f"Successfully recorded in {category.capitalize()}!",
            "data": data_store[category]
        })
    
    return jsonify({"status": "error", "message": "Invalid category"}), 400

@app.route('/api/records', methods=['GET'])
def get_records():
    """Returns all stored records for front-end checking."""
    return jsonify(data_store)

if __name__ == '__main__':
    print("Starting Flask backend on http://127.0.0.1:5000...")
    app.run(port=5000, debug=True)