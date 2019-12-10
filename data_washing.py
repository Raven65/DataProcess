# -*- coding: utf-8 -*-

import pandas as pd
import os
import time
from dateutil import parser
from datetime import datetime, timezone, timedelta

date_start = 1113
date_end = 1127

host_start = 59
host_end = 70


def transTime(ts):
	dt = parser.parse(ts)
	cn_dt = dt.astimezone(timezone(timedelta(hours=8)))
	new_ts = cn_dt.strftime("%Y-%m-%d %H:%M:%S")
	return new_ts


def process():
	vm_date = {"date": range(date_start, date_end + 1)}
	host_date = {"date": range(date_start, date_end + 1)}
	for date in range(date_start, date_end + 1):
		for host in range(host_start, host_end + 1):
			path = "E:/BaiduNetdiskDownload/monitor_data/2019" + str(date) + "/" + "xen_rrd_data_" + str(
				host) + "_" + str(date) + ".csv"
			if not os.path.exists(path):
				continue
			print("processing " + path)
			df = pd.read_csv(path, low_memory=False, error_bad_lines=False)
			# 去除无效记录
			df = df[df['timestamp'].map(len) == 20]
			# 把时间戳时区调整为北京时间
			df['timestamp'] = df['timestamp'].apply(transTime)

			lis = df.columns.values.tolist()
			vm_ind = ["vm_name", "host_name", "timestamp", "vbd_xvdb_write_latency", "vbd_xvda_write_latency",
					  "vbd_xvda_read_latency", "memory_target", "memory_internal_free", "memory", "vbd_xvdb_iowait",
					  "vbd_xvda_iowait", "vif_0_rx", "vif_0_tx", "cpu0", "cpu1", "cpu2", "cpu3", "cpu4", "cpu5", "cpu6",
					  "cpu7"]
			vm_set = set()
			host_ind = []
			host_name = str()
			for name in lis:
				if name.find("vm:") != -1:
					tmp = name.split(":")
					vm_set.add(":".join(tmp[2:-1]))
				elif name.find("host:") != -1:
					if not host_name:
						host_name = name.split(":")[-2]
					host_ind.append(name.split(":")[-1])
			host_ind = ['host_name', 'timestamp'] + host_ind
			for vm in vm_set:
				if vm not in vm_date:
					vm_date[vm] = [0] * (date_end - date_start + 1)
				vm_date[vm][date - date_start] = 1
				df1 = pd.DataFrame(columns=vm_ind)
				df1['timestamp'] = df['timestamp']
				for i in range(3, len(vm_ind)):
					col_name = " AVERAGE:vm:" + vm + ":" + vm_ind[i]
					if col_name in lis:
						df1[vm_ind[i]] = df[col_name]
				df1['vm_name'] = vm
				df1['host_name'] = host_name
				df1 = df1[~df1['memory'].isin([' N/A'])]
				df1 = df1.dropna(axis=1, how='all')
				save_path = 'E:/data/vm/' + str(vm.replace(':', " ").replace('/', ' '))
				if not os.path.exists(save_path):
					os.makedirs(save_path)
				df1.to_csv(save_path + '/' + str(date) + '_' + str(host) + '.csv',
						   index=False)
			host_df = pd.DataFrame(columns=host_ind)
			host_df['timestamp'] = df['timestamp']
			for i in range(2, len(host_ind)):
				col_name = " AVERAGE:host:" + host_name + ":" + host_ind[i]
				if col_name in lis:
					host_df[host_ind[i]] = df[col_name]
			host_df['host_name'] = host_name
			save_path = 'E:/data/host/'
			if not os.path.exists(save_path):
				os.makedirs(save_path)
			host_df.to_csv(save_path + '/' + str(date) + '_' + str(host) + '.csv',
						   index=False)
			if host not in host_date:
				host_date[host] = [0] * (date_end - date_start + 1)
			host_date[host][date - date_start] = 1

	vm_df = pd.DataFrame(data=vm_date)
	vm_df.to_csv("E:/data/vm_list.csv", index=False)
	host_df = pd.DataFrame(data=host_date)
	host_df.to_csv("E:/data/host_list.csv", index=False)




if __name__ == "__main__":
	process()
