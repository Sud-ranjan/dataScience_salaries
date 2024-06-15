import flask
from flask import Flask, jsonify, request, render_template, session
import json
import pickle
import pandas as pd
import numpy as np
from dash_application import create_dash_app

def load_models():
    file_name = 'models/trained_ml_model.pkl'
    with open(file_name,'rb') as pickled:
        model = pickle.load(pickled)
        # model = data['model']
    return model


server = Flask(__name__)
dash_app = create_dash_app(server)


@server.route('/')
def index():
    print("Homepage requested")
    return "Hello from flask homepage"

@server.route('/dash')
def dash_page():
    return dash_app.index()
    # return 'Hello This is Dash Dashboard'

@server.route('/predict',methods = ['GET'])
def predict():
    # stub input features
    request_json = request.get_json()
    X = request_json['input']
    x_test = np.array(X).reshape(1,-1)
    model = load_models()
    prediction = model.predict(x_test)[0]
    response = json.dumps({'response': prediction})

    return response,200

if __name__ == '__main__':
    server.run(debug = True)



