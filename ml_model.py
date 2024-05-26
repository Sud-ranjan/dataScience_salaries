import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('explored_data_for_model.csv')

#Todo:
#choose relevant cols - Done
#get dummy data - Done
#train test split - Done
#multi-linear regression - Done
#lasso regression - Done
#randomforest - Done
#tune hyperparameters with gridSearchCV - Done
#test ensamble models - Done


#choose relevant cols------------------------------
df_model = df[['avg_salary','Rating','Size','Type of ownership','employer_provided','Industry', 'Sector', 'Revenue','num_comp','hourly','job_state','same_state_as_hq','company_age','python_yn', 'spark_yn', 'cloud_yn', 'deployments_yn',
       'viz_tools_yn', 'api_dev_yn','job_title_simplified', 'seniority','jd_length']]

#convert booleans to int
bool_columns = df_model.select_dtypes(include='bool').columns
df_model[bool_columns] = df_model[bool_columns].astype(int)

#get dummy data------------------------------
df_dum = pd.get_dummies(df_model)



#train test split------------------------------
from sklearn.model_selection import train_test_split

X = df_dum.drop(['avg_salary'], axis = 1)
y = df_dum.avg_salary.values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#multi-linear regression------------------------------
# using statsmodel ols model
import statsmodels.api as sm

X_sm = sm.add_constant(X)
model = sm.OLS(y,X_sm)

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train,y_train)
lm_scores = np.mean(cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv = 3))

print('Linear Regression',lm_scores)


#lasso regression------------------------------
alpha = []
mse_lasso = []

for i in range(1,100):
    alpha.append(i/100)
    lm_l = Lasso(alpha=i/100)
    mse_lasso.append(np.mean(cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv = 3)))


lm_lasso_errors = tuple(zip(alpha,mse_lasso))
df_lm_lasso_errors = pd.DataFrame(lm_lasso_errors,columns = ['alpha','error'])

opt_alpha = df_lm_lasso_errors[df_lm_lasso_errors.error == max(df_lm_lasso_errors.error )]
opt_alpha.reset_index(drop=True, inplace = True)

lm_lasso = Lasso(opt_alpha['alpha'][0]) 
lm_lasso.fit(X_train,y_train)
lm_lasso_scores = np.mean(cross_val_score(lm_lasso, X_train, y_train, scoring='neg_mean_absolute_error', cv = 3))

print('Lasso Regression',lm_lasso_scores)


#randomforest------------------------------
from sklearn.ensemble import RandomForestRegressor

rf_model = RandomForestRegressor()
rf_model_score = np.mean(cross_val_score(rf_model, X_train, y_train, scoring='neg_mean_absolute_error', cv = 3))

print('Random Forest', rf_model_score)


#tune hyperparameters with gridSearchCV------------------------------
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': range(10,300,10),
    'criterion': ('squared_error','absolute_error'),
    'max_features': ('auto','sqrt','log2')
}

# Create GridSearchCV object
grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, scoring='neg_mean_absolute_error')

# Fit the GridSearchCV object to the training data
grid_search.fit(X_train, y_train)

# Get the best hyperparameters
best_params = grid_search.best_params_


#test ensamble ------------------------------
y_pred_lm = lm.predict(X_test)
y_pred_lm_lasso = lm_lasso.predict(X_test)
y_pred_rf = grid_search.best_estimator_.predict(X_test)


from sklearn.metrics import mean_absolute_error
print('Linear Regression mse = ',mean_absolute_error(y_test,y_pred_lm))
print('Lasso Regression mse = ',mean_absolute_error(y_test,y_pred_lm_lasso))
print('Random Forest mse = ',mean_absolute_error(y_test,y_pred_rf))
# print(grid_search.best_estimator_)

print('Combined Random Forest with lasso mse = ',mean_absolute_error(y_test,(y_pred_rf+y_pred_lm_lasso)/2))

import pickle

with open('./flaskAPI/models/trained_ml_model.pkl', 'wb') as f:
    pickle.dump(grid_search.best_estimator_,f)

print("successfully exported model. \n Model details:", grid_search.best_estimator_)


# Creating x_test separately to test flask app:
X_test.to_csv('X_test.csv')