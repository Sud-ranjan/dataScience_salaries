import flask
from flask import Flask, jsonify, request
import json
import pickle
import pandas as pd
import numpy as np


def load_models():
    file_name = 'models/trained_ml_model.pkl'
    with open(file_name,'rb') as pickled:
        model = pickle.load(pickled)
        # model = data['model']
    return model


app = Flask(__name__)
@app.route('/predict',methods = ['GET'])



def predict():
    # stub input features
    request_json = request.get_json()
    X = request_json['input']
    x_test = np.array(X).reshape(1,-1)

    print(X)
    model = load_models()
    prediction = model.predict(x_test)[0]
    response = json.dumps({'response': prediction})

    # response = json.dumps({'response': 'Hellooooo!!'})
    return response,200

if __name__ == '__main__':
    application.run(debug = True)



