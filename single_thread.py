import csv

def get_csv(filename):
	with open(filename) as csvfile:
		book_list = []
		readcsv = csv.reader(csvfile, delimiter = ',')
		for row in readcsv:
			book_list.append(row[1])
		return book_list

# main
book_list = get_csv('BOOK.csv')
keyword = input("Search books via keyword: ")
for row in book_list:
	if keyword.lower() in row.lower():
		print(row)