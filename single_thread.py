import csv
import time
import threading

def get_csv(filename):
	with open(filename) as csvfile:
		book_list = []
		readcsv = csv.reader(csvfile, delimiter = ',')
		for row in readcsv:
			book_list.append(row[1])
		return book_list

# Put into List
book_list = get_csv('BOOK.csv')

# Serialized
keyword = input("Search books via keyword: ")

serial_start_time = time.time()
counter = 0
for row in book_list:
	if keyword.lower() in row.lower():
		counter += 1
print("--------------------------------------------------")
print("Total books found:" + str(counter))
serial_end_time = time.time()
print("Serialized Time: " + str(serial_end_time - serial_start_time))
print("--------------------------------------------------")

#Two threads
def find_book(start_index, end_index, keyword, book_list):
	i = start_index
	ctr = 0
	while i < end_index:
		if keyword.lower() in book_list[i].lower():
			#print(book_list[i])
			ctr += 1
		i += 1
	print("Total books found:" + str(ctr))
	return

# User inputs how many threads
num_threads = int(input("Number of threads: "))
scope = int(len(book_list) / num_threads)
start_offset = 0
end_offset = scope - 1
threads = []
for i in range(0, num_threads):
	if(i != num_threads - 1):
		t = threading.Thread(target = find_book, args = (start_offset, end_offset, keyword, book_list))
		threads.append(t)

	else:
		t = threading.Thread(target = find_book, args = (start_offset, len(book_list), keyword, book_list))
		threads.append(t)

	start_offset += scope
	end_offset += scope

threads_start_time = time.time()
for i in threads:
	i.start()
	i.join()
threads_end_time = time.time()
print("Parallelized time: " + str(threads_end_time - threads_start_time))


"""
t1 = threading.Thread(target = find_book, args = (0, len(book_list)//2, keyword, book_list))
t2 = threading.Thread(target = find_book, args = ((len(book_list)//2) + 1, len(book_list), keyword, book_list))
threads_start_time = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
threads_end_time = time.time()
print("Parallelized time: " + str(threads_end_time - threads_start_time))
"""

