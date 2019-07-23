# Service issue management system
## App to manage service issues between sales and tech service department and the manufacturer. 
### Introduction
#### Background:
Firma prowadzi sprzedaż hurtową urządzeń AGD. W ramach prowadzonej działalności udziela  3-6 letnią gwarancji na swoje produkty. 
W ramach gwarancji niezależne serwisy zgłaszają zapotrzebowanie do działu handlowego. Po zatwierdzeniu zgłoszenia dział handlowy daje zlecenie wymiany do magazynu. Magazyn wymienia uszkodzoną część na nową i dostarcza uszkodzoną część do działu handlowego. Dział handlowy blokuje nową część w ERP. 
Raz w miesiącu dział handlowy składa raport o wymienionych częściach do producenta. Producent rozpatruje które części wymieni w ramach gwarancji. Części odrzucone w reklamacji przez producenta należy ściągnąć z magazynu (z ERP) dokumentem RW.
Części uznane przez producenta, w zależności od fabryki w której są produkowane , są wymieniane odpowiednio po: 60-90 dni, 90-120 dni lub 120-150 dni.  Na życzenie producenta część części jest odsyłana do fabryk>
Koncepcja:
Stworzyć aplikacji dzięki której cały proces będzie transparenty i jak najbardziej zautomatyzowany.
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
