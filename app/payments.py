from flask import render_template
from datetime import datetime


'''
now = datetime.now()
now_str = now.strftime('%Y-%m-%d')
customers_adres = {"ZIMET":'info@janome.pl', 'ANWO': 'info@janome.pl'}
'''

def test():
    a =2
    return a


def delayed_payments(data):
    customers = {}
    for line in data:
        data_list = line.split('\t')
        while '' in data_list:
            a.remove('')
        if len(data_list)>5:
            data_list[5] = data_list[5].replace(',','.')
            if (data_list[3]< now_str) and (float(data_list[5]) > 9):
                #cyfra(y) po znaku większości oznaczają minimalne kwota zadłużenia która będzie brana pod uwagę.
                if not data_list[0] in customers:
                    customers[data_list[0]]=[(data_list[1], data_list[2], data_list[5])]
                else:
                     customers[data_list[0]].append((data_list[1], data_list[2], data_list[5]))
    #return customers
