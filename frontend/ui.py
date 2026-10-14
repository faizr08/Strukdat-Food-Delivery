"""Antarmuka 2EZ4U - satu jendela Tkinter untuk M1, M2, dan M3.

Berkas ini memakai struktur data di backend: di sini objek Array, LinkedList,
Stack, dan kedua antrean dibuat, diisi dari CSV, lalu dijalankan. Algoritma
pengurutan dan pencarian M3 juga dipanggil dari sini. Struktur dan algoritmanya
sendiri tetap di backend/m1_pesanan.py, m2_antrean.py, dan m3_laporan.py.

Tata letak: daftar menu di kiri, form parameter dan hasil di kanan, panel
COMMAND di bawah. Setiap aksi mengerjakan hal yang sama pada struktur
pembanding (Array vs LinkList, antrean naif vs melingkar) supaya waktunya bisa
diadu langsung.
"""

import csv
import os
import time
import tkinter as tk
from tkinter import ttk, messagebox

from backend.m1_pesanan import Array, LinkedList
from backend.m2_antrean import Stack, NaiveQueue, CircularQueue
from backend.m3_laporan import (
    insertion_sort, merge_sort, linear_search, binary_search)

JUDUL = "2EZ4U - Struktur Data (M1, M2 & M3)"

BATAS_INSERTION = 5000

AKAR_PROYEK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_BAWAAN = os.path.join(AKAR_PROYEK, "data", "pesanan.csv")

MENU = (
    ("ARRAY", (
        ("A_LIHAT", "ARRAY - LIHAT PESANAN", "lihat", "array", "no",
         "Buka detail satu pesanan. Array O(1) karena alamat dihitung langsung, "
         "LinkList O(n) karena harus menelusuri simpul."),
        ("A_REG", "ARRAY - TAMBAH PESANAN REGULER", "tambah", "array", "reguler",
         "Pesanan reguler masuk barisan paling belakang. Keduanya O(1); Array "
         "hanya sesekali menyalin saat kapasitas berlipat."),
        ("A_PRI", "ARRAY - TAMBAH PESANAN PRIORITAS", "tambah", "array", "prioritas",
         "Pesanan prioritas menyerobot ke tengah (size // 2). Array menggeser "
         "separuh isi, LinkList menelusuri separuh simpul."),
        ("A_VIP", "ARRAY - TAMBAH PESANAN VIP", "tambah", "array", "vip",
         "Pesanan VIP langsung ke urutan pertama. Array menggeser seluruh isi, "
         "LinkList hanya mengubah satu petunjuk."),
        ("A_HAPUS", "ARRAY - HAPUS PESANAN", "hapus", "array", "no",
         "Pesanan dicabut dari barisan. Array menggeser sisa isi, LinkList "
         "menelusuri sampai simpul sebelumnya."),
    )),
    ("LINKED LIST", (
        ("L_LIHAT", "LINKED LIST - LIHAT PESANAN", "lihat", "link", "no",
         "Sama dengan ARRAY - LIHAT PESANAN, tetapi yang disorot waktu LinkList."),
        ("L_REG", "LINKED LIST - TAMBAH PESANAN REGULER", "tambah", "link", "reguler",
         "Menempel di ujung belakang lewat penunjuk tail, O(1) tanpa telusur."),
        ("L_PRI", "LINKED LIST - TAMBAH PESANAN PRIORITAS", "tambah", "link", "prioritas",
         "Menelusuri sampai tengah lalu menyambung sekali, O(n)."),
        ("L_VIP", "LINKED LIST - TAMBAH PESANAN VIP", "tambah", "link", "vip",
         "Mengubah satu petunjuk saja, O(1), tidak ada yang digeser."),
        ("L_HAPUS", "LINKED LIST - HAPUS PESANAN", "hapus", "link", "no",
         "Telusuri sampai simpul sebelum yang dicabut, potong rantai."),
    )),
    ("STACK", (
        ("S_POST", "STACK - POSTFIX (MESIN KASIR)", "postfix", "stack", "ekspresi",
         "Ubah struk infix menjadi postfix lalu hitung totalnya memakai Stack."),
        ("S_UNDO", "STACK - UNDO LAST", "undo", "stack", "",
         "Batalkan aksi antrean terakhir memakai tumpukan undo."),
        ("S_REDO", "STACK - REDO LAST", "redo", "stack", "",
         "Kerjakan ulang aksi yang baru dibatalkan; aksi baru mengosongkan redo."),
    )),
    ("QUEUE", (
        ("Q_ENQ", "QUEUE - ENQUEUE", "enqueue", "queue", "order",
         "Tambah satu pesanan ke belakang KEDUA antrean (naif dan melingkar)."),
        ("Q_DQN", "QUEUE - DEQUEUE NAIF", "dequeue_naif", "queue", "jumlah",
         "Keluarkan n pesanan dari depan; versi naif menggeser seluruh sisa isi."),
        ("Q_DQC", "QUEUE - DEQUEUE CIRCULAR", "dequeue_circular", "queue", "jumlah",
         "Keluarkan n pesanan dari depan; versi melingkar hanya memajukan front."),
    )),
    ("SORT", (
        ("S3_INS", "SORT - INSERTION SORT", "sort_insertion", "array", "sort_kecil",
         "Urutkan data kecil dengan insertion sort. Stabil. O(n^2); menolak "
         "data lebih dari 5.000 baris supaya tidak membeku."),
        ("S3_MRG", "SORT - MERGE SORT", "sort_merge", "link", "sort_besar",
         "Urutkan data besar dengan merge sort. Stabil. O(n log n)."),
    )),
    ("SEARCH", (
        ("S4_LIN", "SEARCH - LINEAR SEARCH", "search_linear", "array", "cari",
         "Cari oid dengan menelusuri satu per satu. O(n); tidak butuh data terurut."),
        ("S4_BIN", "SEARCH - BINARY SEARCH", "search_binary", "link", "cari",
         "Cari oid pada daftar terurut. O(log n); daftar oid diurutkan dulu "
         "sekali dengan merge sort, ongkosnya ikut dilaporkan."),
    )),
    ("SISTEM", (
        ("S_MUAT", "MUAT ULANG DATA", "muat", "", "",
         "Baca ulang data/pesanan.csv ke semua struktur M1 dan M2."),
        ("S_CEK", "CEK KONSISTENSI", "cek", "", "",
         "Pastikan Array dan LinkList memuat urutan pesanan yang sama."),
        ("S_STAT", "STATISTIK STRUKTUR", "stat", "", "",
         "Panjang, kapasitas, geseran, dan simpul yang ditelusuri."),
        ("S_STAT2", "STATISTIK ANTREAN (M2)", "stat2", "", "",
         "Panjang kedua antrean, kapasitas, total geseran, kedalaman undo/redo."),
        ("S_CUPLIK", "CUPLIKAN 200 PESANAN", "cuplik", "", "",
         "Tampilkan 200 pesanan pertama beserta posisinya."),
    )),
)


# ------------------------------------------------------------- model

class Pesanan:
    """Satu baris pesanan, sembilan kolom seperti di CSV."""

    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas,
                 t_masuk, t_selesai, status):
        self.oid = oid
        self.pelanggan = pelanggan
        self.resto = resto
        self.menu = menu
        self.harga = harga
        self.prioritas = prioritas
        self.t_masuk = t_masuk
        self.t_selesai = t_selesai
        self.status = status

    def jenis(self):
        if self.prioritas == 1:
            return "VIP"
        if self.prioritas == 2:
            return "PRIORITAS"
        return "REGULER"

    def ringkas(self):
        return "{0} | {1:<14} | {2:<13} | {3:<18} | {4:>10} | {5:<9} | {6}".format(
            self.oid, self.pelanggan[:14], self.resto[:13], self.menu[:18],
            rupiah(self.harga), self.jenis(), self.status)

    def detail(self):
        selesai = "-" if self.t_selesai is None else str(self.t_selesai) + " dtk"
        return (
            "oid       : {0}\n"
            "pelanggan : {1}\n"
            "resto     : {2}\n"
            "menu      : {3}\n"
            "harga     : {4}\n"
            "prioritas : {5} ({6})\n"
            "t masuk   : {7} dtk\n"
            "t selesai : {8}\n"
            "status    : {9}"
        ).format(self.oid, self.pelanggan, self.resto, self.menu,
                 rupiah(self.harga), self.prioritas, self.jenis(),
                 self.t_masuk, selesai, self.status)


# ---------------------------------------------------------- utilitas

def angka(nilai, desimal=0):
    """1234567 -> '1.234.567'; 0,0234 -> '0,02' (gaya Indonesia)."""
    teks = "{0:,.{1}f}".format(float(nilai), desimal)
    return teks.replace(",", "_").replace(".", ",").replace("_", ".")


def rupiah(nilai):
    return "Rp " + angka(nilai)


def _bilangan(teks, bawaan):
    teks = (teks or "").strip()
    if teks == "":
        return bawaan
    try:
        return int(teks)
    except ValueError:
        return bawaan


def ambil_kunci(pesanan, nama):
    """Ambil nilai yang dipakai sebagai kunci pengurutan/pencarian."""
    if nama == "oid":
        return pesanan.oid
    if nama == "harga":
        return pesanan.harga
    if nama == "selesai":
        return pesanan.t_selesai if pesanan.t_selesai is not None else 0
    raise ValueError("kunci hanya boleh oid, harga, atau selesai")


# ------------------------------------------------------- mesin kasir

def tokenkan(teks):
    """Pecah struk menjadi token; kurung dipisah supaya mudah di-split."""
    return teks.replace("(", " ( ").replace(")", " ) ").split()


def _prio(op):
    if op == "*" or op == "/":
        return 2
    if op == "+" or op == "-":
        return 1
    return 0


def ke_postfix(token):
    """Ubah token infix menjadi postfix memakai Stack operator."""
    keluar = []
    tumpuk = Stack()
    for t in token:
        if t in ("+", "-", "*", "/"):
            while (not tumpuk.is_empty()) and tumpuk.peek() != "(" \
                    and _prio(tumpuk.peek()) >= _prio(t):
                keluar.append(tumpuk.pop())
            tumpuk.push(t)
        elif t == "(":
            tumpuk.push(t)
        elif t == ")":
            while (not tumpuk.is_empty()) and tumpuk.peek() != "(":
                keluar.append(tumpuk.pop())
            tumpuk.pop()
        else:
            keluar.append(t)
    while not tumpuk.is_empty():
        keluar.append(tumpuk.pop())
    return keluar


def _angka_token(t):
    try:
        return int(t)
    except ValueError:
        return float(t)


def hitung_postfix(postfix):
    """Hitung postfix memakai Stack angka; yang keluar dulu operand kanan."""
    tumpuk = Stack()
    for t in postfix:
        if t in ("+", "-", "*", "/"):
            b = tumpuk.pop()
            a = tumpuk.pop()
            if t == "+":
                tumpuk.push(a + b)
            elif t == "-":
                tumpuk.push(a - b)
            elif t == "*":
                tumpuk.push(a * b)
            else:
                if b == 0:
                    raise ValueError("pembagian dengan nol")
                tumpuk.push(a / b)
        else:
            tumpuk.push(_angka_token(t))
    return tumpuk.pop()


# ------------------------------------------------------------ jendela

class Jendela:
    def __init__(self, root, path):
        self.root = root
        self.path = path

        # objek struktur data dibuat di sini
        self.array = Array()
        self.link = LinkedList()
        self.naif = NaiveQueue()
        self.melingkar = CircularQueue()
        self.undo = Stack()
        self.redo = Stack()

        self.jumlah_muat = 0
        self.nomor_baru = 0
        self.rek_terpilih = None
        self.fokus = ""
        self.entri = []
        self.urut_oid = None

        root.title(JUDUL)
        root.geometry("1200x780")
        root.minsize(1000, 640)

        self._bangun_status()
        self._bangun_command()
        self._bangun_menu()
        self._bangun_kanan()

        self.root.after(150, self.muat_awal)

    # -------------------------------------------------- tata letak
    def _bangun_menu(self):
        self.bingkai = ttk.Frame(self.root, padding=6)
        self.bingkai.pack(side="top", fill="both", expand=True)

        kiri = ttk.LabelFrame(self.bingkai, text="MENU", padding=6)
        kiri.grid(row=0, column=0, sticky="nsw", padx=(0, 6))
        self.pohon = ttk.Treeview(kiri, show="tree", height=17, selectmode="browse")
        self.pohon.column("#0", width=300)
        self.pohon.grid(row=0, column=0, sticky="nsew")
        gulir = ttk.Scrollbar(kiri, orient="vertical", command=self.pohon.yview)
        gulir.grid(row=0, column=1, sticky="ns")
        self.pohon.configure(yscrollcommand=gulir.set)

        for grup, isi in MENU:
            self.pohon.insert("", "end", iid="G_" + grup, text=grup, open=True)
            for rek in isi:
                self.pohon.insert("G_" + grup, "end", iid=rek[0], text="  " + rek[1])
        self.pohon.bind("<<TreeviewSelect>>", self.pilih_menu)

        self.kanan = ttk.Frame(self.bingkai)
        self.kanan.grid(row=0, column=1, sticky="nsew")
        self.bingkai.columnconfigure(1, weight=1)
        self.bingkai.rowconfigure(0, weight=1)

    def _bangun_kanan(self):
        self.label_info = ttk.Label(self.kanan, text="Pilih menu di kiri untuk mulai.",
                                    wraplength=760, justify="left", foreground="#334")
        self.label_info.grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.kanan.columnconfigure(0, weight=1)

        self.kotak_form = ttk.LabelFrame(self.kanan, text="PARAMETER", padding=8)
        self.kotak_form.grid(row=1, column=0, sticky="ew")

        self.kotak_hasil = ttk.LabelFrame(self.kanan, text="HASIL", padding=8)
        self.kotak_hasil.grid(row=2, column=0, sticky="nsew", pady=6)
        self.kanan.rowconfigure(2, weight=1)

        self.teks_hasil = tk.Text(self.kotak_hasil, height=10, wrap="none",
                                  font=("DejaVu Sans Mono", 10),
                                  background="#fbfbfb", relief="flat")
        self.teks_hasil.grid(row=0, column=0, sticky="nsew")
        gulir = ttk.Scrollbar(self.kotak_hasil, orient="vertical",
                              command=self.teks_hasil.yview)
        gulir.grid(row=0, column=1, sticky="ns")
        self.teks_hasil.configure(yscrollcommand=gulir.set)
        self.kotak_hasil.columnconfigure(0, weight=1)
        self.kotak_hasil.rowconfigure(0, weight=1)
        self.teks_hasil.tag_configure("kepala", font=("DejaVu Sans Mono", 10, "bold"))
        self.teks_hasil.configure(state="disabled")

        self.kotak_adu = ttk.LabelFrame(self.kanan, text="ADU PERFORMA", padding=8)
        self.kotak_adu.grid(row=3, column=0, sticky="ew")
        self.label_array = ttk.Label(self.kotak_adu, text="Array    -")
        self.label_array.grid(row=0, column=0, sticky="w")
        self.label_link = ttk.Label(self.kotak_adu, text="LinkList -")
        self.label_link.grid(row=1, column=0, sticky="w")

    def _bangun_command(self):
        kotak = ttk.LabelFrame(self.root, text="COMMAND", padding=6)
        kotak.pack(side="bottom", fill="x", padx=6, pady=(0, 4))
        self.teks_log = tk.Text(kotak, height=7, wrap="word",
                                font=("DejaVu Sans Mono", 9),
                                background="#1e1e1e", foreground="#dcdcdc",
                                relief="flat")
        self.teks_log.grid(row=0, column=0, sticky="nsew")
        gulir = ttk.Scrollbar(kotak, orient="vertical", command=self.teks_log.yview)
        gulir.grid(row=0, column=1, sticky="ns")
        self.teks_log.configure(yscrollcommand=gulir.set)
        self.teks_log.tag_configure("perintah", foreground="#6fd06f",
                                    font=("DejaVu Sans Mono", 9, "bold"))
        self.teks_log.tag_configure("modul", foreground="#7fb8ff")
        self.teks_log.tag_configure("galat", foreground="#ff7b7b")
        kotak.columnconfigure(0, weight=1)
        kotak.rowconfigure(0, weight=1)

    def _bangun_status(self):
        self.label_status = ttk.Label(self.root, text="Memuat ...", anchor="w",
                                      padding=(8, 3))
        self.label_status.pack(side="bottom", fill="x")

    # -------------------------------------------------- pemuatan data
    def muat_awal(self):
        self._ganti_status("Memuat data dari " + self.path + " ...")
        self.root.update_idletasks()
        try:
            jumlah, ms = self.muat_data(self.path)
        except OSError:
            self._ganti_status("Berkas tidak ditemukan: " + self.path)
            self._catat("GAGAL memuat data: Berkas tidak ditemukan", "galat")
            return
        self._ganti_status(
            "dimuat {0} pesanan dalam {1} ms | array kapasitas {2} | {3} pesanan ANTRE".format(
                angka(jumlah), angka(ms, 2), angka(self.array.capacity),
                angka(self.naif.size())))
        self._catat("MUAT {0} pesanan ke Array & LinkList [{1} ms]".format(
            angka(jumlah), angka(ms, 2)), "modul")
        self._catat("M2: {0} pesanan ANTRE masuk ke KEDUA antrean".format(
            angka(self.naif.size())), "modul")

    def muat_data(self, path):
        """Baca CSV ke Array dan LinkList, lalu isi kedua antrean M2."""
        self.array = Array()
        self.link = LinkedList()
        self.urut_oid = None
        jumlah = 0
        awal = time.perf_counter()
        with open(path, "r", newline="", encoding="utf-8-sig") as f:
            baris = csv.reader(f)
            try:
                next(baris)  # buang baris header
            except StopIteration:
                raise OSError("CSV kosong: " + path)
            for kolom in baris:
                if len(kolom) < 9 or not kolom[0].strip():
                    continue
                pesanan = Pesanan(
                    kolom[0].strip(), kolom[1].strip(), kolom[2].strip(),
                    kolom[3].strip(), _bilangan(kolom[4], 0),
                    _bilangan(kolom[5], 3), _bilangan(kolom[6], 0),
                    _bilangan(kolom[7], None), kolom[8].strip() or "ANTRE")
                self.array.insert(self.array.size, pesanan)
                self.link.insert(self.link.size, pesanan)
                jumlah += 1
        ms = (time.perf_counter() - awal) * 1000.0
        self.jumlah_muat = jumlah
        self._isi_antrean_m2()
        return jumlah, ms

    def _isi_antrean_m2(self):
        self.naif = NaiveQueue()
        self.melingkar = CircularQueue()
        self.undo = Stack()
        self.redo = Stack()
        i = 0
        while i < self.array.size:
            pesanan = self.array.get(i)
            if pesanan.status == "ANTRE":
                self.naif.enqueue(pesanan)
                self.melingkar.enqueue(pesanan)
            i += 1

    def _oid_baru(self):
        self.nomor_baru += 1
        return "O-{0:06d}".format(self.jumlah_muat + self.nomor_baru)

    # -------------------------------------------------- pilih menu
    def pilih_menu(self, _=None):
        pilihan = self.pohon.selection()
        if not pilihan:
            return
        rek = _cari_menu(pilihan[0])
        if rek is None:
            return
        self.rek_terpilih = rek
        self.fokus = rek[3]
        self.label_info.configure(text=rek[1] + "\n" + rek[5])
        self._bangun_form(rek)

    def _bangun_form(self, rek):
        for anak in self.kotak_form.winfo_children():
            anak.destroy()
        self.entri = []
        mode = rek[4]
        baris = 0
        if mode == "no":
            self._tambah_entri(0, "no", "Nomor pesanan (1-based)", "100000")
            baris = 1
        elif mode in ("reguler", "prioritas", "vip"):
            self._tambah_entri(0, "pelanggan", "pelanggan", "Pelanggan Baru")
            self._tambah_entri(1, "resto", "resto", "warung-uji")
            self._tambah_entri(2, "menu", "menu", "nasi-goreng")
            self._tambah_entri(3, "harga", "harga", "22000")
            baris = 4
        elif mode == "ekspresi":
            self._tambah_entri(0, "ekspresi", "ekspresi infix",
                               "( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
            baris = 1
        elif mode == "order":
            self._tambah_entri(0, "pelanggan", "pelanggan", "Pelanggan Baru")
            baris = 1
        elif mode == "jumlah":
            self._tambah_entri(0, "jumlah", "jumlah pesanan", "1")
            baris = 1
        elif mode == "sort_kecil":
            self._tambah_entri(0, "kunci", "kunci (oid/harga/selesai)", "harga")
            self._tambah_entri(1, "jumlah", "jumlah baris (maks 5000)", "10")
            baris = 2
        elif mode == "sort_besar":
            self._tambah_entri(0, "kunci", "kunci (oid/harga/selesai)", "oid")
            self._tambah_entri(1, "jumlah", "jumlah baris (maks 200000)", "4000")
            baris = 2
        elif mode == "cari":
            self._tambah_entri(0, "target", "oid yang dicari", "O-137442")
            baris = 1
        ttk.Button(self.kotak_form, text="JALANKAN", command=self.jalankan).grid(
            row=baris, column=0, columnspan=2, sticky="w", pady=(8, 0))
        self.kotak_form.columnconfigure(1, weight=1)
        self.root.bind("<Return>", self._enter)

    def _tambah_entri(self, baris, nama, label, bawaan):
        ttk.Label(self.kotak_form, text=label).grid(row=baris, column=0,
                                                    sticky="w", padx=(0, 8), pady=2)
        w = ttk.Entry(self.kotak_form, width=40)
        w.insert(0, bawaan)
        w.grid(row=baris, column=1, sticky="ew", pady=2)
        self.entri.append((nama, w))

    def _enter(self, _):
        self.jalankan()

    def _nilai(self, nama):
        for n, w in self.entri:
            if n == nama:
                return w.get()
        return ""

    # -------------------------------------------------- jalankan
    def jalankan(self):
        if self.rek_terpilih is None:
            return
        kode, label, aksi, fokus, mode, _ = self.rek_terpilih
        try:
            self._lakukan(aksi, mode)
        except (ValueError, IndexError) as galat:
            messagebox.showerror("Gagal", str(galat))
            self._catat(label + ": " + str(galat), "galat")
        self._perbarui_status()

    def _lakukan(self, aksi, mode):
        if aksi == "muat":
            self.aksi_muat()
        elif aksi == "cek":
            self.aksi_cek()
        elif aksi == "stat":
            self.aksi_stat()
        elif aksi == "cuplik":
            self.aksi_cuplik()
        elif aksi == "postfix":
            self.aksi_postfix()
        elif aksi == "undo":
            self.aksi_undo()
        elif aksi == "redo":
            self.aksi_redo()
        elif aksi == "enqueue":
            self.aksi_enqueue()
        elif aksi == "dequeue_naif":
            self.aksi_dequeue("naif")
        elif aksi == "dequeue_circular":
            self.aksi_dequeue("melingkar")
        elif aksi == "stat2":
            self.aksi_stat2()
        elif aksi == "sort_insertion":
            self.aksi_insertion_sort()
        elif aksi == "sort_merge":
            self.aksi_merge_sort()
        elif aksi == "search_linear":
            self.aksi_linear_search()
        elif aksi == "search_binary":
            self.aksi_binary_search()
        elif aksi == "lihat":
            self.aksi_lihat()
        elif aksi == "hapus":
            self.aksi_hapus()
        else:
            self.aksi_tambah(mode)

    # -------------------------------------------------- aksi M1
    def _indeks(self, teks):
        if self.array.size == 0:
            raise ValueError("antrean masih kosong")
        try:
            n = int(str(teks).strip())
        except ValueError:
            raise ValueError("nomor pesanan bukan angka: " + str(teks))
        if n < 1 or n > self.array.size:
            raise ValueError("nomor {0} di luar jangkauan 1..{1}".format(n, self.array.size))
        return n - 1

    def aksi_lihat(self):
        i = self._indeks(self._nilai("no"))
        pa, pl, ms_a, ms_l, geser, telusur = self._adu(
            lambda: self.array.get(i), lambda: self.link.get(i))
        if pa is None or pl is None or pa.oid != pl.oid:
            raise ValueError("struktur tidak sinkron di indeks " + str(i))
        self._tulis_hasil(pa.detail(), "LIHAT no " + str(i + 1))
        self._adu_m1(self.fokus, ms_a, geser, ms_l, telusur)
        self._catat("LIHAT no {0} [{1}]".format(i + 1, pa.oid), "perintah")
        self._catat("  [M1 - array] {0} ms, geser {1}   |   "
                    "[M1 - linklist] {2} ms, telusur {3}".format(
                        angka(ms_a, 2), angka(geser), angka(ms_l, 2), angka(telusur)),
                    "modul")

    def aksi_tambah(self, jenis):
        if jenis == "vip":
            i = 0
            prioritas = 1
        elif jenis == "prioritas":
            i = self.array.size // 2
            prioritas = 2
        else:
            i = self.array.size
            prioritas = 3
        pesanan = Pesanan(self._oid_baru(), self._nilai("pelanggan"),
                          self._nilai("resto"), self._nilai("menu"),
                          _bilangan(self._nilai("harga"), 0), prioritas, 0, None, "ANTRE")
        pa, pl, ms_a, ms_l, geser, telusur = self._adu(
            lambda: self.array.insert(i, pesanan),
            lambda: self.link.insert(i, pesanan))
        self.urut_oid = None   # data berubah, daftar terurut oid tidak berlaku lagi
        label = "TAMBAH " + jenis.upper()
        self._tulis_hasil("{0} masuk di posisi ke-{1}".format(pesanan.oid, i + 1), label)
        self._adu_m1(self.fokus, ms_a, geser, ms_l, telusur)
        self._catat(label + " " + pesanan.oid, "perintah")
        self._catat("  posisi ke-{0} | [array] {1} ms, geser {2}   |   "
                    "[linklist] {3} ms, telusur {4}".format(
                        i + 1, angka(ms_a, 2), angka(geser), angka(ms_l, 2),
                        angka(telusur)), "modul")

    def aksi_hapus(self):
        i = self._indeks(self._nilai("no"))
        pa, pl, ms_a, ms_l, geser, telusur = self._adu(
            lambda: self.array.remove(i), lambda: self.link.remove(i))
        self.urut_oid = None   # data berubah, daftar terurut oid tidak berlaku lagi
        if pa is None or pl is None or pa.oid != pl.oid:
            raise ValueError("struktur tidak sinkron saat hapus indeks " + str(i))
        self._tulis_hasil(pa.oid + " dicabut dari antrean", "HAPUS no " + str(i + 1))
        self._adu_m1(self.fokus, ms_a, geser, ms_l, telusur)
        self._catat("HAPUS no {0} [{1}]".format(i + 1, pa.oid), "perintah")
        self._catat("  [M1 - array] {0} ms, geser {1}   |   "
                    "[M1 - linklist] {2} ms, telusur {3}".format(
                        angka(ms_a, 2), angka(geser), angka(ms_l, 2), angka(telusur)),
                    "modul")

    def _adu(self, kerja_array, kerja_link):
        """Kerjakan hal sama di Array dan LinkList, ukur waktu dan hitungannya."""
        geser0 = self.array.shifts
        telusur0 = self.link.traversals
        t0 = time.perf_counter()
        hasil_array = kerja_array()
        ms_array = (time.perf_counter() - t0) * 1000.0
        t0 = time.perf_counter()
        hasil_link = kerja_link()
        ms_link = (time.perf_counter() - t0) * 1000.0
        return (hasil_array, hasil_link, ms_array, ms_link,
                self.array.shifts - geser0, self.link.traversals - telusur0)

    def _adu_m1(self, fokus, ms_a, geser, ms_l, telusur):
        self.label_array.configure(text=("- " if fokus == "array" else "  ") +
                                   "Array      {0} ms  (geser {1} elemen)".format(
                                       angka(ms_a, 2), angka(geser)))
        self.label_link.configure(text=("- " if fokus == "link" else "  ") +
                                  "LinkList   {0} ms  (telusur {1} simpul)".format(
                                      angka(ms_l, 2), angka(telusur)))

    # -------------------------------------------------- aksi M2
    def aksi_postfix(self):
        token = tokenkan(self._nilai("ekspresi"))
        if not token:
            raise ValueError("ekspresi kosong")
        postfix = ke_postfix(token)
        total = hitung_postfix(postfix)
        teks = "postfix : {0}\nTOTAL   : {1}".format(" ".join(postfix), rupiah(total))
        self._tulis_hasil(teks, "STACK - POSTFIX (MESIN KASIR)")
        self.label_array.configure(text="  -")
        self.label_link.configure(text="  -")
        self._catat("POSTFIX {" + " ".join(postfix) + "}", "perintah")
        self._catat("  TOTAL " + rupiah(total) + " [M2 - stack]", "modul")

    def aksi_enqueue(self):
        pesanan = Pesanan(self._oid_baru(), self._nilai("pelanggan"),
                          "warung-uji", "menu-uji", 0, 3, 0, None, "ANTRE")
        g0 = self.naif.array.shifts
        t0 = time.perf_counter()
        self.naif.enqueue(pesanan)
        ms_naif = (time.perf_counter() - t0) * 1000.0
        t0 = time.perf_counter()
        self.melingkar.enqueue(pesanan)
        ms_circ = (time.perf_counter() - t0) * 1000.0
        geser = self.naif.array.shifts - g0
        self.undo.push(("ENQUEUE", [pesanan]))
        self.redo = Stack()
        self._tulis_hasil(pesanan.oid + " masuk paling belakang", "QUEUE - ENQUEUE")
        self._adu_m2("", ms_naif, geser, ms_circ, 0)
        self._catat("ENQUEUE " + pesanan.oid, "perintah")
        self._catat("  naif {0} ms, geser {1}   |   melingkar {2} ms".format(
            angka(ms_naif, 2), angka(geser), angka(ms_circ, 2)), "modul")

    def aksi_dequeue(self, versi):
        if self.naif.size() == 0:
            raise ValueError("antrean kosong")
        try:
            n = int(str(self._nilai("jumlah")).strip())
        except ValueError:
            raise ValueError("jumlah bukan angka: " + self._nilai("jumlah"))
        if n < 1:
            raise ValueError("jumlah minimal 1")
        if n > self.naif.size():
            raise ValueError("jumlah {0} melebihi panjang antrean {1}".format(
                n, self.naif.size()))
        keluar = []
        g0 = self.naif.array.shifts
        t0 = time.perf_counter()
        k = 0
        while k < n:
            keluar.append(self.naif.dequeue())
            k += 1
        ms_naif = (time.perf_counter() - t0) * 1000.0
        t0 = time.perf_counter()
        k = 0
        while k < n:
            self.melingkar.dequeue()
            k += 1
        ms_circ = (time.perf_counter() - t0) * 1000.0
        geser = self.naif.array.shifts - g0
        self.undo.push(("DEQUEUE", keluar))
        self.redo = Stack()
        contoh = keluar[0].oid
        if n > 1:
            contoh += " ... " + keluar[n - 1].oid
        self._tulis_hasil("{0} pesanan keluar: {1}".format(angka(n), contoh),
                          "QUEUE - DEQUEUE " + versi.upper())
        self._adu_m2(versi, ms_naif, geser, ms_circ, 0)
        self._catat("DEQUEUE {0} pesanan ({1})".format(angka(n), versi), "perintah")
        self._catat("  naif {0} ms, geser {1}   |   melingkar {2} ms, geser 0".format(
            angka(ms_naif, 2), angka(geser), angka(ms_circ, 2)), "modul")

    def aksi_undo(self):
        if self.undo.is_empty():
            raise ValueError("tumpukan undo kosong, tidak ada yang dibatalkan")
        jenis, daftar = self.undo.pop()
        if jenis == "ENQUEUE":
            self.naif.dequeue_back()
            self.melingkar.dequeue_back()
            pesan = daftar[0].oid + " dibatalkan dari belakang antrean"
        else:
            i = len(daftar) - 1
            while i >= 0:
                self.naif.enqueue_front(daftar[i])
                self.melingkar.enqueue_front(daftar[i])
                i -= 1
            pesan = "{0} pesanan dikembalikan ke DEPAN kedua antrean".format(
                angka(len(daftar)))
        self.redo.push((jenis, daftar))
        self._tulis_hasil(pesan, "STACK - UNDO LAST")
        self.label_array.configure(text="  Tumpukan undo  kedalaman " + str(self.undo.size()))
        self.label_link.configure(text="  Tumpukan redo  kedalaman " + str(self.redo.size()))
        self._catat("UNDO " + jenis, "perintah")
        self._catat("  " + pesan, "modul")

    def aksi_redo(self):
        if self.redo.is_empty():
            self._tulis_hasil("tumpukan redo kosong, tidak ada yang diulang",
                              "STACK - REDO LAST")
            self.label_array.configure(text="  Tumpukan undo  kedalaman " + str(self.undo.size()))
            self.label_link.configure(text="  Tumpukan redo  kedalaman " + str(self.redo.size()))
            self._catat("REDO: tumpukan redo kosong", "modul")
            return
        jenis, daftar = self.redo.pop()
        if jenis == "ENQUEUE":
            for pesanan in daftar:
                self.naif.enqueue(pesanan)
                self.melingkar.enqueue(pesanan)
            pesan = daftar[0].oid + " dimasukkan lagi ke belakang antrean"
        else:
            k = 0
            while k < len(daftar):
                self.naif.dequeue()
                self.melingkar.dequeue()
                k += 1
            pesan = "{0} pesanan keluar lagi dari depan kedua antrean".format(
                angka(len(daftar)))
        self.undo.push((jenis, daftar))
        self._tulis_hasil(pesan, "STACK - REDO LAST")
        self.label_array.configure(text="  Tumpukan undo  kedalaman " + str(self.undo.size()))
        self.label_link.configure(text="  Tumpukan redo  kedalaman " + str(self.redo.size()))
        self._catat("REDO " + jenis, "perintah")
        self._catat("  " + pesan, "modul")

    def _adu_m2(self, fokus, ms_n, geser, ms_c, geser_c):
        self.label_array.configure(text=("- " if fokus == "naif" else "  ") +
                                   "Antrean naif       {0} ms  (geser {1})".format(
                                       angka(ms_n, 2), angka(geser)))
        self.label_link.configure(text=("- " if fokus == "melingkar" else "  ") +
                                  "Antrean melingkar  {0} ms  (geser {1})".format(
                                      angka(ms_c, 2), angka(geser_c)))

    # -------------------------------------------------- aksi SISTEM
    def aksi_muat(self):
        jumlah, ms = self.muat_data(self.path)
        self._tulis_hasil("Data dibaca ulang: {0} pesanan dalam {1} ms\n"
                          "M2: {2} pesanan ANTRE masuk ke KEDUA antrean".format(
                              angka(jumlah), angka(ms, 2), angka(self.naif.size())))
        self._catat("MUAT ULANG {0} pesanan [{1} ms]".format(
            angka(jumlah), angka(ms, 2)), "modul")

    def aksi_cek(self):
        pesan = self._verifikasi()
        self._tulis_hasil(pesan)
        self._catat("CEK KONSISTENSI: " + pesan, "modul")

    def _verifikasi(self):
        if self.array.size != self.link.size:
            return "TIDAK COCOK: panjang berbeda {0} vs {1}".format(
                self.array.size, self.link.size)
        node = self.link.head
        i = 0
        while i < self.array.size:
            if self.array.get(i) is not node.data:
                return "TIDAK COCOK: indeks {0} berbeda".format(i)
            node = node.next
            i += 1
        return "cocok: identik pada {0} posisi".format(self.array.size)

    def aksi_stat(self):
        baris = [
            "  {0:<26} {1}".format("jumlah pesanan", angka(self.array.size)),
            "  {0:<26} {1}".format("array kapasitas", angka(self.array.capacity)),
            "  {0:<26} {1}".format("array geseran", angka(self.array.shifts)),
            "  {0:<26} {1}".format("array penyalinan", angka(self.array.copies)),
            "  {0:<26} {1}".format("linklist simpul", angka(self.link.size)),
            "  {0:<26} {1}".format("linklist telusuran", angka(self.link.traversals)),
        ]
        self._tulis_hasil("STATISTIK STRUKTUR\n" + "\n".join(baris))
        self._catat("STATISTIK STRUKTUR", "modul")

    def aksi_stat2(self):
        baris = [
            "  {0:<26} {1}".format("panjang antrean naif", angka(self.naif.size())),
            "  {0:<26} {1}".format("panjang antrean melingkar", angka(self.melingkar.size())),
            "  {0:<26} {1}".format("kapasitas naif", angka(self.naif.array.capacity)),
            "  {0:<26} {1}".format("kapasitas melingkar", angka(self.melingkar.capacity)),
            "  {0:<26} {1}".format("total geseran naif", angka(self.naif.array.shifts)),
            "  {0:<26} {1}".format("kedalaman undo", angka(self.undo.size())),
            "  {0:<26} {1}".format("kedalaman redo", angka(self.redo.size())),
        ]
        self._tulis_hasil("STATISTIK ANTREAN (M2)\n" + "\n".join(baris))
        self._catat("STATISTIK ANTREAN (M2)", "modul")

    def aksi_cuplik(self):
        baris = []
        i = 0
        while i < self.array.size and i < 200:
            baris.append("  {0:>7}. {1}".format(i + 1, self.array.get(i).ringkas()))
            i += 1
        self._tulis_hasil("200 PESANAN PERTAMA\n" + "\n".join(baris))
        self._catat("CUPLIKAN 200 PESANAN", "modul")

    # -------------------------------------------------- aksi M3
    def _data_laporan(self, jumlah=None):
        """Snapshot pesanan dari Array menjadi list primitif untuk diolah."""
        data = []
        batas = self.array.size
        if jumlah is not None and jumlah < batas:
            batas = jumlah
        i = 0
        while i < batas:
            data.append(self.array.get(i))
            i += 1
        return data

    def _kunci_dipilih(self):
        nama = self._nilai("kunci").strip().lower()
        if nama == "":
            nama = "harga"
        return nama, (lambda pesanan: ambil_kunci(pesanan, nama))

    def aksi_insertion_sort(self):
        nama, kunci = self._kunci_dipilih()
        jumlah = _bilangan(self._nilai("jumlah"), 10)
        if jumlah < 1:
            raise ValueError("jumlah minimal 1")
        if jumlah > BATAS_INSERTION:
            raise ValueError("insertion sort menolak {0} baris; maksimal {1} baris".format(
                angka(jumlah), angka(BATAS_INSERTION)))
        data = self._data_laporan(jumlah)
        t0 = time.perf_counter()
        banding, pindah = insertion_sort(data, kunci)
        ms = (time.perf_counter() - t0) * 1000.0
        self._tampil_sort("SORT - INSERTION SORT", data, nama, banding, pindah, ms)
        self.label_array.configure(text="  Insertion sort  {0} banding, {1} pindah, {2} ms".format(
            angka(banding), angka(pindah), angka(ms, 2)))
        self._catat("INSERTION SORT {0} baris kunci {1} [{2} ms]".format(
            angka(jumlah), nama, angka(ms, 2)), "perintah")
        self._catat("  {0} perbandingan, {1} pemindahan".format(
            angka(banding), angka(pindah)), "modul")

    def aksi_merge_sort(self):
        nama, kunci = self._kunci_dipilih()
        jumlah = _bilangan(self._nilai("jumlah"), 4000)
        if jumlah < 1:
            raise ValueError("jumlah minimal 1")
        if jumlah > self.array.size:
            jumlah = self.array.size
        data = self._data_laporan(jumlah)
        t0 = time.perf_counter()
        hasil, banding, pindah = merge_sort(data, kunci)
        ms = (time.perf_counter() - t0) * 1000.0
        self._tampil_sort("SORT - MERGE SORT", hasil, nama, banding, pindah, ms)
        self.label_link.configure(text="  Merge sort  {0} banding, {1} pindah, {2} ms".format(
            angka(banding), angka(pindah), angka(ms, 2)))
        self._catat("MERGE SORT {0} baris kunci {1} [{2} ms]".format(
            angka(jumlah), nama, angka(ms, 2)), "perintah")
        self._catat("  {0} perbandingan, {1} pemindahan".format(
            angka(banding), angka(pindah)), "modul")

    def _tampil_sort(self, judul, data, nama, banding, pindah, ms):
        baris = [
            "kunci         : " + nama,
            "jumlah baris  : " + angka(len(data)),
            "perbandingan  : " + angka(banding),
            "pemindahan    : " + angka(pindah),
            "lama          : " + angka(ms, 2) + " ms",
            "",
            "10 baris pertama (terurut):",
        ]
        i = 0
        while i < len(data) and i < 10:
            baris.append("  {0:>3}. {1}".format(i + 1, data[i].ringkas()))
            i += 1
        self._tulis_hasil("\n".join(baris), judul)

    def aksi_linear_search(self):
        target = self._nilai("target").strip()
        if not target:
            raise ValueError("target kosong")
        data = self._data_laporan()
        t0 = time.perf_counter()
        indeks, banding = linear_search(data, target, lambda pesanan: pesanan.oid)
        ms = (time.perf_counter() - t0) * 1000.0
        self._tampil_cari("SEARCH - LINEAR SEARCH", data, indeks, banding, ms)
        self.label_array.configure(text="  Linear search  {0} banding, {1} ms".format(
            angka(banding), angka(ms, 2)))
        self._catat("LINEAR SEARCH {0} [{1} ms]".format(target, angka(ms, 2)), "perintah")
        self._catat("  {0} perbandingan".format(angka(banding)), "modul")

    def aksi_binary_search(self):
        target = self._nilai("target").strip()
        if not target:
            raise ValueError("target kosong")
        if self.urut_oid is None:
            data = self._data_laporan()
            t0 = time.perf_counter()
            self.urut_oid, banding_sort, pindah_sort = merge_sort(
                data, lambda pesanan: pesanan.oid)
            ms_sort = (time.perf_counter() - t0) * 1000.0
            baris_urut = [
                "membangun daftar terurut oid (sekali saja):",
                "  {0} perbandingan, {1} pemindahan, {2} ms".format(
                    angka(banding_sort), angka(pindah_sort), angka(ms_sort, 2)),
            ]
        else:
            ms_sort = 0.0
            baris_urut = [
                "membangun daftar terurut oid:",
                "  dipakai ulang dari pencarian sebelumnya (0 ms)",
            ]
        t0 = time.perf_counter()
        indeks, banding = binary_search(
            self.urut_oid, target, lambda pesanan: pesanan.oid)
        ms_cari = (time.perf_counter() - t0) * 1000.0
        baris = baris_urut + [
            "",
            "pencarian biner:",
            "  {0} perbandingan, {1} ms".format(angka(banding), angka(ms_cari, 2)),
            "",
        ]
        if indeks < 0:
            baris.append("tidak ditemukan")
        else:
            baris.append("ditemukan di indeks {0} (baris ke-{1})".format(
                angka(indeks), angka(indeks + 1)))
            baris.append("  " + self.urut_oid[indeks].ringkas())
        self._tulis_hasil("\n".join(baris), "SEARCH - BINARY SEARCH")
        self.label_link.configure(text="  Binary search  {0} banding, {1} ms".format(
            angka(banding), angka(ms_cari, 2)))
        self._catat("BINARY SEARCH {0} [{1} ms]".format(target, angka(ms_cari, 2)), "perintah")
        self._catat("  urut {0} ms, cari {1} banding, {2} ms".format(
            angka(ms_sort, 2), angka(banding), angka(ms_cari, 2)), "modul")

    def _tampil_cari(self, judul, data, indeks, banding, ms):
        baris = [
            "perbandingan : " + angka(banding),
            "lama         : " + angka(ms, 2) + " ms",
            "",
        ]
        if indeks < 0:
            baris.append("tidak ditemukan")
        else:
            baris.append("ditemukan di indeks {0} (baris ke-{1})".format(
                angka(indeks), angka(indeks + 1)))
            baris.append("  " + data[indeks].ringkas())
        self._tulis_hasil("\n".join(baris), judul)

    # -------------------------------------------------- tampilan
    def _tulis_hasil(self, isi, judul=None):
        self.teks_hasil.configure(state="normal")
        self.teks_hasil.delete("1.0", "end")
        if judul is not None:
            self.teks_hasil.insert("end", judul + "\n", "kepala")
        self.teks_hasil.insert("end", isi + "\n")
        self.teks_hasil.configure(state="disabled")

    def _catat(self, teks, tag=None):
        self.teks_log.configure(state="normal")
        stempel = time.strftime("%H:%M:%S")
        self.teks_log.insert("end", stempel + "  " + teks + "\n", tag)
        self.teks_log.see("end")
        self.teks_log.configure(state="disabled")

    def _ganti_status(self, teks):
        self.label_status.configure(text=teks)

    def _perbarui_status(self):
        self._ganti_status(
            "M1: {0} pesanan (array kap {1}, linklist {2}) | M2: naif {3} = "
            "melingkar {4} (kap {5}) | undo {6} redo {7}".format(
                angka(self.array.size), angka(self.array.capacity),
                angka(self.link.size), angka(self.naif.size()),
                angka(self.melingkar.size()), angka(self.melingkar.capacity),
                angka(self.undo.size()), angka(self.redo.size())))


def _cari_menu(kode):
    for _, isi in MENU:
        for rek in isi:
            if rek[0] == kode:
                return rek
    return None


def buka(jendela, path):
    return Jendela(jendela, path)
