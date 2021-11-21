import tushare as ts
import csv

pro = ts.pro_api('d2144df3d2c4f703454e331d9c95c0dc8685101ca04795d337cd5de1')
file = open("daily.txt", 'w')
data = pro.stock_basic()
ts_code = data['ts_code']
name=data['name']
for i in range(len(data['ts_code'])):
    file.write("[name:{}, ts_code:{}],\n".format(ts_code[i], name[i]))
file.close()
