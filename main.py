import csv
import time
import threading

def get_csv(filename):
	with open(filename, encoding='utf-8') as csvfile:
		book_list = []
		readcsv = csv.reader(csvfile, delimiter = ',')
		for row in readcsv:
			book_list.append(row[0])
		return book_list

# Put into List
book_list = get_csv('BOOK200.csv')

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

################## single thread vs. multi-thread ##################

#multi-threads
def find_book(tnum, start_index, end_index, keyword, book_list):
	i = start_index
	ctr = 0
	t_start_time = time.time()
	while i < end_index:
		if keyword.lower() in book_list[i].lower():
			ctr += 1
		i += 1
	t_end_time = time.time()
	print("[Thread", tnum,"] Total books found:" + str(ctr))
	return

#User inputs how many threads
num_threads = int(input("Number of threads: "))
scope = int(len(book_list) / num_threads)
start_offset = 0
end_offset = scope - 1
threads = []

threads_start_time = time.time()
for i in range(0, num_threads):
	if(i != num_threads - 1):
		t = threading.Thread(target = find_book, args = (i, start_offset, end_offset, keyword, book_list))
		threads.append(t)
		t.start()
		t.join()

	else:
		t = threading.Thread(target = find_book, args = (i, start_offset, len(book_list), keyword, book_list))
		threads.append(t)
		t.start()
		t.join()

	start_offset += scope
	end_offset += scope

threads_end_time = time.time()
print("Parallelized time: " + str(threads_end_time - threads_start_time))

