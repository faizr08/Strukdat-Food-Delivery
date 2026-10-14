"""
backend/m3_laporan.py - Milestone 3: Insertion Sort vs Merge Sort & Linear vs Binary Search
Proyek "2EZ4U APP" - Struktur Data & Analisa Algoritma (EC234303)

Aturan: Dilarang menggunakan dict, set, sorted, .sort(), heapq, collections.*.
Hanya gunakan list primitif, tuple, int, float, str, I/O.
"""

import time

def ambil_nilai_kunci(pesanan, kunci):
    """Mengekstrak nilai kunci dari objek Pesanan."""
    kunci_lower = str(kunci).lower()
    if kunci_lower in ('harga', 'price'):
        return pesanan.harga
    elif kunci_lower in ('oid', 'id'):
        return pesanan.oid
    elif kunci_lower in ('selesai', 't_selesai', 't_selesai_detik'):
        # Nilai None diperlakukan sebagai tak hingga agar berada di akhir laporan
        return pesanan.t_selesai_detik if pesanan.t_selesai_detik is not None else float('inf')
    elif kunci_lower in ('masuk', 't_masuk', 't_masuk_detik'):
        return pesanan.t_masuk_detik
    elif kunci_lower in ('prioritas', 'priority'):
        return pesanan.prioritas
    elif kunci_lower in ('pelanggan', 'customer'):
        return pesanan.pelanggan
    elif kunci_lower in ('resto', 'restaurant'):
        return pesanan.resto
    return pesanan.oid


# ==========================================
# Bagian A: Algoritma Pengurutan (Sort)
# ==========================================

def insertion_sort(larik_asli, kunci='harga', max_limit=20000):
    """
    Insertion Sort in-place dan STABIL.
    Kompleksitas: O(n^2) rata-rata/terburuk, O(n) terbaik.
    Menghitung perbandingan (comparisons) dan pergeseran (shifts).
    Jika panjang data melebihi max_limit, fungsi menolak agar aplikasi tidak freeze.
    """
    n = len(larik_asli)
    if n > max_limit:
        return None, 0, 0, 0.0, f"DITOLAK: batasnya {max_limit:,} baris, pakai merge sort untuk data penuh"

    # Salin list agar tidak merusak data asli
    larik = [None] * n
    for i in range(n):
        larik[i] = larik_asli[i]

    comparisons = 0
    shifts = 0
    t0 = time.perf_counter()

    for i in range(1, n):
        kunci_elemen = larik[i]
        val_kunci = ambil_nilai_kunci(kunci_elemen, kunci)
        j = i - 1

        # STABIL: Menggunakan operator > (bukan >=)
        while j >= 0:
            comparisons += 1
            if ambil_nilai_kunci(larik[j], kunci) > val_kunci:
                larik[j + 1] = larik[j]
                shifts += 1
                j -= 1
            else:
                break

        larik[j + 1] = kunci_elemen
        shifts += 1

    t1 = time.perf_counter()
    durasi_ms = (t1 - t0) * 1000
    return larik, comparisons, shifts, durasi_ms, "Sukses"


def merge_sort(larik_asli, kunci='harga'):
    """
    Merge Sort divide-and-conquer dan STABIL.
    Kompleksitas: O(n log n) di semua kasus.
    Mampu mengurutkan seluruh dataset 200.000+ baris secara stabil.
    Menghitung jumlah perbandingan dan pemindahan elemen.
    """
    n = len(larik_asli)
    larik = [None] * n
    for i in range(n):
        larik[i] = larik_asli[i]

    temp = [None] * n
    counter = [0, 0]  # [comparisons, moves]

    t0 = time.perf_counter()

    def _merge_sort_recursive(arr, aux, low, high):
        if low >= high:
            return
        mid = (low + high) // 2
        _merge_sort_recursive(arr, aux, low, mid)
        _merge_sort_recursive(arr, aux, mid + 1, high)

        # Penggabungan (Merge)
        i = low
        j = mid + 1
        k = low

        while i <= mid and j <= high:
            counter[0] += 1  # comparisons
            # STABIL: Gunakan <= agar elemen dari sisi kiri selalu didahulukan bila kunci sama
            if ambil_nilai_kunci(arr[i], kunci) <= ambil_nilai_kunci(arr[j], kunci):
                aux[k] = arr[i]
                counter[1] += 1
                i += 1
            else:
                aux[k] = arr[j]
                counter[1] += 1
                j += 1
            k += 1

        # Salin sisa sisi kiri
        while i <= mid:
            aux[k] = arr[i]
            counter[1] += 1
            i += 1
            k += 1

        # Salin sisa sisi kanan
        while j <= high:
            aux[k] = arr[j]
            counter[1] += 1
            j += 1
            k += 1

        # Salin kembali ke larik asli
        for idx in range(low, high + 1):
            arr[idx] = aux[idx]
            counter[1] += 1

    _merge_sort_recursive(larik, temp, 0, n - 1)
    t1 = time.perf_counter()
    durasi_ms = (t1 - t0) * 1000

    return larik, counter[0], counter[1], durasi_ms, "Sukses"


# ==========================================
# Bagian B: Algoritma Pencarian (Search)
# ==========================================

def linear_search(larik, target_oid):
    """
    Linear Search menelusuri satu per satu dari awal.
    Kompleksitas: O(n). Tidak mensyaratkan data terurut.
    Mengembalikan: (index, pesanan_ditemukan, comparisons, durasi_ms)
    """
    target_clean = str(target_oid).strip()
    comparisons = 0
    t0 = time.perf_counter()

    found_idx = -1
    found_item = None

    for i in range(len(larik)):
        comparisons += 1
        if larik[i].oid == target_clean:
            found_idx = i
            found_item = larik[i]
            break

    t1 = time.perf_counter()
    durasi_ms = (t1 - t0) * 1000
    return found_idx, found_item, comparisons, durasi_ms


def binary_search(larik_terurut_oid, target_oid):
    """
    Binary Search pada data yang sudah terurut menurut OID.
    Kompleksitas: O(log n).
    Mengembalikan: (index, pesanan_ditemukan, comparisons, durasi_ms)
    """
    target_clean = str(target_oid).strip()
    comparisons = 0
    t0 = time.perf_counter()

    lo = 0
    hi = len(larik_terurut_oid) - 1
    found_idx = -1
    found_item = None

    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        curr_oid = larik_terurut_oid[mid].oid

        if curr_oid == target_clean:
            found_idx = mid
            found_item = larik_terurut_oid[mid]
            break
        elif curr_oid < target_clean:
            lo = mid + 1
        else:
            hi = mid - 1

    t1 = time.perf_counter()
    durasi_ms = (t1 - t0) * 1000
    return found_idx, found_item, comparisons, durasi_ms
