import csv

myCsvRow = ['a','b','c',1,2,3]

fd = open('log.csv','a')
writer = csv.writer(fd, lineterminator='\n')
writer.writerow(myCsvRow)
fd.close()
