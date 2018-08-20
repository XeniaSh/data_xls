import pandas as pd

dataDE = pd.read_excel("trans_data.xlsx", usecols = "D:E")
len_data = len(dataDE)

#1.1, 1.2
def prop(data):
	#поиск отрицательных ячеек и нахождение их доли по столбцам amount и initial_pr
	data_minus_amount = dataDE[data.amount < 0]
	data_minus_pr = dataDE[data.initial_pr < 0]
	amount_minus = len(data_minus_amount)/len_data
	pr_minus = len(data_minus_pr)/len_data
	#поиск незаполненных ячеек и нахождение их доли по столбцам amount и initial_pr
	data_null_amount = dataDE[data.amount.isnull()] 
	data_null_pr = dataDE[data.initial_pr.isnull()]
	amount_null = len(data_null_amount)/len_data
	pr_null = len(data_null_pr)/len_data
	#вывод ответа в файл
	if ((len(data_minus_amount) > 0) |  (len(data_minus_pr) > 0)):
		str = f"есть отрицательные числа: доля в amount {amount_minus}, доля в initial_pr {pr_minus}" 
		with open("1.txt",'w') as f:
			f.write(str)
	else: 
		str = f"нет отрицательных чисел"
		with open("1.txt",'w') as f:
			f.write(str)
	if ((len(data_null_amount) > 0) |  (len(data_null_pr) > 0)):	
		str = "\n" + f"есть пропуски: доля в amount {amount_null}, доля в initial_pr {pr_null}" 
		with open("1.txt",'a') as f:
			f.write(str)
	else: 
		str = "\n" + f"нет пропусков"
		with open("1.txt",'a') as f:
			f.write(str)
prop(dataDE)

def excel_writer(data):
	#запись данных в новую таблицу
	writer = pd.ExcelWriter("data_new.xlsx", engine='xlsxwriter', date_format='dd.mm.yyyy', datetime_format = 'dd.mm.yyyy')
	data.to_excel(writer, 'Sheet1', index = False)
	writer.save()

#1.3
def new_table(data):
	#замена отрицательных чисел
	data.amount[data.amount < 0] = -data.amount
	data.initial_pr[data.initial_pr < 0] = -data.initial_pr
	excel_writer(data)
	#замена пропусков
	data = pd.read_excel("data_new.xlsx")
	median_pr = data['initial_pr'].median()
	median_amount = data['amount'].median()
	data.amount[data.amount.isnull()] = median_amount
	data.initial_pr[data.initial_pr.isnull()] = median_pr
	#запись данных в новую таблицу
	excel_writer(data)
new_table(dataDE)

#2.a
dataABC = pd.read_excel("trans_data.xlsx", usecols = "A:C")
def last_month_day(data):
	from pandas.tseries.offsets import MonthEnd
	#проверка, все ли даты соответствуют последним дням месяца
	if (pd.to_datetime(data['value_month']) < (pd.to_datetime(data['value_month'])+MonthEnd(0))).any():
		data['value_month'] = pd.to_datetime(data['value_month']) + MonthEnd(0)
		str = "не все даты соответствуют последним дням месяца"
		with open("2a.txt",'w') as f:
			f.write(str)
			data['value_month'].to_csv(r'2a.txt', header=None, index=None, sep=' ', mode='a')
	else:
		str = "все даты соответствуют последним дням месяца"
		with open("2a.txt",'w') as f:
			f.write(str)
	return data
	
#2.b
def check_MOB(data):
	#проверка условий по MOB и вывод данных
	if ((data['MOB'].dtype == "int64") & (data['MOB'] >= 0) & (data['MOB'] <= 35)).all():
		str = "2b: MOB целое от 0 до 35"
		with open("2b.txt",'w') as f:
			f.write(str)
	else:
		str ="MOB не целое от 0 до 35"
		with open("2b.txt",'w') as f:
			f.write(str)
	dif = (data['month_date'].dt.year - data['value_month'].dt.year)*12 + (data['month_date'].dt.month - data['value_month'].dt.month)
	if (data['MOB'] != dif).any():	
		str = '\n'+"MOB не равно количеству месяцев между month_date и value_month"
		data['MOB'] = dif
		with open("2b.txt",'a') as f:
			f.write(str)
		data['MOB'].to_csv(r'2b.txt', header=None, index=None, sep=' ', mode='a')
check_MOB(last_month_day(dataABC))

