# 2EZ4U APP - Engine Backend Delivery Service

> **Studi Kasus Proyek Akhir**  
> **Mata Kuliah:** Struktur Data & Analisa Algoritma (EC234303)  
> **Dosen Pengampu:** Ir. Arta Kusuma Hernanda, S.T., M.T.  
> **Program Sarjana Departemen Teknik Komputer - FTEIC ITS**  

---

##  Deskripsi Proyek
**2EZ4U APP** adalah engine backend mini untuk layanan pesan-antar makanan/barang (sejenis GoFood/GrabFood/ShopeeFood) yang dirancang khusus untuk menangani trafik tinggi dengan dataset sebesar **200.000+ data pesanan**. 

Proyek ini dibuat untuk mensimulasikan dan membandingkan secara langsung efisiensi performa kompleksitas waktu ($O(1)$, $O(n)$, $O(n^2)$, $O(n \log n)$, $O(\log n)$) dari berbagai struktur data dan algoritma buatan sendiri (*custom implementation*) tanpa menggunakan pustaka/fungsi instan bawaan Python (seperti `dict`, `set`, `.sort()`, `heapq`, `collections`, dll).

---

##  Struktur Repositori Proyek

```text
2ez4u/
│
├── README.md                <- Laporan & Dokumentasi Progres Utama Proyek
├── app.py                   <- Main Entry Point Aplikasi ("python app.py")
│
├── data/                    <- Dataset Sistem
│   ├── pesanan.csv          <- 200.000+ Data Pesanan
│   └── peta.csv             <- Data Graf Lokasi Peta & Navigasi
│
├── backend/                 <- Enam Modul Fitur Inti (DSA Custom)
│   ├── m1_pesanan.py        <- M1: Dynamic Array vs Doubly Linked List
│   ├── m2_antrean.py        <- M2: Antrean Melingkar (Queue) + Tumpukan (Stack Undo/Redo)
│   ├── m3_laporan.py        <- M3: Insertion Sort vs Merge Sort & Search
│   ├── m4_pencarian.py      <- M4: Peta Hash (Hash Map) + Merge Sort
│   ├── m5_katalog.py        <- M5: Katalog Binary Search Tree (BST) + MinHeap Prioritas
│   └── m6_peta.py           <- M6: Graf Peta Navigasi + BFS + Dijkstra
│
└── frontend/                <- Antarmuka Pengguna (GUI)
    └── ui.py                <- Jendela Tkinter untuk Visualisasi Backend