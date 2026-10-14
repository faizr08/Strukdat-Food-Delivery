"""
backend/M1_Pesanan.py - Milestone 1: Custom Data Structures (Dynamic Array & Doubly Linked List)
Proyek "2EZ4U APP" - Struktur Data & Analisa Algoritma
"""

import csv
import os

class NodeDLL:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        new_node = NodeDLL(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    def get(self, index):
        if index < 0 or index >= self.size:
            return None
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data


class DynamicArray:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self._data = [None] * self.capacity

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self._data[i]
        self._data = new_data
        self.capacity = new_capacity

    def append(self, item):
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        self._data[self.size] = item
        self.size += 1

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        return self._data[index]

    def set(self, index, item):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        self._data[index] = item


class PesananRecord:
    def __init__(self, oid, nama_pelanggan, menu, harga, t_selesai_detik, prioritas=1):
        self.oid = str(oid)
        self.nama_pelanggan = str(nama_pelanggan)
        self.menu = str(menu)
        try:
            self.harga = float(harga)
        except ValueError:
            self.harga = 0.0
        try:
            self.t_selesai_detik = int(t_selesai_detik)
        except ValueError:
            self.t_selesai_detik = 0
        try:
            self.prioritas = int(prioritas)
        except ValueError:
            self.prioritas = 1

    def get_prioritas_teks(self):
        if 1 <= self.prioritas <= 3:
            return ("VIP", "PRIORITAS", "REGULER")[self.prioritas - 1]
        return "REGULER"


def muat_data_pesanan(filepath="Data/pesanan.csv"):
    array_pesanan = DynamicArray()
    if not os.path.exists(filepath):
        return array_pesanan

    try:
        with open(filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                record = PesananRecord(
                    oid=row.get('oid') or row.get('ID') or '0',
                    nama_pelanggan=row.get('nama_pelanggan') or row.get('Nama') or 'Umum',
                    menu=row.get('menu') or row.get('Menu') or 'Paket Reguler',
                    harga=row.get('harga') or row.get('Harga') or 0,
                    t_selesai_detik=row.get('t_selesai_detik') or row.get('Waktu') or 0,
                    prioritas=row.get('prioritas') or 1
                )
                array_pesanan.append(record)
    except Exception as e:
        print(f"Error memuat file pesanan: {e}")

    return array_pesanan