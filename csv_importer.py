import csv

def get_csv(filename):
	with open(filename) as csvfile:
		readcsv = csv.reader(csvfile, delimiter = ',')
		return readcsv