# 2EZ4U APP - Engine Layanan Pesan-Antar Makanan (Mini Delivery Service)

> **Studi Kasus Proyek Akhir**  
> **Mata Kuliah:** Struktur Data & Analisa Algoritma (EC234303)  
> **Dosen Pengampu:** Ir. Arta Kusuma Hernanda, S.T., M.T.  
> **Program Sarjana Departemen Teknik Komputer - Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC) ITS**  

---
> **Author :: Faiz Rizqi Aqila Lubis**
> **NRP :: 5024251025**
## 1. Deskripsi Proyek

**2EZ4U APP** adalah simulasi engine backend berkinerja tinggi untuk layanan pesan-antar makanan dan barang (seperti GoFood, GrabFood, ShopeeFood versi mini). Aplikasi dirancang untuk menangani beban trafik tinggi dengan dataset sebesar **200.000+ baris data pesanan** (`pesanan.csv`) dan data graf peta navigasi (`peta.csv`).

Proyek ini dibangun dari nol (*from scratch*) dengan mematuhi **Aturan Integritas Akademik Ketat**:
- **Dilarang menggunakan fungsi/pustaka instan bawaan Python**: seperti `dict`, `set`, `sorted`, `.sort()`, `heapq`, `bisect`, `collections.*`, literal `{}` dan comprehension dict/set.
- **Hanya diperbolehkan**: `list` primitif sebagai alokasi memori array tetap (`[None] * capacity`), `tuple`, aritmetika dasar, string, dan I/O.
- Seluruh struktur data (Dynamic Array, Doubly Linked List, Circular Queue, Stack, Hash Map, Binary Search Tree, Binary Min-Heap, dan Graph Adjacency List) diimplementasikan secara mandiri.

---

## 2. Struktur Repositori

```text
2ez4u/
├── README.md                <- Dokumentasi Lengkap & Laporan Analisis Algoritma
├── app.py                   <- Titik Masuk Utama Aplikasi ("python app.py")
├── test_m1_m3.py            <- Script Pengujian Unit & Verifikasi Logika M1-M3
├── benchmark_dataset.py     <- Script Benchmark Skala Penuh (200.000 Pesanan)
│
├── data/                    <- Penyimpanan Dataset Sistem
│   ├── pesanan.csv          <- 200.000+ Baris Data Pesanan Pelanggan
│   └── peta.csv             <- Graf Konektivitas Lokasi & Estimasi Waktu (Menit)
│
├── backend/                 <- 6 Modul Fitur Struktur Data & Algoritma Murni
│   ├── m1_pesanan.py        <- M1: Dynamic Array vs Doubly Linked List
│   ├── m2_antrean.py        <- M2: Antrean Melingkar (Queue) + Tumpukan (Stack Kasir & Undo/Redo)
│   ├── m3_laporan.py        <- M3: Insertion Sort vs Merge Sort & Linear vs Binary Search
│   ├── m4_pencarian.py      <- M4: PetaHash (Hash Map Separate Chaining O(1))
│   ├── m5_katalog.py        <- M5: Katalog Menu (BST) & Min-Heap Prioritas Dispatch
│   └── m6_peta.py           <- M6: Graf Navigasi + BFS (Radius Hops) + Dijkstra (Rute Tercepat)
│
└── frontend/                <- Antarmuka Pengguna Grafis (GUI)
    └── ui.py                <- Jendela GUI Tkinter (Sidebar Menu, Form Dinamis, Command Log)
```

---

## 3. Peta Milestone & Analisis Kompleksitas

### Milestone 1 (M1): Dynamic Array vs Doubly Linked List
Menyimpan dan mengelola pesanan dengan 3 tingkatan prioritas:
1. **REGULER (3)**: Mengantre di urutan paling belakang.
2. **PRIORITAS (2)**: Menyerobot ke posisi tengah barisan ($\lfloor n/2 \rfloor$).
3. **VIP (1)**: Langsung masuk ke urutan paling depan (indeks 0).

| Operasi Bisnis | Dynamic Array | Doubly Linked List | Penjelasan Mekanisme Fisik |
|---|---|---|---|
| **Lihat Pesanan ke-$i$** | $O(1)$ | $O(n)$ | Array menghitung alamat memori langsung; Linked list menelusuri pointer simpul. |
| **Tambah REGULER** | Amortized $O(1)$ | $O(1)$ | Keduanya menempel di ujung belakang (`tail`). |
| **Tambah PRIORITAS** | $O(n)$ | $O(n)$ | Array menggeser $n/2$ elemen; Linked list menelusuri $n/2$ simpul lalu menyambung pointer. |
| **Tambah VIP** | $O(n)$ | $O(1)$ | Array menggeser seluruh $n$ elemen; Linked list hanya memindahkan pointer `head`. |
| **Hapus Pesanan ke-$i$** | $O(n)$ | $O(n)$ | Array menggeser elemen kanan; Linked list menelusuri simpul lalu melepas tautan pointer. |

---

### Milestone 2 (M2): Stack Mesin Kasir & Antrean Naif vs Circular

#### A. Mesin Kasir (Infix ke Postfix & Evaluasi)
- **Konversi Shunting-Yard**: Mengubah ekspresi matematika kasir `( 3 * 12000 ) + ( 2 * 8500 ) - 5000` menjadi format RPN (Reverse Polish Notation): `3 12000 * 2 8500 * + 5000 -`.
- **Evaluasi Postfix**: Menggunakan stack nilai. Untuk operator `-` dan `/`, operand kedua yang di-*pop* adalah sisi kiri ($a - b$, bukan $b - a$).

#### B. Antrean Naif vs Antrean Melingkar (Circular Queue)
- **Antrean Naif (Larik Biasa)**: Mengambil elemen depan (`dequeue`) membutuhkan penggeseran seluruh $n-1$ sisa elemen ke kiri $\rightarrow O(n)$.
- **Antrean Melingkar (Circular Queue)**: Array berkapasitas tetap dengan pointer `front`, `rear`, dan variabel `count`. Mengambil pesanan hanya memajukan pointer `front = (front + 1) % K` tanpa menggeser satu pun elemen $\rightarrow O(1)$ mutlak.

#### C. Mekanisme Undo & Redo
- Setiap aksi `ENQUEUE` atau `DEQUEUE` didorong ke `undo_stack`.
- **Undo DEQUEUE**: Mengembalikan elemen-elemen yang baru keluar ke **DEPAN** antrean (`push_front` / memundurkan pointer `front`).
- **Undo ENQUEUE**: Mengeluarkan pesanan dari **BELAKANG** antrean (`pop_back`).
- **Mengapa tumpukan Redo harus dikosongkan saat ada aksi baru?**  
  Karena jika pengguna melakukan aksi baru di tengah riwayat, garis waktu riwayat telah bercabang (*branching*). Menjalankan redo setelah aksi baru akan menempelkan keadaan masa lalu yang tidak valid ke kondisi data baru, merusak integritas sistem antrean.

---

### Milestone 3 (M3): Sort & Search

#### A. Insertion Sort vs Merge Sort
- **Kestabilan (Stability)**: Algoritma pengurutan disebut **stabil** jika elemen dengan nilai kunci yang sama tidak saling bertukar posisi aslinya.
  - `insertion_sort`: Stabil karena menggunakan perbandingan strictly greater (`>`), bukan `>=`.
  - `merge_sort`: Stabil karena saat menggabungkan dua bagian terurut, elemen dari sub-array kiri selalu didahulukan ketika kuncinya bernilai sama (`<=`).

#### Tabel Perbandingan Empiris Riil (Dataset pesanan.csv)

| Algoritma | Jumlah Data ($N$) | Kunci | Jumlah Perbandingan | Waktu Eksekusi | Kompleksitas Teoretis |
|---|---|---|---|---|---|
| **Insertion Sort** | 2.000 | `harga` | 963.016 | 299,99 ms | $O(n^2)$ |
| **Merge Sort** | 2.000 | `harga` | 19.331 | 12,35 ms | $O(n \log n)$ |
| **Insertion Sort** | 4.000 | `harga` | 3.833.706 (~4x lipat) | 1.315,77 ms | $O(n^2)$ kuadratik |
| **Merge Sort** | 4.000 | `harga` | 42.556 (~2x lipat) | 30,95 ms | $O(n \log n)$ linearitmik |
| **Insertion Sort** | 200.000 | `harga` | *Ditolak otomatis* | - | Mencegah aplikasi freeze |
| **Merge Sort** | 200.000 | `harga` | 3.226.139 | 2.027,53 ms | Mampu mengurutkan skala penuh |

#### B. Linear Search vs Binary Search
Mencari target pesanan `O-199999` pada 200.000 data:
- **Linear Search**: Memeriksa satu per satu dari awal $\rightarrow$ **200.000 perbandingan** (15,61 ms).
- **Binary Search**: Membagi ruang pencarian menjadi separuh tiap langkah $\rightarrow$ **hanya 16 perbandingan** (0,02 ms)!  
  *Catatan*: Binary search menuntut array terurut. Membangun indeks terurut dengan Merge Sort memakan waktu ~2.000 ms, sehingga Binary Search sangat efisien jika data dicari berulang kali (*multi-query*).

---



## 4. Cara Menjalankan Aplikasi

Pastikan Python 3.11+ terpasang pada komputer Anda.

### Menjalankan Aplikasi GUI Tkinter
```bash
python app.py
```
*(Atau menggunakan `uv`: `uv run --python 3.12 app.py`)*

### Menjalankan Uji Logika Backend M1 - M3
```bash
python test_m1_m3.py
```

### Menjalankan Benchmark Skala Penuh (200.000 Data)
```bash
python benchmark_dataset.py
```

---

## 5. Ringkasan Desain Antarmuka (GUI)

Antarmuka dibangun dengan modul standar `tkinter` dengan 3 panel utama:
1. **Sidebar Menu (Kiri)**: Navigasi modul M1 hingga M6 lengkap dengan operasi Array, Linked List, Stack Kasir, Queue, Sort, Search, Hash Map, Katalog BST, MinHeap, dan Peta Graf.
2. **Form Parameter & Layar Hasil (Kanan)**: Input dinamis yang menyesuaikan fitur yang dipilih, serta terminal hasil monospace dengan rincian langkah dan analisis kompleksitas.
3. **Panel COMMAND (Bawah)**: Tabel pencatat setiap aksi yang dijalankan pengguna, modul terkait, jumlah elemen digeser / perbandingan, dan durasi eksekusi riil dalam milidetik ($ms$).