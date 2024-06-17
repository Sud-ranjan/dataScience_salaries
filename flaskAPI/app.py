import flask
from flask import Flask, jsonify, request, render_template, session
import requests
import json
import pickle
import pandas as pd
import numpy as np
from dash_application import create_dash_app
from data_preprocessor import parse_input

def load_models():
    file_name = 'models/RF_model_pipelined.pkl'
    with open(file_name,'rb') as pickled:
        model = pickle.load(pickled)
        # model = data['model']
    return model

def read_city_state_data():
    usa_geo = pd.read_csv('/Users/sudhanshuranjan/Documents/dataScience_salaries/Helper Datasets/uscities.csv')
    cities = usa_geo.city.unique()
    states = usa_geo.state_name.unique()
    usa_geo_data = { 'states' : states,'cities': cities}
    return usa_geo_data

def preprocessor_for_predicting(df_form):
    x_test = parse_input(df_form)
    x_test_json = x_test.to_json()
    return x_test_json


server = Flask(__name__)
dash_app = create_dash_app(server)


@server.route('/')
def index():
    name = 'Admin'
    usa_geo_data = read_city_state_data()
    print("Homepage requested")
    return render_template('index.html', data = usa_geo_data)

# `read-form` endpoint  
@server.route('/read-form', methods=['POST']) 
def read_form(): 

    # Get the form data as Python ImmutableDict datatype  
    form_Data = request.form
    df_form = pd.DataFrame(form_Data, index=[0])            #converted to dataframe for preprocessing
    
    x_test_json = preprocessor_for_predicting(df_form)      #got back jsonified data from preprocessor

    PARAMS = {'Content-type': 'application/json '}
    data = {'input':x_test_json}
    URL = 'http://127.0.0.1:5000/predict'


    r = requests.get(URL, headers=PARAMS, json = data)      #Requesting prediction passing jsonified data
    print(r)
    result = r.json()
    return result

@server.route('/dash')
def dash_page():
    return dash_app.index()
    # return 'Hello This is Dash Dashboard'

@server.route('/predict',methods = ['GET'])
def predict():
    # stub input features
    request_json = request.get_json()                       #parsing json from the request
    X = request_json['input']                               #parsing out the x_test data from request json
    
    print(X)
    x_test = pd.read_json(X)
    print(x_test)

    model = load_models()
    prediction = model.predict(x_test)[0]
    print(prediction)
    response = json.dumps({'response': prediction})

    return response

if __name__ == '__main__':
    server.run(debug = True)



