from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/draw-card', methods=['POST'])
def draw_card():
    # TODO: Implement card drawing logic
    return jsonify({"message": "Card drawn successfully"})

@app.route('/api/reading', methods=['POST'])
def get_reading():
    # TODO: Implement tarot reading logic
    return jsonify({"message": "Reading generated successfully"})

if __name__ == '__main__':
    app.run(debug=True)
