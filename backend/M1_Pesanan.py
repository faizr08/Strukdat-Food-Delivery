"""
backend/m1_pesanan.py - Milestone 1: Dynamic Array vs Doubly Linked List
Proyek "2EZ4U APP" - Struktur Data & Analisa Algoritma (EC234303)
"""

import csv
import time

class Pesanan:
    """Model representasi satu pesanan."""
    __slots__ = ('oid', 'pelanggan', 'resto', 'menu', 'harga', 'prioritas', 't_masuk_detik', 't_selesai_detik', 'status')

    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas, t_masuk, t_selesai=None, status="ANTRE"):
        self.oid = str(oid).strip()
        self.pelanggan = str(pelanggan).strip()
        self.resto = str(resto).strip()
        self.menu = str(menu).strip()
        self.harga = int(float(harga)) if harga and str(harga).strip() else 0
        self.prioritas = int(prioritas) if prioritas and str(prioritas).strip() else 3
        self.t_masuk_detik = int(float(t_masuk)) if t_masuk and str(t_masuk).strip() else 0
        self.t_selesai_detik = int(float(t_selesai)) if t_selesai and str(t_selesai).strip() else None
        self.status = str(status).strip()

    def prioritas_nama(self):
        return ("VIP", "PRIORITAS", "REGULER")[self.prioritas - 1] if 1 <= self.prioritas <= 3 else "REGULER"

    def __repr__(self):
        return f"[{self.oid}] {self.pelanggan} | {self.menu} ({self.resto}) | Rp{self.harga:,} | {self.prioritas_nama()} | {self.status}"


class DynamicArray:
    """Dynamic Array murni dengan penggandaan kapasitas (Amortized O(1))."""
    def __init__(self, initial_capacity=4, capacity=None):
        cap = capacity if capacity is not None else initial_capacity
        self.capacity, self.size = max(cap, 4), 0
        self.data = [None] * self.capacity

    def _resize(self, new_cap):
        new_data = [None] * new_cap
        new_data[:self.size] = self.data[:self.size]
        self.data, self.capacity = new_data, new_cap

    def append(self, item):
        """Tambah REGULER di paling belakang - Amortized O(1)."""
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        self.data[self.size] = item
        self.size += 1

    def insert(self, idx, item):
        """Tambah PRIORITAS / VIP - O(n) geser elemen."""
        idx = max(0, min(idx, self.size))
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        self.data[idx + 1:self.size + 1] = self.data[idx:self.size]
        self.data[idx] = item
        self.size += 1

    def get(self, idx):
        """Akses acak langsung O(1)."""
        return self.data[idx] if 0 <= idx < self.size else None

    def delete(self, idx):
        """Hapus elemen indeks ke-i - O(n) geser elemen."""
        if not (0 <= idx < self.size):
            return None
        removed = self.data[idx]
        self.data[idx:self.size - 1] = self.data[idx + 1:self.size]
        self.data[self.size - 1] = None
        self.size -= 1
        return removed

    def insert_by_priority(self, p):
        """Aturan bisnis: VIP (0), PRIORITAS (n//2), REGULER (belakang)."""
        if p.prioritas == 1: self.insert(0, p)
        elif p.prioritas == 2: self.insert(self.size // 2, p)
        else: self.append(p)

    def to_primitive_list(self):
        return self.data[:self.size]

    def __len__(self):
        return self.size


class Node:
    """Simpul Doubly Linked List."""
    __slots__ = ('data', 'next', 'prev')
    def __init__(self, data, prev=None, next=None):
        self.data, self.prev, self.next = data, prev, next


class LinkedList:
    """Doubly Linked List murni dengan Head dan Tail."""
    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def _node_at(self, idx):
        """Helper penelusuran dua arah O(n)."""
        if idx < self.size // 2:
            curr = self.head
            for _ in range(idx): curr = curr.next
        else:
            curr = self.tail
            for _ in range(self.size - 1 - idx): curr = curr.prev
        return curr

    def append(self, item):
        """Tambah REGULER di Tail - O(1)."""
        new_node = Node(item, prev=self.tail)
        if not self.head: self.head = self.tail = new_node
        else: self.tail.next = self.tail = new_node
        self.size += 1

    def prepend(self, item):
        """Tambah VIP di Head - O(1)."""
        new_node = Node(item, next=self.head)
        if not self.head: self.head = self.tail = new_node
        else: self.head.prev = self.head = new_node
        self.size += 1

    def insert_at(self, idx, item):
        """Tambah PRIORITAS di tengah - O(n) telusur simpul."""
        if idx <= 0: return self.prepend(item)
        if idx >= self.size: return self.append(item)
        curr = self._node_at(idx)
        new_node = Node(item, prev=curr.prev, next=curr)
        curr.prev.next = curr.prev = new_node
        self.size += 1

    def get(self, idx):
        """Akses sekuensial simpul O(n)."""
        return self._node_at(idx).data if 0 <= idx < self.size else None

    def delete(self, idx):
        """Hapus simpul ke-i - O(n) telusur & perbarui pointer."""
        if not (0 <= idx < self.size):
            return None
        curr = self._node_at(idx)
        if curr.prev: curr.prev.next = curr.next
        else: self.head = curr.next
        if curr.next: curr.next.prev = curr.prev
        else: self.tail = curr.prev
        self.size -= 1
        return curr.data

    def insert_by_priority(self, p):
        """Aturan bisnis: VIP (Head), PRIORITAS (Tengah), REGULER (Tail)."""
        if p.prioritas == 1: self.prepend(p)
        elif p.prioritas == 2: self.insert_at(self.size // 2, p)
        else: self.append(p)

    def to_primitive_list(self):
        res, curr = [None] * self.size, self.head
        idx = 0
        while curr:
            res[idx] = curr.data
            curr, idx = curr.next, idx + 1
        return res

    def __len__(self):
        return self.size


def muat_data_csv(filepath, limit=None):
    """Memuat data CSV pesanan ke DynamicArray dan LinkedList."""
    t0 = time.perf_counter()
    arr, ll, count = DynamicArray(capacity=1024), LinkedList(), 0
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # Lewati header
        for r in reader:
            if not r or len(r) < 9: continue
            p = Pesanan(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8])
            arr.append(p)
            ll.append(p)
            count += 1
            if limit and count >= limit: break
    return arr, ll, time.perf_counter() - t0
