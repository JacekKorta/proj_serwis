
import time
from datetime import datetime
from app import db
from app.models import Machines, Issues
'''
with open ('machines.txt', 'r') as file:
    for line in file:
        m = Machines(name=line)
        db.session.add(m)
    db.session.commit()
'''
'''
class Issue (object):
    
    def __init__(self, time_stamp, owner, machine_model, serial_number, part_number, quantity, part_name,
                 issue_desc, where_is_part, exchange_status, janome_status, comment):      
        self.time_stamp = time_stamp
        self.owner = owner
        self.machine_model = machine_model
        self.serial_number = serial_number
        self.part_number = part_number
        self.quantity = quantity
        self.part_name = part_name
        self.issue_desc = issue_desc
        self.where_is_part = where_is_part
        self.exchange_status = exchange_status
        self.janome_status = janome_status
        self.comment = comment

with open ("issues.tsv", "r", encoding="utf-8-sig") as file:
    for line in file:
        x = line.split("\t")
        #x[0] = x[0].replace(r"\ufeff",'')
        date = datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S')
        obj = Issues(time_stamp=date,
                     owner=x[1],
                     machine_model=x[2],
                     serial_number=x[3],
                     part_number=x[4],
                     quantity=x[5],
                     part_name=x[6],
                     issue_desc=x[7],
                     where_is_part=x[8],
                     exchange_status=x[9],
                     janome_status = x[10],
                     comment=x[11])
        db.session.add(obj)
    db.session.commit()
        
'''       
        
