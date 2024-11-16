from flask import Flask, request, jsonify, send_file
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
    return jsonify({'message': 'success'})

@app.route('/simplify', methods=['POST'])
def simplify_model():
    arcpy.env.workspace = r"D:\Desktop\cfb\data"
    arcpy.env.overwriteOutput = True
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4548)
    data = request.json
    simplify = Simplify()
    simplify.simplify_params_set(data)
    simplify.simplify()
    return jsonify({'message': 'success'})

@app.route('/neighbor_recognition', methods=['POST'])
def neighbor_recognition_model():
    arcpy.env.workspace = r"D:\Desktop\cfb\data"
    arcpy.env.overwriteOutput = True
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4548)
    data = request.json
    neighborRecognition = NeighborRecognition()
    neighborRecognition.neighbor_recognition_params_set(data)
    neighborRecognition.neighbor_recognition()
    return jsonify({'message': 'success'})

@app.route('/edge_effect_measure', methods=['POST'])
def edge_effect_measure_model():
    arcpy.env.workspace = r"D:\Desktop\cfb\data"
    arcpy.env.overwriteOutput = True
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4548)
    data = request.json
    edgeEffectMeasure = EdgeEffectMeasure()
    edgeEffectMeasure.edge_effect_measure_params_set(data)
    edgeEffectMeasure.edge_effect_measure()
    return send_file(f'D:/Desktop/cfb/data/{data["output_table"]}', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4001)
