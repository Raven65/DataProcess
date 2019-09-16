# -*- coding: utf-8 -*-
from pandas import Series
import math

pstf_list = []


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
	featuretime_list = [df_mean, df_rms, df_skew, df_kurt, df_boxing, df_fengzhi, df_maichong, df_yudu]
	return featuretime_list

