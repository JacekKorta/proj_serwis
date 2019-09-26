from datetime import datetime

now = datetime.now()
now_str = now.strftime('%Y-%m-%d')


def delayed_payments(data):
    # Additional module. Is analyzing data from "symfonia handel" and showing grouped (per customer) unpaid invoices.
    customers = {}
    data_list = data.split('\n')
    while '' in data_list:
        data_list.remove('')
    for item in data_list:
        invoice = item.split('\t')
        if len(invoice) > 5:
            invoice[9] = invoice[9].replace(',','.')
            if (invoice[5] < now_str) and (float(invoice[9]) > 9):
                # The number after ">" means the minimum debt amount with will be checked.
                if not invoice[0] in customers:
                    customers[invoice[0]] = [(invoice[2], invoice[4], invoice[5], invoice[9])]
                else:
                     customers[invoice[0]].append((invoice[2], invoice[4], invoice[5], invoice[9]))
    for item in customers.keys():
        total_dept = 0
        for obj in customers[item]:
            total_dept += round(float(obj[3]), 2)
        customers[item].append(round((total_dept),2))
    return customers
