# Service issue manage system
## App to manage service issues between sales and tech service department and the manufacturer. 
## Table of context
### Introduction
#### <ewentualne rozwinięcie wprowadzenia>
<Tło:
Firma prowadzi sprzedaż hurtową urządzeń AGD. W ramach prowadzonej działalności udziela  3-6 letnią gwarancji na swoje produkty. 
W ramach gwarancji niezależne serwisy zgłaszają zapotrzebowanie do działu handlowego. Po zatwierdzeniu zgłoszenia dział handlowy daje zlecenie wymiany do magazynu. Magazyn wymienia uszkodzoną część na nową i dostarcza uszkodzoną część do działu handlowego. Dział handlowy blokuje nową część w ERP. 
Raz w miesiącu dział handlowy składa raport o wymienionych częściach do producenta. Producent rozpatruje które części wymieni w ramach gwarancji. Części odrzucone w reklamacji przez producenta należy ściągnąć z magazynu (z ERP) dokumentem RW.
Części uznane przez producenta, w zależności od fabryki w której są produkowane , są wymieniane odpowiednio po: 60-90 dni, 90-120 dni lub 120-150 dni.  Na życzenie producenta część części jest odsyłana do fabryk>
Koncepcja:
Stworzyć aplikacji dzięki której cały proces będzie transparenty i jak najbardziej zautomatyzowany.
### Technologies
Python 3.7, flask, sqlalchemy, 
### How to run?
install packages: 
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
 
set FLASK_APP=
### Actual status
### References
