import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('explored_data_for_model.csv')
to_drop = [col for col in df.columns if 'unnamed' in col.lower()]

df = df.drop(columns=to_drop)

features = ['Rating','Size','Type of ownership','Industry', 'Sector', 'Revenue','num_comp','job_state','same_state_as_hq','company_text',
            'company_age','python_yn', 'spark_yn', 'cloud_yn','deployments_yn','viz_tools_yn', 'api_dev_yn','job_title_simplified', 'seniority','jd_length']


#Segregating variables
numerical_features = df[features].select_dtypes(include=np.number).columns.to_list()
categorical_features = df[features].select_dtypes(include='object').columns.to_list()
bool_features = [x for x in features if x not in numerical_features and x not in categorical_features]
df[bool_features] = df[bool_features].astype(int) #Converting bool features to int
numerical_features = numerical_features + bool_features

nominal = ['Size', 'Revenue']
ordinal = [x for x in categorical_features if x not in nominal]


# Fitting all the data into the model (already crossvalidated)
y = df['avg_salary']
X = df[features]

# Creating Encoding pipelines for different types of variables
from sklearn.pipeline import Pipeline, make_pipeline 
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, OrdinalEncoder, FunctionTransformer, MinMaxScaler, PowerTransformer, KBinsDiscretizer, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_validate

ordinal_pipeline = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)                  #categories=[['Yes','No']]*len(ordinal)), MinMaxScaler()
nominal_pipeline = OneHotEncoder(drop='first', handle_unknown = 'ignore')
numeric_pipeline = make_pipeline(PowerTransformer('yeo-johnson'), MinMaxScaler())


preprocessing_pipeline = ColumnTransformer(transformers=[
    ('ordinal_pipeline',ordinal_pipeline,ordinal),
    ('nominal_pipeline',nominal_pipeline,nominal),
    ('numeric_pipeline',numeric_pipeline,numerical_features)
])


from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm
from sklearn import tree

models= {
    'LR':LinearRegression(),
    'RF':RandomForestRegressor(),           #try 'XGB': XGBClassifier(),
    'DTregressor': tree.DecisionTreeRegressor(),
    'svm':svm.SVR(),
    'Lasso':Lasso(alpha=0.5)
    }

result = []
for name,model in models.items():
    final_pipeline = make_pipeline(preprocessing_pipeline,model)
    cv = cross_validate(final_pipeline,X,y, cv = 5, return_train_score=True, scoring='neg_mean_absolute_error')
    result.append(pd.DataFrame(cv).mean().to_frame().set_axis([name],axis = 1))

scores = pd.concat(result, axis = 1)
print(scores)



# hyperparameter tuning for the best model - RF

from sklearn.model_selection import GridSearchCV

#selecting best model:
model = RandomForestRegressor()
final_pipeline = make_pipeline(preprocessing_pipeline,model)
param_grid = {
    'randomforestregressor__n_estimators': range(10,100,10),#    'criterion': ('squared_error','absolute_error'),
    'randomforestregressor__max_features': ('sqrt','log2'),
    'randomforestregressor__min_samples_split': range(5,10,1),
    'randomforestregressor__ccp_alpha': np.arange(0, 1.1, 0.1, dtype=float)
}

grid_search = GridSearchCV(final_pipeline, param_grid=param_grid, cv=5, scoring='neg_mean_absolute_error')
grid_search.fit(X,y)



model = grid_search.best_estimator_

import pickle

model_file_path =  '/Users/sudhanshuranjan/Documents/dataScience_salaries/flaskAPI/models/RF_model_pipelined.pkl'

with open(model_file_path, 'wb') as file:
    pickle.dump(model, file)


