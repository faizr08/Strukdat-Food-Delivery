"""M1 - Dua struktur data dasar: Array (larik) dan LinkedList (rantai).

Hanya berisi kelas struktur datanya saja. Semua logika aplikasi ada di
frontend/ui.py, yang membuat objeknya dan memanggil method di sini.
"""


class Array:
    """Larik dinamis. Menyimpan data dan mencatat jumlah geseran/penyalinan."""

    def __init__(self, capacity=4):
        self.data = [None] * capacity
        self.capacity = capacity
        self.size = 0
        self.shifts = 0
        self.copies = 0

    def get(self, i):
        if 0 <= i < self.size:
            return self.data[i]
        return None

    def insert(self, i, v):
        """Sisipkan v di posisi i. Elemen setelahnya bergeser ke kanan."""
        if i < 0:
            i = 0
        if i > self.size:
            i = self.size
        if self.size == self.capacity:
            self._grow()
        j = self.size
        while j > i:
            self.data[j] = self.data[j - 1]
            j -= 1
            self.shifts += 1
        self.data[i] = v
        self.size += 1

    def remove(self, i):
        """Ambil elemen ke-i. Elemen setelahnya bergeser ke kiri."""
        if not (0 <= i < self.size):
            return None
        nilai = self.data[i]
        j = i
        while j < self.size - 1:
            self.data[j] = self.data[j + 1]
            j += 1
            self.shifts += 1
        self.data[self.size - 1] = None
        self.size -= 1
        return nilai

    def _grow(self):
        baru = [None] * (self.capacity * 2)
        i = 0
        while i < self.size:
            baru[i] = self.data[i]
            i += 1
        self.data = baru
        self.capacity *= 2
        self.copies += self.size


class Node:
    """Satu simpul rantai: menyimpan data dan alamat simpul berikutnya."""

    __slots__ = ("data", "next")

    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    """Rantai simpul. Menyimpan head/tail dan mencatat jumlah telusuran."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.traversals = 0

    def get(self, i):
        if not (0 <= i < self.size):
            return None
        return self._node_at(i).data

    def insert(self, i, v):
        """Sisipkan v di posisi i. Di ujung cukup mengubah petunjuk."""
        if i <= 0:
            self.head = Node(v, self.head)
            if self.tail is None:
                self.tail = self.head
        elif i >= self.size:
            self.tail.next = Node(v)
            self.tail = self.tail.next
        else:
            sebelum = self._node_at(i - 1)
            sebelum.next = Node(v, sebelum.next)
        self.size += 1

    def remove(self, i):
        """Ambil elemen ke-i. Rantai disambung ulang melewatinya."""
        if not (0 <= i < self.size):
            return None
        if i == 0:
            node = self.head
            self.head = node.next
            if self.head is None:
                self.tail = None
        else:
            sebelum = self._node_at(i - 1)
            node = sebelum.next
            sebelum.next = node.next
            if node is self.tail:
                self.tail = sebelum
        self.size -= 1
        return node.data

    def _node_at(self, i):
        node = self.head
        k = 0
        while k < i:
            node = node.next
            k += 1
            self.traversals += 1
        return node
