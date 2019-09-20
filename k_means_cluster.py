# -*- coding: utf-8 -*-

from data_proc import read_structured_data
from data_proc import get_feature
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans

name = "memory"
flag = 0
norm_flag = True
test_flag = False

structured_data = read_structured_data(name)
x = get_feature(structured_data, flag)
if norm_flag:
	x_norm = (x - x.min()) / (x.max() - x.min())
else:
	x_norm = x
pd.set_option('display.max_columns', None)
print(x_norm)
if test_flag:
	plt.figure()
	for i in range(0,6):
		lost = []
		x_tmp = x_norm.iloc[:,i]
		x_tmp = np.array(x_tmp)
		x_tmp = x_tmp.reshape(-1,1)
		for k in range(2, 10):
			estimator = KMeans(n_clusters=k)  # 构造聚类器
			estimator.fit(x_tmp)  # 聚类
			lost.append(estimator.inertia_)
		plt.plot(range(2, 10), lost)

	plt.legend(["mean","var","rms","skew","kurt","boxing"])


	plt.figure()
	for i in range(6,10):
		lost = []
		x_tmp = x_norm.iloc[:,i]
		x_tmp = np.array(x_tmp)
		x_tmp = x_tmp.reshape(-1,1)
		for k in range(2, 10):
			estimator = KMeans(n_clusters=k)  # 构造聚类器
			estimator.fit(x_tmp)  # 聚类
			lost.append(estimator.inertia_)
		plt.plot(range(2, 10), lost)
	plt.legend(["fengzhi","maichong","yudu","lcr","corr_mean"])
	plt.show()
else:
	lost = []
	for k in range(2, 20):
		estimator = KMeans(n_clusters=k)  # 构造聚类器
		estimator.fit(x_norm)  # 聚类
		lost.append(estimator.inertia_)
	plt.plot(range(2, 20), lost)
	plt.show()

	estimator = KMeans(n_clusters=3)  # 构造聚类器
	estimator.fit(x_norm)  # 聚类
	label_pred = estimator.labels_  # 获取聚类标签
	res = pd.DataFrame(index=structured_data.keys(), columns=['label'], data=label_pred)
	if norm_flag:
		res.to_csv('result/' + name + '_norm_label' + str(flag) + '.csv', encoding='utf-8')
	else:
		res.to_csv('result/' + name + '_label' + str(flag) + '.csv', encoding='utf-8')
	print(res)

# TODO:不同硬盘index咋办
