import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from model.tools import *
from publish import Publisher

app = Flask(__name__)
CORS(app)

@app.route('/publish', methods=['POST'])
def publish():
    data = request.json
    publisher = Publisher()
    publisher.publish_params_set(data)
    publisher.publish()
    return jsonify({'message': 'Publish success'})

@app.route('/simplify', methods=['POST'])
def simplify_model():
    data = request.json
    simplify = Simplify()
    simplify.simplify_params_set(data)
    simplify.simplify()
    return jsonify({'message': 'Publish success'})

@app.route('/neighbor_recognition', methods=['POST'])
def neighbor_recognition_model():
    data = request.json
    neighborRecognition = NeighborRecognition()
    neighborRecognition.neighbor_recognition_params_set(data)
    neighborRecognition.neighbor_recognition()
    return jsonify({'message': 'Publish success'})

@app.route('/edge_effect_measure', methods=['POST'])
def edge_effect_measure_model():
    data = request.json
    edgeEffectMeasure = EdgeEffectMeasure()
    edgeEffectMeasure.edge_effect_measure_params_set(data)
    edgeEffectMeasure.edge_effect_measure()
    return jsonify({'message': 'Publish success'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4001)
