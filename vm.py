# -*- coding: utf-8 -*-


class Vm:
	def __init__(self, name):
		self.name = name
		self.data = {}
		self.date = set()
		self.attrs = set()
		self.actual_time = {}

	def set_timestamp(self, date, timestamp):
		if date not in self.date:
			self.date.add(date)
		self.actual_time[date] = timestamp

	def set_data(self, date, key, value):
		if date not in self.date:
			self.date.add(date)
		if date not in self.data:
			self.data[date] = {}
		self.data[date][key] = value
		self.attrs.add(key)

	def get_data(self, date, start_time, end_time, key):
		if date not in self.date:
			return None
		if start_time < self.actual_time[date][0] or end_time > self.actual_time[date][-1]:
			return None
		start_idx = self.actual_time[date].index(start_time)
		end_idx = self.actual_time[date].index(end_time)
		return self.data[date][key][start_idx:end_idx + 1]
