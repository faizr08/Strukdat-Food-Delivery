"""M3 - Algoritma pengurutan dan pencarian.

Hanya berisi fungsinya saja, semuanya bekerja di atas list primitif. Yang
memanggil dan menampilkan hasilnya adalah frontend/ui.py. Setiap fungsi
mengembalikan jumlah perbandingan (dan jumlah pemindahan untuk pengurutan),
karena angka itulah yang membuktikan bedanya O(n^2) dan O(n log n).
"""


def insertion_sort(data, kunci):
    """Urutkan data di tempat menurut kunci. Stabil. -> (banding, pindah)."""
    banding = 0
    pindah = 0
    i = 1
    while i < len(data):
        nilai = data[i]
        kunci_nilai = kunci(nilai)
        j = i - 1
        while j >= 0:
            banding += 1
            if kunci(data[j]) > kunci_nilai:   # > , bukan >= , supaya stabil
                data[j + 1] = data[j]
                pindah += 1
                j -= 1
            else:
                break
        data[j + 1] = nilai
        i += 1
    return banding, pindah


def merge_sort(data, kunci):
    """Urutkan data (list) menurut kunci. Stabil. -> (hasil, banding, pindah)."""
    banding = 0
    pindah = 0

    def gabung(kiri, kanan):
        nonlocal banding, pindah
        hasil = []
        i = 0
        j = 0
        while i < len(kiri) and j < len(kanan):
            banding += 1
            if kunci(kiri[i]) <= kunci(kanan[j]):   # <= , supaya stabil
                hasil.append(kiri[i])
                i += 1
            else:
                hasil.append(kanan[j])
                j += 1
            pindah += 1
        while i < len(kiri):          # sisa kiri ikut disalin
            hasil.append(kiri[i])
            i += 1
            pindah += 1
        while j < len(kanan):         # sisa kanan ikut disalin
            hasil.append(kanan[j])
            j += 1
            pindah += 1
        return hasil

    def urut(bagian):
        if len(bagian) <= 1:
            return bagian
        tengah = len(bagian) // 2
        kiri = urut(bagian[:tengah])
        kanan = urut(bagian[tengah:])
        return gabung(kiri, kanan)

    hasil = urut(data)
    return hasil, banding, pindah


def linear_search(data, target, kunci):
    """Telusuri satu per satu, tidak menuntut data terurut. -> (indeks, banding)."""
    banding = 0
    i = 0
    while i < len(data):
        banding += 1
        if kunci(data[i]) == target:
            return i, banding
        i += 1
    return -1, banding


def binary_search(data, target, kunci):
    """Cari pada data terurut; tiap langkah membuang separuh. -> (indeks, banding)."""
    banding = 0
    lo = 0
    hi = len(data) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        banding += 1
        nilai = kunci(data[mid])
        if nilai == target:
            return mid, banding
        if nilai < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, banding
