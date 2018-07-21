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
print("Total books found: " + str(counter))
serial_end_time = time.time()
print("Serialized Time: " + str(serial_end_time - serial_start_time))
print("--------------------------------------------------")

# Parallelized System
import pygame
import random

def getDecrement(counter, end_index):
	percentage = counter / end_index
	return int(500 * percentage)

def find_book(start_index, end_index, keyword, book_list, screen, coordinates):
	i = start_index
	ctr = 0
	while i < end_index:
		if keyword.lower() in book_list[i].lower():
			ctr += 1
		i += 1
		coordinates[1] -= getDecrement(i, end_index)
		pygame.draw.circle(screen,coordinates[3], (coordinates[0], coordinates[1]), coordinates[2])
	print("Total books found: " + str(ctr))
	return

def generateColor():
    newColor = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    return newColor

# User inputs how many threads
num_threads = int(input("Number of threads: "))
scope = int(len(book_list) / num_threads)
start_offset = 0
end_offset = scope - 1

# Start pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
done = False

threads = []
coordinates = []
for i in range(0, num_threads):
	coordinates.append([50 + (i * 5 * 2), 550, 5, generateColor()])
	if(i != num_threads - 1):
		t = threading.Thread(target = find_book, args = (start_offset, end_offset, keyword, book_list, screen, coordinates[i]))
		threads.append(t)

	else:
		t = threading.Thread(target = find_book, args = (start_offset, len(book_list), keyword, book_list, screen, coordinates[i]))
		threads.append(t)

	start_offset += scope
	end_offset += scope

clock = pygame.time.Clock()

timed = False
while not done:
	screen.fill((0, 0, 0))

	threads_start_time = time.time()
	for i in threads:
		i.start()
		i.join()

	threads_end_time = time.time()
	print("Parallelized time: " + str(threads_end_time - threads_start_time))
	if not done:
		done = not done

	pygame.display.flip()
	clock.tick(60)