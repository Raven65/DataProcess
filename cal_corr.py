# -*- coding: utf-8 -*-
import read_data
import numpy as np
import matplotlib.pyplot as plt
from vm import Vm


def cal_cpu_corr(vm_list, date_start, date_end):
	corr_list = []
	for vm_name in vm_list:
		cpu_all_date = []
		vm = read_data.read_data_to_vm(vm_name)
		for date in range(date_start, date_end + 1):
			if date not in vm.date:
				continue
			cpu_cores = [attr for attr in vm.attrs if attr.find("cpu") != -1]
			cpu = []
			for cpu_core in cpu_cores:
				cpu_data = vm.get_data(date, "08:00:00", "10:00:00", cpu_core)
				if cpu_data:
					cpu.append(cpu_data)
			if cpu:
				cpu = np.mean(cpu, axis=0).tolist()
				cpu_all_date.append(cpu)
		corr = np.corrcoef(cpu_all_date).tolist()
		for x in corr:
			for y in x:
				if y <0.99999:
					corr_list.append(y)
	return corr_list

def get_corr_hist():
	corr_list = cal_cpu_corr(["POOL02-OA-7","POOL02-OA-10"],1114,1120)
	plt.hist(corr_list, np.arange(-1.05, 1.05, 0.05), alpha = 0.5)
	plt.show()

if __name__ == "__main__":
	get_corr_hist()
