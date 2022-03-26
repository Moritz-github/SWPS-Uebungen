class Node:
    def __init__(self, data=None, next=None, prev=None):
        self.data = data
        self.prev = prev
        self.next = next

    def __repr__(self):
        return repr(self.data)


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        temp = self.head
        elements = []
        while temp:
            elements.append(repr(temp))
            temp = temp.next
        return '[' + ' -> '.join(elements) + ']'

    def __getitem__(self, key):
        temp = self.head
        while temp and temp.data != key:
            temp = temp.next
        return temp

    def __setitem__(self, key, value):
        temp = self.head
        while temp and temp.data != key:
            temp = temp.next
        if not temp:
            return
        temp.data = value

    def append(self, data):
        if not self.head:
            self.head = Node(data=data)
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = Node(data=data, prev=temp)

    def appendleft(self, data):
        temp = self.head
        temp.prev = Node(data=data, next=temp)
        self.head = temp.prev

    def pop(self):
        if not self.head:
            return
        temp = self.head
        i = 0
        while temp.next:
            temp = temp.next
            i += 1
        if not i:
            self.head = None
            return
        temp.prev.next = None
        temp = None

    def popleft(self):
        if not self.head:
            return
        temp = self.head
        self.head = temp.next
        if not self.head:
            return
        self.head.prev = None
        temp = None

    def find_node(self, key):
        temp = self.head
        while temp and temp.data != key:
            temp = temp.next
        return temp

    def delete(self, key):
        if not self.head:
            return
        current = self.head
        while current and current.data != key:
            current = current.next
        if not current:
            return
        if not current.next:
            return self.pop()
        elif not current.prev:
            return self.popleft()
        temp = current.prev
        current.prev.next = current.next
        current.next.prev = temp
        current = None

    def delete_before(self, key):
        if not self.head:
            return
        current = self.head
        while current and current.data != key:
            current = current.next
        if not current:
            print('Element nicht in der Linked List vorhanden')
            return
        temp = current.prev
        if not temp:
            return
        temp.prev.next = current
        current.prev = temp.prev
        temp = None

    def delete_after(self, key):
        if not self.head:
            return
        current = self.head
        while current and current.data != key:
            current = current.next
        if not current:
            print('Element nicht in der Linked List vorhanden')
            return
        temp = current.next
        if not temp:
            return
        current.next = temp.next
        if not temp.next:
            return
        temp.next.prev = current

    def reverse(self):
        curr = self.head
        prev_node = None
        while curr:
            prev_node = curr.prev
            curr.prev = curr.next
            curr.next = prev_node
            curr = curr.prev
        if prev_node:
            self.head = prev_node.prev

    def insertion_sort_asc(self):
        if(self.head == None):
            return
        else:
            current = self.head
            while(current.next != None):
                index = current.next
                while(index != None):
                    if(current.data > index.data):
                        temp = current.data
                        current.data = index.data
                        index.data = temp
                    index = index.next
                current = current.next
    
    def insertion_sort_desc(self):
        if(self.head == None):
            return
        else:
            current = self.head
            while(current.next != None):
                index = current.next
                while(index != None):
                    if(current.data < index.data):
                        temp = current.data
                        current.data = index.data
                        index.data = temp
                    index = index.next
                current = current.next
    
    def insert_before(self, key, data):
        if not self.head:
            return
        current = self.head
        while current and current.data != key:
            current = current.next
        if not current:
            print('Element nicht in der Linked List vorhanden')
            return
        temp = current.prev
        current.prev = Node(data=data, next=current, prev=temp)
        if not temp:
            self.head = current.prev
        else:
            temp.next = current.prev

    def insert_after(self, key, data):
        if not self.head:
            return
        current = self.head
        while current and current.data != key:
            current = current.next
        if not current:
            print('Element nicht in der Linked List vorhanden')
            return
        temp = current.next
        current.next = Node(data=data, next=temp, prev=current)
        if not temp:
            self.head = current.next
        else:
            temp.prev = current.next

if __name__ == '__main__':
    dll = DoublyLinkedList()
    dll.append(20)
    dll.append(84)
    dll.append(4)
    dll.append(32)
    dll.append(3)
    dll.appendleft(25)
    print(dll)
    dll.pop()
    print(dll)
    dll.popleft()
    print(dll)
    print(dll.find(84))
    dll.delete(84)
    print(dll.find(84))
    dll.reverse()
    print(dll)
    dll.insertion_sort_asc()
    print(dll)
    dll.pop()
    print(dll)
    dll.popleft()
    print(dll)
    print(dll.find(84))
    dll.delete(84)
    print(dll.find(84))
    dll.reverse()
    print(dll)
    dll.insertion_sort_asc()
    print(dll)
    dll.insertion_sort_desc()
    print(dll)
    dll.insert_before(4, 100)
    print(dll)
