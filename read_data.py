# -*- coding: utf-8 -*-
import pandas as pd
import os
from vm import Vm
import time
from dateutil import parser
from datetime import datetime, timezone, timedelta

date_start = 1114
date_end = 1127


def read_data_to_vm(vm_name):
	vm = Vm(vm_name)
	names = os.listdir('E:/data/vm/' + vm_name)
	for date in range(date_start, date_end + 1):
		file_list = [name for name in names if name.find(str(date)) != -1]
		if not file_list:
			continue
		idx = 0
		date_df = pd.DataFrame()
		while idx < len(file_list):
			try:
				date_df = pd.read_csv('E:/data/vm/' + vm_name + '/' + file_list[idx], low_memory=False,
									  error_bad_lines=False)
				break
			except:
				idx += 1
				continue
		for i in range(idx, len(file_list)):
			try:
				new_df = pd.read_csv('E:/data/vm/' + vm_name + '/' + file_list[i], low_memory=False,
									 error_bad_lines=False)
				date_df.append(new_df)
			except:
				continue
		if idx == len(file_list):
			return

		timestamp = date_df['timestamp'].apply(lambda x: x[11:]).tolist()
		attrs = date_df.columns.values.tolist()
		attrs.pop(0)
		attrs.pop(1)
		vm.set_timestamp(date, timestamp)
		for attr in attrs:
			vm.set_data(date, attr, date_df[attr].tolist())

	return vm

if __name__ == "__main__":
	read_data_to_vm("POOL02-OA-7")
