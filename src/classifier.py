from feather import read_dataframe
from utils import *

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm
from patsy import dmatrices

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer, KNNImputer, MissingIndicator
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import balanced_accuracy_score, roc_auc_score, accuracy_score, recall_score, confusion_matrix, SCORERS

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# Read cleaned line list df.feather (after data_download.py and data_clean.py)
df = read_dataframe('data/df.feather')
df_imputed = read_dataframe('data/df_imputed.feather')
df_complete_subset = read_dataframe('data/df_complete_subset.feather')
df_imputed.dtypes
df_complete_subset.dtypes

# reported_market_exposure, sequence_available is too sparse,
col_features = ['age', 'male', 'e_asia', 'country', 'wuhan', 'chronic_disease_binary']
col_days = list(filter(lambda x:'days' in x, df.columns))
#['days_onset_outcome', 'days_onset_confirm', 'days_hosp', 'days_admin_confirm']
target = 'died'

df[col_features].head()
df[target].value_counts(dropna=False).sort_index()


########### Using unregularized logit (from statmodels) on df_complete_subset ########################
# gender is 95% missing (imputation unlikely to work)
# median imputation with age (also 95% missing)
# Apply on df_complete_subset if fitting to male
y, X = dmatrices('died ~ age + male + wuhan + china + chronic_disease_binary', data=df_complete_subset, return_type='dataframe')
logit = sm.Logit(y, X)
mod_complete = logit.fit()
print(mod_complete.summary())

# Risk factors for death: wuhan, chronic illness and age
# Sample may be too small to see signficance for being male and being in China
#
# Optimization terminated successfully.
#          Current function value: 0.060221
#          Iterations 11
# print(mod_complete.summary())
#                            Logit Regression Results
# ==============================================================================
# Dep. Variable:                   died   No. Observations:                  740
# Model:                          Logit   Df Residuals:                      734
# Method:                           MLE   Df Model:                            5
# Date:                Mon, 10 Feb 2020   Pseudo R-squ.:                  0.7237
# Time:                        16:43:53   Log-Likelihood:                -44.564
# converged:                       True   LL-Null:                       -161.28
# Covariance Type:            nonrobust   LLR p-value:                 1.961e-48
# ==========================================================================================
#                              coef    std err          z      P>|z|      [0.025      0.975]
# ------------------------------------------------------------------------------------------
# Intercept                -14.9193      2.890     -5.163      0.000     -20.583      -9.256
# age                        0.1341      0.032      4.243      0.000       0.072       0.196
# male                       0.8758      0.620      1.413      0.158      -0.339       2.091
# wuhan                      5.1866      0.983      5.276      0.000       3.260       7.113
# china                      0.5395      1.732      0.311      0.755      -2.855       3.934
# chronic_disease_binary     4.8133      1.500      3.210      0.001       1.874       7.752
# ==========================================================================================


########### Using unregularized logit (from statmodels) on df_impute but drop male (95% missing)  ####################
y, X = dmatrices('died ~ age + wuhan + china + chronic_disease_binary', data=df_imputed, return_type='dataframe')
logit = sm.Logit(y, X)
mod_imputed = logit.fit()
print(mod_imputed.summary())

# Risk factors for death: chronic illness, wuhan and age
# Sample may be too small to see signficance for being male and being in China
#
# Optimization terminated successfully.
#          Current function value: 0.007038
#          Iterations 13
# print(mod_imputed.summary())
#                            Logit Regression Results
# ==============================================================================
# Dep. Variable:                   died   No. Observations:                15604
# Model:                          Logit   Df Residuals:                    15599
# Method:                           MLE   Df Model:                            4
# Date:                Mon, 10 Feb 2020   Pseudo R-squ.:                  0.6295
# Time:                        16:46:41   Log-Likelihood:                -109.83
# converged:                       True   LL-Null:                       -296.39
# Covariance Type:            nonrobust   LLR p-value:                 1.782e-79
# ==========================================================================================
#                              coef    std err          z      P>|z|      [0.025      0.975]
# ------------------------------------------------------------------------------------------
# Intercept                -20.2222      2.258     -8.957      0.000     -24.647     -15.797
# age                        0.1946      0.019     10.450      0.000       0.158       0.231
# wuhan                      3.2612      0.704      4.635      0.000       1.882       4.640
# china                      1.3237      1.881      0.704      0.482      -2.363       5.010
# chronic_disease_binary     6.6814      1.223      5.462      0.000       4.284       9.079
# ==========================================================================================




########### Using sklearn's regularized logit on df_imputed ####################
# use df_impute to mamually impute age, ['male','china','wuhan'] (faster and simpler!)
# imputation done in data_clean.py
# just need to do one-hot encoding on country
df_imputed.country.value_counts(dropna=False)           #27 countries
len(set(df_imputed.country))
ohe = OneHotEncoder(drop='first', dtype='int', sparse=False)
ohe_country = ohe.fit_transform(df_imputed.country._values.reshape(-1, 1))
ohe_country.shape                                       #26 countries
ohe_df =  pd.DataFrame(ohe_country, columns=ohe.categories_[0][1:], dtype='int')
df_imputed = pd.concat([df_imputed.drop(columns='country'),
                        ohe_df],
                       axis=1)
df_imputed.columns

# Split data into training and test sets
col_used = col_features + ohe_df.columns.values.tolist()
col_used = [x for x in col_used if x not in {'country','china'}]
x_train, x_test, y_train, y_test = train_test_split(df_imputed[col_used],
                                                    df_imputed[target],test_size=0.2, random_state=0)

# Tune for optimal lambda
lr_cv = LogisticRegressionCV(Cs = 20, cv=10, penalty='l1', solver='saga',class_weight='balanced',
                             max_iter=100000, random_state=0, scoring='balanced_accuracy').fit(x_train, y_train)
best_C, score_type, scores_df = bestLambda_lrcv(lr_cv, plot=True)
best_C   #best C (4.3 if unbalanced class weight, 206.91 if balanced class weight)
1/best_C #best lambda (0.23 if unbalanced class weight, 0.0048 if balanced class weight)

# Fit lr to optimal lambda
lr = LogisticRegression(C=best_C, penalty='l1', solver='saga', max_iter=10000, class_weight='balanced')
lr_results = lr.fit(x_train, y_train)

coef_series = sk_mod_summary(lr_results, list(x_train.columns.values))
coef_series
# age                        1.970138
# male                       0.246590
# e_asia                   -34.076842
# wuhan                      2.483723
# chronic_disease_binary    85.198255
# Australia                 -1.283972
# Belgium                   -0.122400
# Cambodia                  -0.121003
# Canada                    -0.477260
# China                    -26.494932
# Finland                    0.000000
# France                    -0.604424
# Germany                   -1.326027
# India                     -0.116803
# Italy                     -0.238722
# Japan                     -3.458126
# Malaysia                  -0.591860
# Nepal                     -0.118072
# Philippines                3.504032
# Russia                    -0.239357
# Singapore                 -1.848598
# South Korea               -1.593051
# Spain                     -0.118628
# Sri Lanka                 -0.119137
# Sweden                    -0.113273
# Taiwan                    -0.359567
# Thailand                  -2.612527
# UAE                       -0.481555
# United Kingdom            -0.355992
# United States             -1.210166
# Vietnam                   -0.614444
# NB: wuhan, china, e_asia are highly correlated  -> elnet may be bettter

logit_pvalue(lr, x_train)   #TODO: illconditioning

predictions = lr.predict(x_test)
probabilities = pd.DataFrame(lr.predict_proba(x_test))[1]

accuracy = lr.score(x_test,y_test)              #0.97
roc_auc_score(y_test, probabilities)            #0.98
balanced_accuracy_score(y_test, predictions)    #0.98
recall_score(y_test, predictions, None)

cm = confusion_matrix(y_test, predictions)
print(cm)


##### Using Pipeline and ColumnTransformer (too slow!)
#
# Assemble the transformers for the preprocessor
# Needs a triple tuple (name, transformer, columns) in ColumnTransformer()
# Nested within is a transformer double tuple (name, transform)
#
# preprocessor_age = SimpleImputer(strategy='constant', fill_value=50)
# preprocessor_country = OneHotEncoder(categorical_features = [0], drop='first', dtype='int')
# preprocessor_bin = Pipeline(steps=[ ('imputer', KNNImputer(n_neighbors=3, weights="uniform")),
#                                     ('round', FunctionTransformer(np.round))
#                                     ])
# preprocessor = ColumnTransformer(transformers=[ ('age', preprocessor_age, 'age'),
#                                                 ('country', preprocessor_country, 'country'),
#                                                 ('preprocessor_bin', preprocessor_bin, ['male','china','wuhan'])
#                                                ])
#
# # Assemble the pipeline
# pl_lr = Pipeline(steps=[('preprocessor', preprocessor),
#                       ('classifier', LogisticRegression(penalty='l1', solver='saga', max_iter=1000000, class_weight='balanced'))])
#
# # Fit pipeline to training data
# pl_lr.fit(x_train, y_train)
#
# # Review the fit
# stepnames, classifier_pos = sk_pipeline_step_names(pl_lr)
# coef_series = sk_mod_summary(pl_lr[classifier_pos], list(x_train.columns.values))
# sk_mod_summary(lr_results, list(x_train.columns.values))
