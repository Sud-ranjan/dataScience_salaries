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

def read_city_state_data():
    usa_geo = pd.read_csv('/Users/sudhanshuranjan/Documents/dataScience_salaries/Helper Datasets/uscities.csv')
    cities = usa_geo.city.unique()
    states = usa_geo.state_name.unique()
    usa_geo_data = { 'states' : states,'cities': cities}
    return usa_geo_data

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
    
    data = request.form 
    print(data)
    form_data = { 
        'Job Title': data['jobTitle'],
        'Salary Estimate': data['jobDescription'],
        'Job Description': data['rating'],
        'Rating': data['companyName'],
        'Company Name': data['state'],
        'Location': data['city'],
        'Headquarters State': data['hqState'],
        'Headquarters City': data['hqCity'],
        'Size': data['company-size'],
        'Founded': data['jobTitle'],
        'Type of ownership': data['ownership'],
        'Industry': data['industry'],
        'Sector': data['sector'],
        'Revenue': data['revenue'],
        'Competitors': data['competitors']
    } 
    return jsonify({"message": "Data submitted, awaiting processing and prediction route build"}), 200


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



