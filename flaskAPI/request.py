import requests
import pandas as pd
# import numpy as np

URL = 'http://127.0.0.1:5000/predict'


test_data = pd.read_csv('X_test.csv').drop(['Unnamed: 0'], axis = 1)
row_number = 12

data_single_row = list(test_data.iloc[row_number,:])

PARAMS = {'Content-type': 'application/json '}
data = {'input':data_single_row}
 
r = requests.get(URL, headers=PARAMS, json = data)
result = r.json()

# print salary
predicted_salary = int(result['response'])
print("Predicted Salary = $ {}K".format(predicted_salary))

# print(np.array(data['input']).reshape(1,-1))