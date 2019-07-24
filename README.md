# Service issue management system
## App to manage service issues between sales and tech service department and the manufacturer. 
### Introduction
#### Background:
The company is a wholesaler of household appliances. As a part of its business, the company gives a 3-6 year warranty on its products. Under the warranty independent tech services report a request to the sales department. Once the request is approved, the sales department gives an exchange order to the warehouse. The warehouse exchanges the defective part for the new one and gives the defective part to the sales department, which then blocks the part in the ERP system. Once a month the sales department sends a report on all of the exchanged parts to the manufacturer. Then the manufacturer examines which parts shall be exchanged under the warranty. All of the rejected parts shall be taken from the warehouse (and from the ERP system) with the RW document. The parts accepted by the manufacturer, depending on the producing factory, are exchanged accordingly after: 60-90 days, 90-120 days or 120-150 days. At the manufacturer’s request some parts may be sent back to the factory. The concept was to create an app that helps to make the whole process more transparent and the most automated possible. 
### Technologies
Python 3.7, flask, sqlalchemy, for more see requirements.txt
### How to run?

1) install packages: 
 - flask
 - python-dotenv
 - flask-wtf
 - flask_login
 - flask-sqlalchemy
 - flask-migrate
 - flask-moment (convert time stamp for user local time)
 - flask-mail
 - pandas
 - openpyxl 
 
2) set FLASK_APP=serwis.py

3) create databese:<br>
a) flask db init<br>
b) flask db migrate<br>
c) flask db upgrade<br>

4) Edit fake_config.py file and change it name for config.py

5) run and enyoj :)
### Actual status
almost done, on production, 
TODO:
-refactor code
-more tests
-"Issue" and "Delayed payments" statistics
### References
Inspired "The Flask Mega-Tutorial" from https://blog.miguelgrinberg.com
