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
	return round(t_end_time - t_start_time, 7), ctr

def find_searchers():
	s = []
	with Pyro4.locateNS() as ns:
		for searcher, searcher_uri in ns.list(prefix="library.searcher_").items():
			# print("found searcher", searcher)
			s.append(Pyro4.Proxy(searcher_uri))

	if not s:
		raise ValueError("no searcher found! (have you started the server first?)")
	return s

def main():
	# uri = input("Enter URI: ")
	# searcher = Pyro4.Proxy(uri).strip()
	# id_num = int(input("Enter id: "))
	searchers = find_searchers()
	for i in searchers:
		r = find_book(i.start_index(), i.end_index(), i.keyword(), i.book_list())
		print(i.name() + " | Time: " + str(r[0]) + " | Total: " + str(r[1]))
		i.report(r[0], r[1])
	# r = find_book(searcher.start_index(), searcher.end_index(), searcher.keyword(), searcher.book_list())
	# searcher.report(r[0], r[1])

main()