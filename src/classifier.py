from feather import read_dataframe, write_dataframe

import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm
from patsy import dmatrices

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Read cleaned line list df.feather (after data_download.py and data_clean.py)
df_imputed = read_dataframe('data/df_imputed.feather')
df_complete_subset = read_dataframe('data/df_complete_subset.feather')
df_complete_subset.dtypes

# to add country' (need one-hot)
col_features = ['age', 'male',
                'wuhan', 'chronic_disease_binary', 'sequence_available',
                'days_onset_outcome', 'days_onset_confirm', 'days_hosp',
                'days_admin_confirm']
target = 'died'

df[col_features]
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
#          Current function value: 0.058198
#          Iterations 11
#                            Logit Regression Results
# ==============================================================================
# Dep. Variable:                   died   No. Observations:                  766
# Model:                          Logit   Df Residuals:                      760
# Method:                           MLE   Df Model:                            5
# Date:                Sun, 09 Feb 2020   Pseudo R-squ.:                  0.7261
# Time:                        22:49:27   Log-Likelihood:                -44.579
# converged:                       True   LL-Null:                       -162.77
# Covariance Type:            nonrobust   LLR p-value:                 4.563e-49
# ==========================================================================================
#                              coef    std err          z      P>|z|      [0.025      0.975]
# ------------------------------------------------------------------------------------------
# Intercept                -14.9645      2.876     -5.203      0.000     -20.602      -9.327
# age                        0.1345      0.032      4.258      0.000       0.073       0.196
# male                       0.8772      0.620      1.414      0.157      -0.338       2.093
# wuhan                      5.1989      0.981      5.297      0.000       3.275       7.122
# china                      0.5520      1.727      0.320      0.749      -2.832       3.936
# chronic_disease_binary     4.8284      1.498      3.223      0.001       1.892       7.765
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
# ==============================================================================
# Dep. Variable:                   died   No. Observations:                15604
# Model:                          Logit   Df Residuals:                    15599
# Method:                           MLE   Df Model:                            4
# Date:                Sun, 09 Feb 2020   Pseudo R-squ.:                  0.6295
# Time:                        22:52:39   Log-Likelihood:                -109.83
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



########### Using sklearn's regularized logit and imputation on df ####################

x_train, x_test, y_train, y_test = train_test_split(df[col_features], df[target], test_size=0.2, random_state=0)
lr = LogisticRegression()
lr.fit(x_train, y_train)

# Returns a NumPy Array
# Predict for One Observation (image)
logisticRegr.predict(x_test[0].reshape(1,-1))

predictions = logisticRegr.predict(x_test)


# Use score method to get accuracy of model
score = logisticRegr.score(x_test, y_test)
print(score)

cm = metrics.confusion_matrix(y_test, predictions)
print(cm)


