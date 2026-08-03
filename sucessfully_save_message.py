import tkinter as tk
from tkinter import messagebox


root = tk.Tk()
root.withdraw()


messagebox.showinfo(
    "Good Plan Better Life",
    "Reminder system is working!"
)
from flask import Flask, jsonify, request
from flask_cors import CORS # Requires pip install flask-cors


app = Flask(__name__)
CORS(app) # Allows JavaScript frontend to connect


@app.route('/api/data', methods=['POST'])
def process_data():
    input_data = request.json.get("value")
    return jsonify({"result": f"Python received: {input_data}"})


if __name__ == '__main__':
    app.run(port=5000)





