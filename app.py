"""
backend/m1_pesanan.py - Milestone 1: Dynamic Array vs Doubly Linked List
Proyek "2EZ4U APP" - Struktur Data & Analisa Algoritma (EC234303)
"""

import csv

class Pesanan:
    """Model penampung data untuk 1 pesanan."""
    __slots__ = ('oid', 'pelanggan', 'resto', 'menu', 'harga', 'prioritas', 't_masuk_detik', 't_selesai_detik', 'status')

    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas, t_masuk_detik, t_selesai_detik=None, status="ANTRE"):
        self.oid = str(oid)
        self.pelanggan = str(pelanggan)
        self.resto = str(resto)
        self.menu = str(menu)
        self.harga = int(harga) if harga else 0
        self.prioritas = int(prioritas) if prioritas else 3  # 1: VIP, 2: PRIORITAS, 3: REGULER
        self.t_masuk_detik = int(t_masuk_detik) if t_masuk_detik else 0
        self.t_selesai_detik = int(float(t_selesai_detik)) if t_selesai_detik and str(t_selesai_detik).strip() != '' else None
        self.status = str(status)

    def __repr__(self):
        p_map = {1: "VIP", 2: "PRIORITAS", 3: "REGULER"}
        return f"[{self.oid}] {self.pelanggan} | {self.menu} ({self.resto}) | Rp{self.harga:,} | {p_map.get(self.prioritas, 'REGULER')} | {self.status}"


class DynamicArray:
    """
    Implementasi Dynamic Array murni dengan penggandaan kapasitas (Amortized O(1)).
    Dilarang menggunakan method bawaan .append() atau .insert() dari list Python.
    """
    def __init__(self, initial_capacity=4):
        self.capacity = initial_capacity
        self.size = 0
        self.data = [None] * self.capacity

    def _resize(self, new_capacity):
        """Alokasi memori baru berukuran 2x lipat dan salin elemen lama - O(n)."""
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def append(self, pesanan):
        """Tambah REGULER di paling belakang - Amortized O(1)."""
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        self.data[self.size] = pesanan
        self.size += 1

    def insert(self, index, pesanan):
        """Tambah di indeks tertentu (PRIORITAS / VIP) - O(n) karena menggeser elemen."""
        if index < 0:
            index = 0
        if index > self.size:
            index = self.size

        if self.size == self.capacity:
            self._resize(self.capacity * 2)

        # Geser elemen ke kanan
        for i in range(self.size, index, -1):
            self.data[i] = self.data[i - 1]

        self.data[index] = pesanan
        self.size += 1

    def get(self, index):
        """Akses acak langsung berdasar indeks - O(1)."""
        if 0 <= index < self.size:
            return self.data[index]
        return None

    def delete(self, index):
        """Hapus elemen pada indeks ke-i - O(n) karena menggeser elemen."""
        if index < 0 or index >= self.size:
            return None
        removed = self.data[index]
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        self.data[self.size - 1] = None
        self.size -= 1
        return removed

    def insert_by_priority(self, pesanan):
        """
        Aturan Bisnis M1:
        - REGULER (3): Paling belakang (append) -> Amortized O(1)
        - PRIORITAS (2): Serobot ke tengah (insert di size // 2) -> O(n)
        - VIP (1): Langsung ke urutan pertama (insert di 0) -> O(n)
        """
        if pesanan.prioritas == 3:
            self.append(pesanan)
        elif pesanan.prioritas == 2:
            self.insert(self.size // 2, pesanan)
        elif pesanan.prioritas == 1:
            self.insert(0, pesanan)
        else:
            self.append(pesanan)

    def __len__(self):
        return self.size


class Node:
    """Simpul untuk Doubly Linked List."""
    __slots__ = ('data', 'next', 'prev')

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class LinkedList:
    """
    Implementasi Doubly Linked List murni dengan pointer Head dan Tail.
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, pesanan):
        """Tambah REGULER di paling belakang (Tail) - O(1)."""
        new_node = Node(pesanan)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def prepend(self, pesanan):
        """Tambah VIP di paling depan (Head) - O(1)."""
        new_node = Node(pesanan)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def insert_at(self, index, pesanan):
        """Tambah PRIORITAS di tengah - O(n) telusur simpul."""
        if index <= 0:
            self.prepend(pesanan)
            return
        if index >= self.size:
            self.append(pesanan)
            return

        new_node = Node(pesanan)
        curr = self.head
        for _ in range(index):
            curr = curr.next

        prev_node = curr.prev
        prev_node.next = new_node
        new_node.prev = prev_node
        new_node.next = curr
        curr.prev = new_node
        self.size += 1

    def get(self, index):
        """Akses sekuensial - O(n)."""
        if index < 0 or index >= self.size:
            return None
        # Optimasi: Telusur dari Head jika < size/2, dari Tail jika >= size/2
        if index < self.size // 2:
            curr = self.head
            for _ in range(index):
                curr = curr.next
        else:
            curr = self.tail
            for _ in range(self.size - 1 - index):
                curr = curr.prev
        return curr.data

    def delete(self, index):
        """Hapus pesanan ke-i - O(n) telusur."""
        if index < 0 or index >= self.size:
            return None

        if self.size == 1:
            removed = self.head.data
            self.head = None
            self.tail = None
            self.size = 0
            return removed

        if index == 0:
            removed = self.head.data
            self.head = self.head.next
            self.head.prev = None
            self.size -= 1
            return removed

        if index == self.size - 1:
            removed = self.tail.data
            self.tail = self.tail.prev
            self.tail.next = None
            self.size -= 1
            return removed

        curr = self.head
        for _ in range(index):
            curr = curr.next

        removed = curr.data
        curr.prev.next = curr.next
        curr.next.prev = curr.prev
        self.size -= 1
        return removed

    def insert_by_priority(self, pesanan):
        """
        Aturan Bisnis M1:
        - REGULER (3): Paling belakang (append) -> O(1)
        - PRIORITAS (2): Serobot ke tengah (insert_at) -> O(n) telusur
        - VIP (1): Paling depan (prepend) -> O(1)
        """
        if pesanan.prioritas == 3:
            self.append(pesanan)
        elif pesanan.prioritas == 2:
            self.insert_at(self.size // 2, pesanan)
        elif pesanan.prioritas == 1:
            self.prepend(pesanan)
        else:
            self.append(pesanan)

    def __len__(self):
        return self.size


def muat_data_csv(filepath, limit=None):
    """Memuat data CSV pesanan ke DynamicArray dan LinkedList."""
    arr = DynamicArray()
    ll = LinkedList()

    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)  # Skip header

        count = 0
        for row in reader:
            if not row or len(row) < 9:
                continue
            oid, pelanggan, resto, menu, harga, prioritas, t_masuk, t_selesai, status = row[:9]
            p = Pesanan(oid, pelanggan, resto, menu, harga, prioritas, t_masuk, t_selesai, status)
            arr.append(p)
            ll.append(p)
            count += 1
            if limit and count >= limit:
                break

    return arr, ll