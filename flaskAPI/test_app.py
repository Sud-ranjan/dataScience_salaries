import pandas as pd

# getting test data into the app to check model predictions
df = pd.read_csv('../explored_data_for_model.csv')
df_model = df[['avg_salary','Rating','Size','Type of ownership','employer_provided','Industry', 'Sector', 'Revenue','num_comp','hourly','job_state','same_state_as_hq','company_age','python_yn', 'spark_yn', 'cloud_yn', 'deployments_yn',
       'viz_tools_yn', 'api_dev_yn','job_title_simplified', 'seniority','jd_length']]

bool_columns = df_model.select_dtypes(include='bool').columns
df_model[bool_columns] = df_model[bool_columns].astype(int)

df_dum = pd.get_dummies(df_model)
from sklearn.model_selection import train_test_split

X = df_dum.drop(['avg_salary'], axis = 1)
y = df_dum.avg_salary.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#TODO__: Format incoming data in correct format for model to ingest
# -----
# -----
# -----
X_test.to_csv('X_test.csv')
import pickle

# Load the pickled model from the file
with open('models/trained_ml_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Use the loaded model to make predictions
predictions = model.predict(X_test)

from sklearn.metrics import mean_absolute_error

print('Random Forest mse = ',mean_absolute_error(y_test,predictions))

