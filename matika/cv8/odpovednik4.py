from scipy.stats import randint, bernoulli, geom, binom, poisson, uniform, expon, norm 
import numpy as np
from math import exp, sqrt
import matplotlib.pyplot as plt
import pandas as pd
import itertools
from icecream import ic

data = pd.read_csv(r"data.csv")
print(np.mean(data["height"]))
print(np.var(data["height"]))

q_025 = np.quantile(data["weight"], 0.25, method = 'inverted_cdf')
print(q_025)

n = len(data)
X  = data["weight"]
median = np.quantile(X, 0.5, method = 'inverted_cdf')
q_025 = np.quantile(X, 0.25, method = 'inverted_cdf')
q_075 = np.quantile(X, 0.75, method = 'inverted_cdf')
IQR = q_075 - q_025 # kvartilova odchylka

dvnh = q_025 - 1.5 * IQR # dolni vnitrni hradba
hvnh = q_075 + 1.5 * IQR# horni vnitrni hradba
dvoh = q_025 - 3 * IQR# dolni vonkajsi hradba
hvoh = q_075 + 3 * IQR# horni vonkajsi hradba

# plt.boxplot(X, vert = False)
# y = np.random.normal(1, 0.04, len(X))
# plt.scatter(X, y)
# plt.title("Boxplot")
# plt.savefig('boxplot_grah.png')

number_of_bins = 5
counts, intervals = np.histogram(data["BMI"], bins=number_of_bins, range=(15.001, 40.001), density=None, weights=None)
ic(len(counts), len(intervals), counts, intervals)


for iii in range(0, 25, 5):
    print(len([x for x in data["BMI"] if x > 15+iii and x <=20+iii]) / n)

data2 = pd.DataFrame(list(zip(intervals[:-1], intervals[1:], counts)),columns =['start', 'end', 'counts'])
data2["ECDF"] = data2["counts"] / n

data2["popis"] = round(data2["start"]).astype(str) + "-" + round(data2["end"]).astype(str)
plt.scatter(data2["popis"], data2["ECDF"], label='Polygon cetnosti', ec = "blue")
plt.plot(data2["popis"], data2["ECDF"], label='Polygon cetnosti')
plt.title("Polygon relativni cetnosti")
plt.savefig('polygon_grap.png')
ic(data2)
