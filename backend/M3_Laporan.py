"""
backend/m3_laporan.py - Milestone 3: Sorting & Searching Algorithms
"""

def insertion_sort(larik_pesanan, kunci='harga'):
    n = larik_pesanan.size if hasattr(larik_pesanan, 'size') else len(larik_pesanan)
    perbandingan = 0
    pemindahan = 0

    arr = []
    for i in range(n):
        item = larik_pesanan.get(i) if hasattr(larik_pesanan, 'get') else larik_pesanan[i]
        arr.append(item)

    for i in range(1, n):
        key_item = arr[i]
        key_val = getattr(key_item, kunci, None)
        if key_val is None:
            key_val = key_item[kunci] if isinstance(key_item, dict) else key_item

        j = i - 1
        while j >= 0:
            curr_item = arr[j]
            curr_val = getattr(curr_item, kunci, None)
            if curr_val is None:
                curr_val = curr_item[kunci] if isinstance(curr_item, dict) else curr_item

            perbandingan += 1
            if curr_val > key_val:
                arr[j + 1] = arr[j]
                pemindahan += 1
                j -= 1
            else:
                break
        arr[j + 1] = key_item
        pemindahan += 1

    return arr, perbandingan, pemindahan


def merge_sort(larik_pesanan, kunci='harga'):
    n = larik_pesanan.size if hasattr(larik_pesanan, 'size') else len(larik_pesanan)
    arr = []
    for i in range(n):
        item = larik_pesanan.get(i) if hasattr(larik_pesanan, 'get') else larik_pesanan[i]
        arr.append(item)

    stats = {'perbandingan': 0, 'pemindahan': 0}

    def _get_val(obj):
        val = getattr(obj, kunci, None)
        if val is None and isinstance(obj, dict):
            val = obj.get(kunci)
        return val

    def _merge_sort_rec(sub_arr):
        if len(sub_arr) <= 1:
            return sub_arr
        mid = len(sub_arr) // 2
        left = _merge_sort_rec(sub_arr[:mid])
        right = _merge_sort_rec(sub_arr[mid:])
        return _merge(left, right)

    def _merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            stats['perbandingan'] += 1
            val_l = _get_val(left[i])
            val_r = _get_val(right[j])
            if val_l <= val_r:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
            stats['pemindahan'] += 1

        while i < len(left):
            result.append(left[i])
            i += 1
            stats['pemindahan'] += 1

        while j < len(right):
            result.append(right[j])
            j += 1
            stats['pemindahan'] += 1

        return result

    sorted_arr = _merge_sort_rec(arr)
    return sorted_arr, stats['perbandingan'], stats['pemindahan']


def linear_search(larik_pesanan, target_oid):
    n = larik_pesanan.size if hasattr(larik_pesanan, 'size') else len(larik_pesanan)
    perbandingan = 0

    for i in range(n):
        item = larik_pesanan.get(i) if hasattr(larik_pesanan, 'get') else larik_pesanan[i]
        oid_val = getattr(item, 'oid', None)
        if oid_val is None and isinstance(item, dict):
            oid_val = item.get('oid')

        perbandingan += 1
        if str(oid_val) == str(target_oid):
            return i, item, perbandingan

    return -1, None, perbandingan


def binary_search(sorted_larik, target_oid):
    n = len(sorted_larik)
    lo = 0
    hi = n - 1
    perbandingan = 0

    def _get_oid(obj):
        oid = getattr(obj, 'oid', None)
        if oid is None and isinstance(obj, dict):
            oid = oid.get('oid')
        return str(oid)

    while lo <= hi:
        perbandingan += 1
        mid = (lo + hi) // 2
        mid_oid = _get_oid(sorted_larik[mid])

        if mid_oid == str(target_oid):
            return mid, sorted_larik[mid], perbandingan
        elif mid_oid < str(target_oid):
            lo = mid + 1
        else:
            hi = mid - 1

    return -1, None, perbandingan
