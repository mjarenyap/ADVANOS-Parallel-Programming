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

def find_searchers(num):
	s = None
	i = 0
	with Pyro4.locateNS() as ns:
		for searcher, searcher_uri in ns.list(prefix="library.searcher_").items():
			# print("found searcher", searcher)
			if i == num:
				s = Pyro4.Proxy(searcher_uri)
				break
			i += 1

	if not s:
		raise ValueError("no searcher found! (have you started the server first?)")
	return s

def main():
	num = int(input("nth System: "))
	searcher = find_searchers(num)
	r = find_book(searcher.start_index(), searcher.end_index(), searcher.keyword(), searcher.book_list())
	searcher.report(r[0], r[1])
	print(searcher.name() + " | Time: " + str(r[0]) + " | Total: " + str(r[1]))

main()