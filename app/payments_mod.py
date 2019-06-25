from flask import render_template
from datetime import datetime
from app import app

now = datetime.now()
now_str = now.strftime('%Y-%m-%d')
customers_adres = {"ZIMET":'info@janome.pl', 'ANWO': 'info@janome.pl'}

'''
class delayed_obj(customer_name, invoices, total_delayed_value):
    self.customer_name = customer_name
    self.invoices = invoices
    self.total_delayed_value = total_delayed_value
'''

def delayed_payments(data):
    customers = {}
    obj_list =[]
    #for line in data:
        #print(line)
    data_list = data.split('\n')
    while '' in data_list:
        data_list.remove('')
    for item in data_list:
        invoice = item.split('\t')
        if len(invoice)>5:
            invoice[9] = invoice[9].replace(',','.')
            if (invoice[5]< now_str) and (float(invoice[9]) > 9):
                #cyfra(y) po znaku większości oznaczają minimalne kwota zadłużenia która będzie brana pod uwagę.
                if not invoice[0] in customers:
                    customers[invoice[0]]=[(invoice[2], invoice[4],invoice[5], invoice[9])]
                else:
                     customers[invoice[0]].append((invoice[2], invoice[4], invoice[5], invoice[9]))
    for item in customers.keys():
        total_dept = 0
        for obj in customers[item]:
            total_dept += round(float(obj[3]), 2)
        customers[item].append(round((total_dept),2))
    return customers