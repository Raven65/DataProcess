# -*- coding: utf-8 -*-
import pandas as pd
import math
import numpy as np


def read_structured_data(name: str):
	dff = pd.DataFrame()
	if name == "memory":
		name = "memoryUsed"
		dff = pd.read_csv("./data/memoryTotal.csv")
	df = pd.read_csv("./data/" + name + ".csv")
	object_id = df['object_id'].drop_duplicates().tolist()
	data = {}
	for oi in object_id:
		df2 = df.loc[df['object_id'] == oi]
		df2 = df2.drop_duplicates()
		index = df2['disk_index'].drop_duplicates().tolist()
		data_idx = {}

		for idx in index:
			idx_value = df2.loc[df2['disk_index'] == idx]
			value = idx_value['value'].tolist()
			if sum(value) == 0 or len(value) < 24:
				continue
			key = "disk_index_" + str(idx)
			data_idx[key] = []
			for i in range(len(value) // 24):
				data_idx[key].append(value[i * 24:i * 24 + 24])
		if name == "memoryUsed":
			if data_idx:
				dff2 = dff.loc[dff['object_id'] == oi]
				if len(dff2):
					data_idx['total'] = dff2['value'].values[0]
				else:
					data_idx = {}
		if data_idx:
			data[oi] = data_idx

	return data


def time_feature(data, p1, p2):
	# 均值
	df_mean = data[p1:p2].mean()
	# 方差
	df_var = data[p1:p2].var()
	# 标准差
	df_std = data[p1:p2].std()
	# 均方根
	df_rms = math.sqrt(pow(df_mean, 2) + pow(df_std, 2))
	# 偏度
	df_skew = data[p1:p2].skew()
	# 峭度
	df_kurt = data[p1:p2].kurt()
	sum = 0
	for i in range(p1, p2):
		sum += math.sqrt(abs(data[i]))
	# 波形因子
	df_boxing = df_rms / (abs(data[p1:p2]).mean())
	# 峰值因子
	df_fengzhi = (max(data[p1:p2])) / df_rms
	# 脉冲因子
	df_maichong = (max(data[p1:p2])) / (abs(data[p1:p2]).mean())
	# 裕度因子
	df_yudu = (max(data[p1:p2])) / pow((sum / (p2 - p1)), 2)
	t = data[p1:p2] - df_mean
	pre = t[0]
	cnt = 0
	for i in range(1, len(t)):
		if pre * t[i] < 0:
			cnt += 1
		pre = t[i]
	lcr = cnt / (p2 - p1 - 1)
	# featuretime_list = [df_mean, df_var, df_rms, df_skew, df_kurt, df_boxing, df_fengzhi, df_maichong, df_yudu,lcr]
	featuretime_list = [df_var, df_yudu]
	return featuretime_list


def get_corr(data):
	if len(data) == 1:
		return 1
	corr = np.corrcoef(data).tolist()
	# print(corr)
	res = 0
	sum = 0
	for x in corr:
		for c in x:
			if abs(c) < 0.99:
				sum += c
			if res > 0 and c > res and abs(c) < 0.99:
				res = c
			elif res <= 0 and abs(c) > res and abs(c) < 0.99:
				res = c
	# print(res)
	l = len(data)
	mean = sum / (l * l - l)
	print(mean)
	return mean


# 0表示提取范围为全部时间段，1为用每小时平均值
def get_feature(s_data, flag):
	feature = []
	for key in s_data:
		tmp = []
		for disk_index in s_data[key]:
			proc_data = []
			feature_tmp = []
			if disk_index == "total":
				for feature_tmp in tmp:
					feature_tmp.append(s_data[key][disk_index])
				continue
			total_data = s_data[key][disk_index]
			corr = get_corr(total_data)
			if flag == 0:
				raw_data = np.array([])
				for day_data in total_data:
					raw_data = np.append(raw_data, day_data)
				proc_data = raw_data
			elif flag == 1:
				raw_data = np.array([range(0, 24)])
				for day_data in total_data:
					raw_data = np.append(raw_data, [day_data], axis=0)
				raw_data = np.delete(raw_data, 0, axis=0)
				proc_data = np.mean(raw_data, axis=0)

			df = pd.Series(proc_data)
			feature_tmp += time_feature(df, 0, len(proc_data) - 1)
			feature_tmp.append(corr)
			tmp.append(feature_tmp)
		tmp = np.array(tmp)
		tmp = np.mean(tmp, axis=0)
		feature.append(tmp.tolist())

	train = pd.DataFrame(data=feature, index=s_data.keys())
	return train

# TODO:每天之间的自相关
# 均值、方差、level crossing rate、
# KMEANS 低纬度聚类，看拐点重合
