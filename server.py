import csv
import time
import Pyro4

@Pyro4.expose
class Searcher(object):
	def __init__(self, name, start_index, end_index, book_list, keyword):
		self._name = name
		self._start_index = start_index
		self._end_index = end_index
		self._book_list = book_list
		self._keyword = keyword

	@Pyro4.expose
	def name(self):
		return self._name

	@Pyro4.expose
	def start_index(self):
		return self._start_index

	@Pyro4.expose
	def end_index(self):
		return self._end_index
		
	@Pyro4.expose
	def book_list(self):
		return self._book_list

	@Pyro4.expose
	def keyword(self):
		return self._keyword

	@Pyro4.expose
	def report(self, time_execution, total, task_time):
		print("[" + self._name + "] just finised! (" + str(total) + " found in " + str(task_time) + "s). Overall: " + str(time_execution))

	def report_slowest(self, slowest, slowest_system):
		print("\n" + slowest_system.name() + " slowest | " + str(slowest) + "s")

def get_csv(filename):
	with open(filename, encoding='utf-8') as csvfile:
		book_list = []
		readcsv = csv.reader(csvfile, delimiter = ',')
		for row in readcsv:
			book_list.append(row[0])

		return book_list

# main program
def main():
	Pyro4.config.THREADPOOL_SIZE = 201
	book_list = get_csv('BOOK200.csv') # data setup
	keyword = input("Search books via keyword: ") # keyword input

	# User inputs how many threads
	num_searchers = int(input("Number of Searchers: "))
	scope = int(len(book_list) / num_searchers)
	start_offset = 0
	end_offset = scope - 1

	searchers = []
	for i in range(num_searchers):
		if i != num_searchers - 1:
			searchers.append(Searcher("searcher_" + str(i), start_offset, end_offset, book_list, keyword))

		else: searchers.append(Searcher("searcher_" + str(i), start_offset, len(book_list), book_list, keyword))

		start_offset += scope
		end_offset += scope

	with Pyro4.Daemon(host = '172.20.10.3', port = 9091) as daemon:
		for i in searchers:
			uri = daemon.register(i)
			# host = '172.20.10.3', port = 9090
			with Pyro4.locateNS() as ns:
				ns.register("library." + i.name(), uri)
				print("PYRO:library." + i.name() + "@172.20.10.3:" + str(uri.port))

		daemon.requestLoop()

main()
