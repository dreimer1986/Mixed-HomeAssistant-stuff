import csv, sys
from datetime import date
from datetime import datetime
from datetime import timedelta

csv_file1 = "/config/www/ocppexport1.txt"
csv_file2 = "/config/www/ocppexport2.txt"
days = int(date.today().strftime("%d"))

the_list1 = []
kwh_list1 = []
the_list2 = []
kwh_list2 = []

if sys.argv[1] == "1":

    # Read the csv_file
    csv_reader1 = csv.DictReader(open(csv_file1), delimiter=';')

    for line in csv_reader1:
        tempdate = datetime.strptime(line['date'], '%d.%m.%Y')
        deltaMonth = timedelta(days=int(date.today().strftime("%d")))
        deltaToday = date.today() - tempdate.date()
        if deltaToday < deltaMonth:
            the_list1.append(line)
            kwh_list1.append(float(line['charged']))

    # Revert the list, we want the last row at the top
    the_list1.reverse()
    kwh_list1.reverse()

    print(sum(kwh_list1))

if sys.argv[1] == "2":

    # Read the csv_file
    csv_reader2 = csv.DictReader(open(csv_file2), delimiter=';')

    for line in csv_reader2:
        tempdate = datetime.strptime(line['date'], '%d.%m.%Y')
        deltaMonth = timedelta(days=int(date.today().strftime("%d")))
        deltaToday = date.today() - tempdate.date()
        if deltaToday < deltaMonth:
            the_list2.append(line)
            kwh_list2.append(float(line['charged']))

    # Revert the list, we want the last row at the top
    the_list2.reverse()
    kwh_list2.reverse()

    print(sum(kwh_list2))
