"""M2 - Tumpukan (stack) dan antrean (queue) di atas struktur M1.

Hanya berisi kelas struktur datanya saja. Yang membuat objek dan memakainya
untuk kasir postfix serta undo/redo adalah frontend/ui.py.
"""

from backend.m1_pesanan import Array


class Stack:
    """LIFO: yang terakhir masuk keluar duluan, dibangun di atas Array."""

    def __init__(self):
        self.array = Array()

    def push(self, v):
        self.array.insert(self.array.size, v)

    def pop(self):
        if self.array.size == 0:
            return None
        return self.array.remove(self.array.size - 1)

    def peek(self):
        return self.array.get(self.array.size - 1)

    def is_empty(self):
        return self.array.size == 0

    def size(self):
        return self.array.size


class NaiveQueue:
    """FIFO naif: dequeue mengambil indeks 0 sehingga seluruh isi bergeser."""

    def __init__(self):
        self.array = Array()

    def enqueue(self, v):
        self.array.insert(self.array.size, v)

    def dequeue(self):
        if self.array.size == 0:
            return None
        return self.array.remove(0)

    def enqueue_front(self, v):
        self.array.insert(0, v)

    def dequeue_back(self):
        if self.array.size == 0:
            return None
        return self.array.remove(self.array.size - 1)

    def size(self):
        return self.array.size


class CircularQueue:
    """FIFO melingkar: front/rear berputar, dequeue tidak menggeser apa pun."""

    def __init__(self, capacity=4):
        self.capacity = capacity
        self.data = [None] * capacity
        self.front = 0
        self.rear = 0
        self.count = 0

    def enqueue(self, v):
        if self.count == self.capacity:
            self._grow()
        self.data[self.rear] = v
        self.rear = (self.rear + 1) % self.capacity
        self.count += 1

    def dequeue(self):
        if self.count == 0:
            return None
        v = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return v

    def enqueue_front(self, v):
        if self.count == self.capacity:
            self._grow()
        self.front = (self.front - 1) % self.capacity
        self.data[self.front] = v
        self.count += 1

    def dequeue_back(self):
        if self.count == 0:
            return None
        self.rear = (self.rear - 1) % self.capacity
        v = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        return v

    def size(self):
        return self.count

    def _grow(self):
        baru = [None] * (self.capacity * 2)
        k = 0
        while k < self.count:
            baru[k] = self.data[(self.front + k) % self.capacity]
            k += 1
        self.data = baru
        self.capacity *= 2
        self.front = 0
        self.rear = self.count
