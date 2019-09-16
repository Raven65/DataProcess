# -*- coding: utf-8 -*-
import pandas as pd


def process_raw_data(name: str):
	df = pd.read_excel("./rawData/" + name + "/" + name + "(hour).xls")
	del df['item_name']
	df.rename(columns={'item_value': 'value', 'index': 'disk_index'}, inplace=True)

	s = df['create_time']
	s = s.map(lambda x: x.split(' ')[1][0:2])

	l = s.tolist()
	group_by_id = df.groupby('object_id')
	cnt = group_by_id.size().tolist()
	start = 0
	mark = []
	for x in cnt:
		tmp = l[start:start + x]
		if "17" not in tmp or "16" not in tmp:
			start += x
			continue
		first = tmp.index("17")
		last = len(tmp) - tmp[::-1].index("16")
		if last <= first or last - first + 1 < 24:
			start += x
			continue
		mark.append([start + first, start + last])
		start += x
	newDf = pd.DataFrame(columns=df.columns.values.tolist())
	for index in mark:
		tmp_df = df.iloc[index[0]:index[1]]
		newDf = newDf.append(tmp_df)
		newDf = newDf.drop_duplicates()
	newDf.to_csv('data/' + name + '.csv', encoding='utf-8')


if __name__ == '__main__':
	process_raw_data("cpu")
	process_raw_data("diskIoWriteLatency")
	process_raw_data("memoryUsed")
	process_raw_data("memoryTotal")
	process_raw_data("ioWait")
	process_raw_data("netReceived")
	process_raw_data("netTransmitted")
