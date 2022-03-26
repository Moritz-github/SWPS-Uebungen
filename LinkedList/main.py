from ArrayList import ArrayList
from DoublyLinkedList import DoublyLinkedList
import time
import random

aList = ArrayList()
dList = DoublyLinkedList()
random_nums = [random.randint(0, 100) for i in range(10000)]

[aList.append(i) for i in random_nums]
[dList.append(i) for i in random_nums]


start = time.time()
dList.insertion_sort_asc()
end = time.time()
print(f'DoublyLinkedList: {end - start}')


start = time.time()
aList.insertion_sort_asc()
end = time.time()
print(f'ArrayList: {end - start}')