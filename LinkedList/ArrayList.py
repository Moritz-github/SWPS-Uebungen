import array as array
import random

class ArrayList():
    def __init__(self):
        self.arr = array.array('i', [])
        self.size = 0

    def __str__(self):
        return str(self.arr)

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        if index < 0 or index >= len(self.arr):
            raise IndexError('Index out of range')
        return self.arr[index]

    def __setitem__(self, index, value):
        self.arr.insert(index, value)

    def make_space(self):
        if self.size == 0:
            self.size += 1
            return
        self.size *= 2

    def append(self, item):
        if len(self.arr) + 1 > self.size:
            self.make_space()
        self.arr.append(item)

    def insert(self, index, item):
        if len(self.arr) + 1 > self.size:
            self.make_space()
        if index < 0 or index > self.size:
            raise IndexError('Index out of range')
        self.arr.insert(index, item)
        self.size += 1

    def insert_before(self, index, item):
        if index < 0 or index > self.size:
            raise IndexError('Index out of range')
        if self.size + 1 > self.size:
            self.make_space()
        self.arr.insert(index, item)
        self.size += 1

    def insert_after(self, index, item):
        if index < 0 or index > self.size:
            raise IndexError('Index out of range')
        if self.size + 1 > self.size:
            self.make_space()
        self.arr.insert(index + 1, item)
        self.size += 1

    def delete_before(self, index):
        if index < 0 or index > self.size:
            raise IndexError('Index out of range')
        self.arr.pop(index - 1)
        self.size -= 1

    def delete_after(self, index):
        if index < 0 or index > self.size:
            raise IndexError('Index out of range')
        self.arr.pop(index + 1)
        self.size -= 1

    def insertion_sort_asc(self):
        for i in range(1, len(self.arr)):
            j = i
            while j > 0 and self.arr[j] < self.arr[j - 1]:
                self.arr[j], self.arr[j - 1] = self.arr[j - 1], self.arr[j]
                j -= 1
    
    def insertion_sort_desc(self):
        for i in range(1, len(self.arr)):
            j = i
            while j > 0 and self.arr[j] > self.arr[j - 1]:
                self.arr[j], self.arr[j - 1] = self.arr[j - 1], self.arr[j]
                j -= 1

if __name__ == "__main__":
    al = ArrayList()
    al.append(35)
    al.append(23)
    al.append(12)
    al.append(45)
    al.append(50)
    print(al)
    al.insertion_sort_asc()
    print(al)
    al.insertion_sort_desc()
    print(al)
    al.insert(2, 99)
    print(al)
    al.insert_before(2, 88)
    print(al)
    al.insert_after(2, 77)
    print(al)
    al.delete_before(2)
    print(al)
    al.delete_after(2)
    print(al)
