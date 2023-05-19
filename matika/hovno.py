from icecream import ic
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd  


data = pd.read_csv(r'dataPy2.csv')
print(data.head())


PREDICTED = 'zasoba.TP' 
PREDICTED_BY = 'spotreba.TP'
data = data.sort_values(by=PREDICTED_BY)
data.head()


# ic(data)
X = data[PREDICTED_BY].tolist()
Y = data[PREDICTED].tolist()
# ic(X, Y)
plt.scatter(X, Y)


#Jednoduchšia verzia ak potrebujete iba jednoduchý graf a predikciu

# parametre sú X, Y a nakoniec stupen polynómu aký chcete

import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
polynomial_features= PolynomialFeatures(degree=1)
XP = polynomial_features.fit_transform(data[PREDICTED_BY].values.reshape((-1, 1)))
# ic(XP)

model = sm.OLS(Y,XP).fit()
model.summary(alpha=0.05)
print("R^2: ", model.rsquared)
print("Adjusted R^2: ", model.rsquared_adj)

X_plot = np.arange(0,14,1)
X_plotP = polynomial_features.fit_transform(X_plot.reshape((-1, 1)))
pred_ols = model.get_prediction(X_plotP)
iv_l = pred_ols.summary_frame(alpha=0.1)["obs_ci_lower"]
iv_u = pred_ols.summary_frame(alpha=0.1)["obs_ci_upper"]
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(X, Y, "o", label="data")
ax.plot(X_plot, pred_ols.predicted_mean, label="OLS")
ax.plot(X_plot, iv_u, "r--")
ax.plot(X_plot, iv_l, "r--")

plt.xlabel("spotreba TP")
plt.ylabel("zasoba TP")
plt.savefig("L_graf.png")

#############################################################################
#############################################################################

coeficients = np.polyfit(X, Y, deg=1)
mymodel = np.poly1d(coeficients)
print("Predikcia pre hodnotu 2:", mymodel(2))

import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
polynomial_features= PolynomialFeatures(degree=2)
XP = polynomial_features.fit_transform(data[PREDICTED_BY].values.reshape((-1, 1)))
# ic(XP)
model = sm.OLS(Y,XP).fit()
model.summary(alpha=0.05)

X_plot = np.arange(0,14,1)
X_plotP = polynomial_features.fit_transform(X_plot.reshape((-1, 1)))
pred_ols = model.get_prediction(X_plotP)
iv_l = pred_ols.summary_frame(alpha=0.1)["obs_ci_lower"]
iv_u = pred_ols.summary_frame(alpha=0.1)["obs_ci_upper"]
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(X, Y, "o", label="data")
ax.plot(X_plot, pred_ols.predicted_mean, label="OLS")
ax.plot(X_plot, iv_u, "r--")
ax.plot(X_plot, iv_l, "r--")

plt.xlabel("spotreba TP")
plt.ylabel("zasoba TP")
plt.savefig("K_graf.png")