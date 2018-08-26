import csv
import time
import Pyro4

def find_book(start_index, end_index, keyword, book_list):
	i = start_index
	ctr = 0
	t_start_time = time.time()
	while i < end_index:
		if keyword.lower() in book_list[i].lower():
			ctr += 1
		i += 1
	t_end_time = time.time()

	# return time result and number of books found
	return round(t_end_time - t_start_time, 4), ctr

def find_searcher(id_num):
	found = None
	i = 0
	with Pyro4.locateNS() as ns:
		for searcher, searcher_uri in ns.list(prefix="library.").items():
			if i == id_num:
				print("found searcher", searcher)
				found = Pyro4.Proxy(searcher_uri)
				break
			i += 1

	if not found:
		raise ValueError("no searcher found! (have you started the server first?)")
	return found

def main():
	# uri = input("Enter URI: ")
	# searcher = Pyro4.Proxy(uri).strip()
	id_num = int(input("Enter id: "))
	searcher = find_searcher(id_num)
	r = find_book(searcher.start_index(), searcher.end_index(), searcher.keyword(), searcher.book_list())
	print("Time: " + str(r[0]))
	print("Total number of books: " + str(r[1]))
	searcher.report(r[0], r[1])

main()