# -*- coding: utf-8 -*-

from data_proc import read_structured_data
from data_proc import get_feature
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans

name = "cpu"
structured_data = read_structured_data(name)

x = get_feature(structured_data, 1)
x_norm = (x - x.min()) / (x.max() - x.min())
#x_norm = x
print(x_norm)
lost = []
for k in range(2, 20):
	estimator = KMeans(n_clusters=k)  # 构造聚类器
	estimator.fit(x_norm)  # 聚类
	lost.append(estimator.inertia_)
plt.plot(range(2, 20), lost)
plt.show()

estimator = KMeans(n_clusters=5)  # 构造聚类器
estimator.fit(x_norm)  # 聚类
label_pred = estimator.labels_  # 获取聚类标签
lost.append(estimator.inertia_)
res = pd.DataFrame(index=structured_data.keys(), columns=['label'], data=label_pred)
res.to_csv('result/' + name + '_label.csv', encoding='utf-8')
print(res)

#TODO:不同硬盘index咋办