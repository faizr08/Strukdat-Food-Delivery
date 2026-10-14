"""
backend/m2_antrean.py - Milestone 2: Stack & Queue
Proyek "2EZ4U APP" - Struktur Data & Analisa Algoritma (EC234303)

Aturan: Dilarang menggunakan dict, set, sorted, .sort(), heapq, collections.*.
Hanya gunakan list primitif, tuple, int, float, str, I/O.
"""

import time

class Tumpukan:
    """
    Implementasi Stack (LIFO) murni di atas Dynamic Array.
    """
    def __init__(self, initial_capacity=8):
        self.capacity = initial_capacity if initial_capacity > 0 else 8
        self.count = 0
        self.data = [None] * self.capacity

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self.count):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def push(self, item):
        if self.count == self.capacity:
            self._resize(self.capacity * 2)
        self.data[self.count] = item
        self.count += 1

    def pop(self):
        if self.count == 0:
            return None
        self.count -= 1
        item = self.data[self.count]
        self.data[self.count] = None
        return item

    def peek(self):
        if self.count == 0:
            return None
        return self.data[self.count - 1]

    def is_empty(self):
        return self.count == 0

    def size(self):
        return self.count

    def clear(self):
        self.count = 0
        self.capacity = 8
        self.data = [None] * self.capacity

    def to_list(self):
        res = [None] * self.count
        for i in range(self.count):
            res[i] = self.data[i]
        return res


# ==========================================
# Bagian A: Mesin Kasir Infix -> Postfix -> Evaluasi
# ==========================================

def tokenize_ekspresi(expr):
    """
    Memecah string ekspresi matematika infix menjadi list token.
    Mendukung angka bernilai besar (multi-digit) dan operator +, -, *, /, (, ).
    """
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        c = expr[i]
        if c == ' ' or c == '\t':
            i += 1
            continue
        if c in '+-*/()':
            tokens.append(c)
            i += 1
        elif c.isdigit() or c == '.':
            start = i
            while i < n and (expr[i].isdigit() or expr[i] == '.'):
                i += 1
            tokens.append(expr[start:i])
        else:
            i += 1
    return tokens


def prioritas_operator(op):
    if op in ('*', '/'):
        return 2
    if op in ('+', '-'):
        return 1
    return 0


def ke_postfix(ekspresi):
    """
    Mengubah ekspresi infix ke postfix menggunakan Stack operator.
    Mengembalikan: (postfix_tokens, postfix_str, list_langkah)
    list_langkah memuat tuple (token, tindakan, snapshot_stack, snapshot_output)
    """
    tokens = tokenize_ekspresi(ekspresi)
    stack_op = Tumpukan()
    output = []
    langkah = []

    for token in tokens:
        if token.isdigit() or ('.' in token and token.replace('.', '', 1).isdigit()):
            output.append(token)
            langkah.append((token, "angka, langsung keluar", " ".join([str(x) for x in stack_op.to_list()]), " ".join(output)))
        elif token == '(':
            stack_op.push(token)
            langkah.append((token, "push (", " ".join([str(x) for x in stack_op.to_list()]), " ".join(output)))
        elif token == ')':
            while not stack_op.is_empty() and stack_op.peek() != '(':
                output.append(stack_op.pop())
            if not stack_op.is_empty() and stack_op.peek() == '(':
                stack_op.pop()  # buang '('
            langkah.append((token, "pop sampai (, buang (", " ".join([str(x) for x in stack_op.to_list()]), " ".join(output)))
        elif token in ('+', '-', '*', '/'):
            p_curr = prioritas_operator(token)
            while (not stack_op.is_empty() and stack_op.peek() != '(' and
                   prioritas_operator(stack_op.peek()) >= p_curr):
                popped = stack_op.pop()
                output.append(popped)
            stack_op.push(token)
            langkah.append((token, f"push {token}", " ".join([str(x) for x in stack_op.to_list()]), " ".join(output)))

    # Pop seluruh sisa stack
    while not stack_op.is_empty():
        op = stack_op.pop()
        if op != '(':
            output.append(op)
    langkah.append(("akhir", "pop sisa stack", "kosong", " ".join(output)))

    return output, " ".join(output), langkah


def hitung_postfix(postfix_tokens):
    """
    Mengevaluasi postfix menggunakan Stack nilai.
    Operand kanan keluar pertama (b = pop(), a = pop(), hitung a op b).
    Mengembalikan: (total_nilai, list_langkah)
    """
    if isinstance(postfix_tokens, str):
        postfix_tokens = tokenize_ekspresi(postfix_tokens)

    stack_val = Tumpukan()
    langkah = []

    for token in postfix_tokens:
        if token.isdigit() or ('.' in token and token.replace('.', '', 1).isdigit()):
            val = float(token) if '.' in token else int(token)
            stack_val.push(val)
            snap = " ".join([str(x) for x in stack_val.to_list()])
            langkah.append((token, f"push {val}", snap))
        elif token in ('+', '-', '*', '/'):
            b = stack_val.pop()
            a = stack_val.pop()
            if a is None or b is None:
                continue

            if token == '+':
                res = a + b
            elif token == '-':
                res = a - b
            elif token == '*':
                res = a * b
            elif token == '/':
                res = a // b if (isinstance(a, int) and isinstance(b, int) and a % b == 0) else a / b

            stack_val.push(res)
            snap = " ".join([str(x) for x in stack_val.to_list()])
            langkah.append((token, f"pop {b} dan {a} -> {a} {token} {b} = {res}", snap))

    total = stack_val.pop()
    if total is None:
        total = 0
    return total, langkah


# ==========================================
# Bagian B: Dua Versi Antrean (Naif vs Melingkar)
# ==========================================

class AntreanNaif:
    """
    Implementasi antrean naif di atas array biasa.
    dequeue() mengambil index 0 lalu menggeser sisa elemen ke kiri -> O(n).
    """
    def __init__(self, initial_capacity=16):
        self.capacity = initial_capacity
        self.size = 0
        self.data = [None] * self.capacity
        self.total_geseran = 0
        self.geseran_terakhir = 0

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def enqueue(self, pesanan):
        """Menambah di belakang antrean - Amortized O(1)."""
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        self.data[self.size] = pesanan
        self.size += 1

    def dequeue(self):
        """
        Mengambil elemen terdepan (indeks 0).
        Semua sisa elemen digeser 1 posisi ke kiri - O(n).
        """
        if self.size == 0:
            self.geseran_terakhir = 0
            return None
        front_val = self.data[0]
        # Geser seluruh elemen ke kiri
        shift_count = self.size - 1
        for i in range(shift_count):
            self.data[i] = self.data[i + 1]
        self.data[self.size - 1] = None
        self.size -= 1
        self.geseran_terakhir = shift_count
        self.total_geseran += shift_count
        return front_val

    def push_front(self, pesanan):
        """Digunakan untuk UNDO Dequeue: mengembalikan ke depan antrean."""
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        for i in range(self.size, 0, -1):
            self.data[i] = self.data[i - 1]
        self.data[0] = pesanan
        self.size += 1

    def pop_back(self):
        """Digunakan untuk UNDO Enqueue: mengeluarkan dari belakang antrean."""
        if self.size == 0:
            return None
        val = self.data[self.size - 1]
        self.data[self.size - 1] = None
        self.size -= 1
        return val

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size


class AntreanMelingkar:
    """
    Implementasi Antrean Melingkar (Circular Queue) berpenunjuk front & rear.
    dequeue() hanya menggeser pointer front -> O(1), 0 elemen digeser!
    """
    def __init__(self, capacity=32768):
        self.capacity = capacity if capacity > 0 else 32768
        self.data = [None] * self.capacity
        self.front = 0
        self.rear = 0
        self.count = 0
        self.total_geseran = 0
        self.geseran_terakhir = 0

    def _resize(self, new_capacity):
        """Penggandaan kapasitas saat penuh dengan menyusun ulang secara sekuensial."""
        new_data = [None] * new_capacity
        for i in range(self.count):
            new_data[i] = self.data[(self.front + i) % self.capacity]
        self.data = new_data
        self.front = 0
        self.rear = self.count
        self.capacity = new_capacity

    def enqueue(self, pesanan):
        """Menambahkan elemen di rear - O(1), 0 elemen digeser."""
        if self.count == self.capacity:
            self._resize(self.capacity * 2)
        self.data[self.rear] = pesanan
        self.rear = (self.rear + 1) % self.capacity
        self.count += 1
        self.geseran_terakhir = 0

    def dequeue(self):
        """
        Mengambil elemen di front - O(1).
        Hanya memajukan pointer front, 0 elemen digeser!
        """
        if self.count == 0:
            self.geseran_terakhir = 0
            return None
        val = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        self.geseran_terakhir = 0
        return val

    def push_front(self, pesanan):
        """
        Digunakan untuk UNDO Dequeue: mengembalikan pesanan ke DEPAN antrean.
        front dimundurkan 1 posisi secara melingkar - O(1)!
        """
        if self.count == self.capacity:
            self._resize(self.capacity * 2)
        self.front = (self.front - 1 + self.capacity) % self.capacity
        self.data[self.front] = pesanan
        self.count += 1

    def pop_back(self):
        """
        Digunakan untuk UNDO Enqueue: mengeluarkan pesanan dari BELAKANG antrean.
        rear dimundurkan 1 posisi secara melingkar - O(1)!
        """
        if self.count == 0:
            return None
        self.rear = (self.rear - 1 + self.capacity) % self.capacity
        val = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        return val

    def peek(self):
        if self.count == 0:
            return None
        return self.data[self.front]

    def is_empty(self):
        return self.count == 0

    def __len__(self):
        return self.count


# ==========================================
# Bagian C: Pengelola Undo & Redo (Aksi Antrean)
# ==========================================

class UndoRedoManager:
    """
    Manajemen Stack Undo & Redo untuk aksi transaksi pesanan.
    Setiap aksi baru membersihkan tumpukan Redo untuk mencegah percabangan riwayat.
    """
    def __init__(self):
        self.undo_stack = Tumpukan()
        self.redo_stack = Tumpukan()

    def catat_aksi(self, tipe_aksi, data):
        """
        tipe_aksi: 'ENQUEUE' atau 'DEQUEUE'
        data: objek pesanan atau list of objek pesanan
        """
        self.undo_stack.push((tipe_aksi, data))
        self.redo_stack.clear()

    def undo(self, q_naif, q_circ):
        """
        Membatalkan aksi terakhir.
        - Jika aksi terakhir ENQUEUE: keluarkan lagi dari belakang antrean.
        - Jika aksi terakhir DEQUEUE: kembalikan semua pesanan ke DEPAN antrean.
        """
        if self.undo_stack.is_empty():
            return None, "Tumpukan undo kosong, tidak ada aksi untuk dibatalkan."

        tipe_aksi, data = self.undo_stack.pop()

        if tipe_aksi == 'ENQUEUE':
            # Data adalah pesanan tunggal yang baru di-enqueue
            p_naif = q_naif.pop_back()
            p_circ = q_circ.pop_back()
            self.redo_stack.push(('ENQUEUE', data))
            return ('ENQUEUE', data), f"Pesanan {data.oid if hasattr(data, 'oid') else data} dikeluarkan lagi dari belakang antrean."

        elif tipe_aksi == 'DEQUEUE':
            # Data adalah list pesanan yang baru saja keluar (dalam urutan keluar)
            # Kembalikan ke DEPAN secara terbalik agar urutannya tetap sama persis!
            # Misal keluar [A, B], maka jika dimasukkan dari belakang list [B, A], front akan berisi A lalu B.
            pesanan_list = data
            n_items = len(pesanan_list)
            for i in range(n_items - 1, -1, -1):
                p = pesanan_list[i]
                q_naif.push_front(p)
                q_circ.push_front(p)
            self.redo_stack.push(('DEQUEUE', data))
            return ('DEQUEUE', data), f"{n_items} pesanan dikembalikan ke DEPAN antrean circular."

        return None, "Tipe aksi tidak dikenali."

    def redo(self, q_naif, q_circ):
        """
        Mengerjakan ulang aksi yang baru saja dibatalkan.
        """
        if self.redo_stack.is_empty():
            return None, "Tumpukan redo kosong, tidak ada yang diulang."

        tipe_aksi, data = self.redo_stack.pop()

        if tipe_aksi == 'ENQUEUE':
            q_naif.enqueue(data)
            q_circ.enqueue(data)
            self.undo_stack.push(('ENQUEUE', data))
            return ('ENQUEUE', data), f"Pesanan {data.oid if hasattr(data, 'oid') else data} masuk kembali ke belakang antrean."

        elif tipe_aksi == 'DEQUEUE':
            pesanan_list = data
            n_items = len(pesanan_list)
            for _ in range(n_items):
                q_naif.dequeue()
                q_circ.dequeue()
            self.undo_stack.push(('DEQUEUE', data))
            return ('DEQUEUE', data), f"{n_items} pesanan keluar lagi dari antrean circular."

        return None, "Tipe aksi tidak dikenali."

    def stats(self):
        return {
            'undo_depth': self.undo_stack.size(),
            'redo_depth': self.redo_stack.size()
        }
