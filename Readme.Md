# 2EZ4U APP - Engine Backend Delivery Service

> **Studi Kasus Proyek Akhir**  
> **Mata Kuliah:** Struktur Data & Analisa Algoritma (EC234303)  
> **Dosen Pengampu:** Ir. Arta Kusuma Hernanda, S.T., M.T.  
> **Program Sarjana Departemen Teknik Komputer - FTEIC ITS**  

---

##  Deskripsi Proyek
**2EZ4U APP** adalah engine backend mini untuk layanan pesan-antar makanan/barang (sejenis GoFood/GrabFood/ShopeeFood) yang dirancang khusus untuk menangani trafik tinggi dengan dataset sebesar **200.000+ data pesanan**. 

Proyek ini dibuat untuk mensimulasikan dan membandingkan secara langsung efisiensi performa kompleksitas waktu ($O(1)$, $O(n)$, $O(n^2)$, $O(n \log n)$, $O(\log n)$) dari berbagai struktur data dan algoritma buatan sendiri (*custom implementation*) tanpa menggunakan pustaka/fungsi instan bawaan Python (seperti `dict`, `set`, `.sort()`, `heapq`, `collections`, dll).

Deskripsi Modul
## Modul 1: Array & Linked List
Penyimpanan dan pengelolaan data pesanan dasar menggunakan dua struktur data yang diadu langsung kinerjanya, yaitu Array (dengan alokasi memori dinamis dan amortized $O(1)$) serta Linked List (menggunakan penunjuk head dan tail). Aturan bisnis pada modul ini mengakomodasi tiga jenis pesanan dengan titik penyisipan yang berbeda, yakni pesanan Reguler yang masuk di barisan paling belakang, pesanan Prioritas yang menyerobot ke tengah barisan, serta pesanan VIP yang langsung menempati urutan pertama. Di samping itu, modul ini juga menyediakan fungsi mendasar untuk melihat detail satu pesanan serta menghapus pesanan dari antrean.

## Modul 2: Stack & Queue
Mengimplementasikan struktur data Stack (tumpukan) dan Queue (antrean) guna menangani operasional kasir dan dapur secara efisien. Stack digunakan pada mesin kasir untuk mengonversi ekspresi infix menjadi postfix sekaligus mengevaluasi total harga belanjaan, serta mendukung fitur Undo/Redo untuk membatalkan atau mengerjakan ulang aksi terakhir. Selain itu, modul ini membandingkan dua versi antrean (Queue), yaitu Queue Naif yang memerlukan pergeseran elemen secara manual saat dequeue ($O(n)$) dan Queue Melingkar / Circular Queue yang memanfaatkan penunjuk front, rear, serta operasi modulo agar proses pengambilan data menjadi sangat cepat ($O(1)$) tanpa ada elemen yang digeser.

## Modul 3: Sorting & Searching
Menangani pembuatan laporan harian dan pencarian data spesifik dengan menerapkan berbagai algoritma pengurutan dan pencarian lengkap bersama pencatat jumlah perbandingannya. Untuk pengurutan (Sorting), modul ini menyediakan Insertion Sort ($O(n^2)$) yang stabil dan cocok untuk data kecil atau hampir terurut, serta Merge Sort ($O(n \log n)$) yang handal dan stabil dalam mengurutkan data skala besar (seperti 200.000 baris pesanan). Sementara itu, untuk pencarian (Searching), modul ini mengimplementasikan Linear Search ($O(n)$) yang menelusuri data satu per satu tanpa syarat terurut, serta Binary Search ($O(\log n)$) yang membuang separuh sisa data di setiap langkah untuk memberikan hasil pencarian kilat pada data yang sudah terurut menurut kunci tertentu.
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