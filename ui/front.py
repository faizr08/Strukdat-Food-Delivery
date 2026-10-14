"""
frontend/ui.py - Antarmuka Grafis Desktop Tkinter
Proyek "2EZ4U APP" - Struktur Data & Analisa Algoritma (EC234303)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import os

from backend.M1_Pesanan import Pesanan, DynamicArray, LinkedList, muat_data_csv
from backend.M2_Antrean import (ke_postfix,  
    ke_postfix, hitung_postfix, AntreanNaif, AntreanMelingkar, UndoRedoManager )

from backend.M3_Laporan import (
    insertion_sort, merge_sort, linear_search, binary_search)

class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("2EZ4U APP - Delivery Service Engine (ITS)")
        self.root.geometry("1150x750")
        self.root.minsize(950, 650)

        # Warna & Tema
        self.bg_color = "#f4f5f7"
        self.sidebar_color = "#1e293b"
        self.sidebar_fg = "#f8fafc"
        self.accent_color = "#2563eb"
        self.accent_hover = "#1d4ed8"

        self.root.configure(bg=self.bg_color)

        # Inisialisasi Data Backend
        self.arr = DynamicArray()
        self.ll = LinkedList()
        self.q_naif = AntreanNaif(initial_capacity=32768)
        self.q_circ = AntreanMelingkar(capacity=32768)
        self.undo_manager = UndoRedoManager()
        self.peta_hash_oid = None
        self.sorted_by_oid = None
       

        self.selected_menu = "M1_ARR_VIEW"

        self._buat_layout_utama()
        self._muat_dataset_awal()

    def _muat_dataset_awal(self):
        """Pemuatan awal dataset pesanan.csv dan peta.csv secara efisien."""
        csv_pesanan = os.path.join("data", "pesanan.csv")
        csv_peta = os.path.join("data", "peta.csv")

        if os.path.exists(csv_pesanan):
            self._log_command("SYSTEM", "Memuat data pesanan.csv (skala 200.000)...")
            # Muat dataset
            self.arr, self.ll, durasi_baca = muat_data_csv(csv_pesanan, limit=200000)
            self._log_command("SYSTEM", f"Berhasil memuat {len(self.arr):,} pesanan", f"{durasi_baca*1000:.2f} ms")

            # Isi antrean ANTRE
            for i in range(len(self.arr)):
                p = self.arr.get(i)
                if p.status == "ANTRE":
                    self.q_naif.enqueue(p)
                    self.q_circ.enqueue(p)

                # Masukkan ke BST katalog menu
                if i < 10000:  # Sampel menu unik untuk katalog
                    self.katalog_bst.tambah(p.menu, p.harga)

                # Masukkan ke MinHeap prioritas (VIP:1, Prio:2, Reg:3)
                if p.status == "ANTRE" and self.min_heap.size() < 1000:
                    self.min_heap.push((p.prioritas, p.t_masuk_detik), p)

        if os.path.exists(csv_peta):
            t_peta = self.peta_graf.muat_csv(csv_peta)
            self._log_command("M6", f"Peta graf dimuat ({self.peta_graf.num_vertices} lokasi, {self.peta_graf.num_edges} jalan)", f"{t_peta:.2f} ms")

        self.status_var.set(f"Dataset Aktif: {len(self.arr):,} pesanan | Antrean ANTRE: {len(self.q_circ):,} pesanan")

    def _buat_layout_utama(self):
        # 1. SIDEBAR (Kiri)
        sidebar_frame = tk.Frame(self.root, bg=self.sidebar_color, width=280)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        sidebar_frame.pack_propagate(False)

        # Judul Sidebar
        lbl_title = tk.Label(sidebar_frame, text="2EZ4U ENGINE", font=("Segoe UI", 14, "bold"),
                             bg=self.sidebar_color, fg="#38bdf8", pady=12)
        lbl_title.pack(fill=tk.X)

        lbl_sub = tk.Label(sidebar_frame, text="Struktur Data & Algoritma", font=("Segoe UI", 8),
                           bg=self.sidebar_color, fg="#94a3b8")
        lbl_sub.pack(fill=tk.X)

        # Canvas dengan scrollbar untuk menu sidebar yang kaya fitur
        canvas = tk.Canvas(sidebar_frame, bg=self.sidebar_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(sidebar_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.sidebar_color)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=265)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._tambah_menu_kategori(scrollable_frame, "M1: ARRAY & LINKED LIST", [
            ("ARRAY - LIHAT PESANAN", "M1_ARR_VIEW"),
            ("ARRAY - TAMBAH REGULER", "M1_ARR_ADD_REG"),
            ("ARRAY - TAMBAH PRIORITAS", "M1_ARR_ADD_PRIO"),
            ("ARRAY - TAMBAH VIP", "M1_ARR_ADD_VIP"),
            ("ARRAY - HAPUS PESANAN", "M1_ARR_DEL"),
            ("LINKED LIST - LIHAT PESANAN", "M1_LL_VIEW"),
            ("LINKED LIST - TAMBAH REGULER", "M1_LL_ADD_REG"),
            ("LINKED LIST - TAMBAH PRIORITAS", "M1_LL_ADD_PRIO"),
            ("LINKED LIST - TAMBAH VIP", "M1_LL_ADD_VIP"),
            ("LINKED LIST - HAPUS PESANAN", "M1_LL_DEL"),
        ])

        self._tambah_menu_kategori(scrollable_frame, "M2: STACK & QUEUE", [
            ("STACK - POSTFIX (KASIR)", "M2_STACK_POSTFIX"),
            ("STACK - UNDO", "M2_STACK_UNDO"),
            ("STACK - REDO", "M2_STACK_REDO"),
            ("QUEUE - ENQUEUE", "M2_QUEUE_ENQ"),
            ("QUEUE - DEQUEUE NAIF", "M2_QUEUE_DEQ_NAIF"),
            ("QUEUE - DEQUEUE CIRCULAR", "M2_QUEUE_DEQ_CIRC"),
        ])

        self._tambah_menu_kategori(scrollable_frame, "M3: SORT & SEARCH", [
            ("SORT - INSERTION SORT", "M3_SORT_INS"),
            ("SORT - MERGE SORT", "M3_SORT_MRG"),
            ("SEARCH - LINEAR SEARCH", "M3_SEARCH_LIN"),
            ("SEARCH - BINARY SEARCH", "M3_SEARCH_BIN"),
        ])

        self._tambah_menu_kategori(scrollable_frame, "M4: PETA HASH", [
            ("HASH - CARI PESANAN O(1)", "M4_HASH_SEARCH"),
            ("HASH - STATISTIK TABEL", "M4_HASH_STATS"),
        ])

        self._tambah_menu_kategori(scrollable_frame, "M5: KATALOG & PRIORITAS", [
            ("KATALOG - RENTANG HARGA (BST)", "M5_BST_RENTANG"),
            ("KATALOG - TAMBAH MENU (BST)", "M5_BST_ADD"),
            ("HEAP - DISPATCH PRIORITAS", "M5_HEAP_DISPATCH"),
        ])

        self._tambah_menu_kategori(scrollable_frame, "M6: PETA & NAVIGASI", [
            ("PETA - ZONA JANGKAUAN (BFS)", "M6_BFS_ZONA"),
            ("PETA - RUTE TERCEPAT (DIJKSTRA)", "M6_DIJKSTRA"),
        ])

        # 2. PANEL UTAMA (Kanan & Bawah)
        main_content = tk.Frame(self.root, bg=self.bg_color)
        main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Panel Atas: Header Fitur Terpilih
        self.header_frame = tk.Frame(main_content, bg="#ffffff", height=50, relief=tk.SOLID, bd=1)
        self.header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        self.lbl_active_feature = tk.Label(self.header_frame, text="ARRAY - LIHAT PESANAN",
                                           font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#0f172a")
        self.lbl_active_feature.pack(side=tk.LEFT, padx=15, pady=8)

        # Panel Tengah: Form Parameter & Output Hasil
        split_frame = tk.Frame(main_content, bg=self.bg_color)
        split_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Sub-panel Kiri Tengah: Form Parameter
        self.form_card = tk.LabelFrame(split_frame, text=" Parameter Input ", font=("Segoe UI", 10, "bold"),
                                       bg="#ffffff", fg="#334155", padx=12, pady=10)
        self.form_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5), ipadx=10)

        self.form_inputs = {}
        self._bangun_form_dinamis()

        # Sub-panel Kanan Tengah: Output Hasil & Transkrip
        result_card = tk.LabelFrame(split_frame, text=" Hasil Eksekusi & Analisis Performa ",
                                    font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#334155", padx=10, pady=8)
        result_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.txt_output = scrolledtext.ScrolledText(result_card, wrap=tk.NONE, font=("Consolas", 9),
                                                    bg="#0f172a", fg="#f8fafc", insertbackground="white")
        self.txt_output.pack(fill=tk.BOTH, expand=True)

        # Panel Bawah: Command Log Table / Transcript
        cmd_card = tk.LabelFrame(main_content, text=" Panel COMMAND & Riwayat Riil ", font=("Segoe UI", 9, "bold"),
                                 bg="#ffffff", fg="#334155", height=160)
        cmd_card.pack(fill=tk.X, padx=10, pady=(5, 5))
        cmd_card.pack_propagate(False)

        cols = ("waktu", "modul", "perintah", "keterangan", "durasi")
        self.cmd_tree = ttk.Treeview(cmd_card, columns=cols, show="headings", height=5)
        self.cmd_tree.heading("waktu", text="Waktu")
        self.cmd_tree.heading("modul", text="Modul")
        self.cmd_tree.heading("perintah", text="Perintah")
        self.cmd_tree.heading("keterangan", text="Rincian / Pergeseran / Perbandingan")
        self.cmd_tree.heading("durasi", text="Waktu Eksekusi")

        self.cmd_tree.column("waktu", width=80, anchor="center")
        self.cmd_tree.column("modul", width=120, anchor="center")
        self.cmd_tree.column("perintah", width=240, anchor="w")
        self.cmd_tree.column("keterangan", width=420, anchor="w")
        self.cmd_tree.column("durasi", width=110, anchor="e")

        tree_scroll = ttk.Scrollbar(cmd_card, orient="vertical", command=self.cmd_tree.yview)
        self.cmd_tree.configure(yscrollcommand=tree_scroll.set)
        self.cmd_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

        # Status Bar
        self.status_var = tk.StringVar(value="Siap.")
        status_bar = tk.Label(main_content, textvariable=self.status_var, font=("Segoe UI", 8),
                              bg="#e2e8f0", fg="#475569", anchor="w", padx=10, pady=2)
        status_bar.pack(fill=tk.X)

    def _tambah_menu_kategori(self, parent, kategori_nama, items):
        lbl = tk.Label(parent, text=kategori_nama, font=("Segoe UI", 8, "bold"),
                       bg=self.sidebar_color, fg="#64748b", anchor="w", pady=4)
        lbl.pack(fill=tk.X, padx=5, pady=(8, 2))

        for text, key in items:
            btn = tk.Button(parent, text=f"  {text}", font=("Segoe UI", 8),
                            bg=self.sidebar_color, fg=self.sidebar_fg, anchor="w",
                            relief=tk.FLAT, activebackground="#334155", activeforeground="#ffffff",
                            command=lambda k=key, t=text: self._pilih_menu(k, t))
            btn.pack(fill=tk.X, pady=1)

    def _pilih_menu(self, menu_key, menu_title):
        self.selected_menu = menu_key
        self.lbl_active_feature.config(text=menu_title)
        self._bangun_form_dinamis()

    def _bangun_form_dinamis(self):
        # Bersihkan form lama
        for widget in self.form_card.winfo_children():
            widget.destroy()
        self.form_inputs.clear()

        key = self.selected_menu

        if "VIEW" in key or "DEL" in key:
            self._buat_input_field("Index Pesanan (ke-i):", "idx", "0")
        elif "ADD" in key and "BST" not in key:
            self._buat_input_field("ID Pesanan (OID):", "oid", "O-200001")
            self._buat_input_field("Nama Pelanggan:", "pelanggan", "Budi Santoso")
            self._buat_input_field("Restoran:", "resto", "kafe-teknik")
            self._buat_input_field("Menu:", "menu", "Nasi Goreng Spesial")
            self._buat_input_field("Harga (Rp):", "harga", "25000")
            if "REG" in key:
                prio_val = "3 (REGULER)"
            elif "PRIO" in key:
                prio_val = "2 (PRIORITAS)"
            else:
                prio_val = "1 (VIP)"
            self._buat_input_field("Prioritas:", "prioritas", prio_val, disabled=True)
        elif key == "M2_STACK_POSTFIX":
            self._buat_input_field("Struk Kasir (Infix):", "ekspresi", "( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
        elif "DEQ" in key:
            self._buat_input_field("Jumlah Pesanan Dilayani:", "n_deq", "1")
        elif key == "M2_QUEUE_ENQ":
            self._buat_input_field("Nama Pelanggan:", "pelanggan", "Pelanggan Baru")
            self._buat_input_field("Resto:", "resto", "kantin-pusat")
            self._buat_input_field("Menu:", "menu", "Es Jeruk Manis")
            self._buat_input_field("Harga (Rp):", "harga", "7000")
            self._buat_input_field("Prioritas (1-3):", "prioritas", "3")
        elif "SORT" in key:
            self._buat_input_field("Jumlah Baris (N):", "n_sort", "2000")
            self._buat_dropdown_field("Kunci Pengurutan:", "kunci_sort", ["harga", "oid", "selesai", "masuk"])
        elif "SEARCH" in key or key == "M4_HASH_SEARCH":
            self._buat_input_field("Target OID Pesanan:", "target_oid", "O-137442")
        elif key == "M5_BST_RENTANG":
            self._buat_input_field("Harga Minimal (Lo):", "lo", "10000")
            self._buat_input_field("Harga Maksimal (Hi):", "hi", "20000")
        elif key == "M5_BST_ADD":
            self._buat_input_field("Nama Menu:", "nama_menu", "Ayam Geprek Keju")
            self._buat_input_field("Harga (Rp):", "harga_menu", "18000")
        elif key == "M6_BFS_ZONA":
            self._buat_input_field("Lokasi Asal:", "asal_zona", "kantin-pusat")
            self._buat_input_field("Maksimal Hops (Langkah):", "hops", "2")
        elif key == "M6_DIJKSTRA":
            self._buat_input_field("Lokasi Asal (Resto):", "asal_rute", "kantin-pusat")
            self._buat_input_field("Lokasi Tujuan (Antar):", "tujuan_rute", "pos-satpam")

        # Tombol Eksekusi
        btn_run = tk.Button(self.form_card, text="JALANKAN PERINTAH", font=("Segoe UI", 9, "bold"),
                            bg=self.accent_color, fg="#ffffff", activebackground=self.accent_hover,
                            relief=tk.FLAT, pady=6, cursor="hand2", command=self._eksekusi_aksi)
        btn_run.pack(fill=tk.X, pady=(15, 5))

    def _buat_input_field(self, label_text, key, default_val="", disabled=False):
        lbl = tk.Label(self.form_card, text=label_text, font=("Segoe UI", 8, "bold"),
                       bg="#ffffff", fg="#475569", anchor="w")
        lbl.pack(fill=tk.X, pady=(4, 1))
        entry = tk.Entry(self.form_card, font=("Segoe UI", 9), relief=tk.SOLID, bd=1)
        entry.insert(0, default_val)
        if disabled:
            entry.config(state="disabled")
        entry.pack(fill=tk.X, pady=(0, 4))
        self.form_inputs[key] = entry

    def _buat_dropdown_field(self, label_text, key, options):
        lbl = tk.Label(self.form_card, text=label_text, font=("Segoe UI", 8, "bold"),
                       bg="#ffffff", fg="#475569", anchor="w")
        lbl.pack(fill=tk.X, pady=(4, 1))
        combo = ttk.Combobox(self.form_card, values=options, state="readonly", font=("Segoe UI", 9))
        combo.current(0)
        combo.pack(fill=tk.X, pady=(0, 4))
        self.form_inputs[key] = combo

    def _log_command(self, modul, perintah, keterangan="", durasi="0.00 ms"):
        waktu_str = time.strftime("%H:%M:%S")
        self.cmd_tree.insert("", 0, values=(waktu_str, modul, perintah, keterangan, durasi))

    def _cetak_ke_terminal(self, teks, clear=True):
        if clear:
            self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, teks + "\n")
        self.txt_output.see(tk.END)

    def _eksekusi_aksi(self):
        key = self.selected_menu
        t0 = time.perf_counter()

        # ==========================================
        # M1: Array vs Linked List
        # ==========================================
        if key == "M1_ARR_VIEW":
            idx = int(self.form_inputs["idx"].get())
            p = self.arr.get(idx)
            durasi = (time.perf_counter() - t0) * 1000
            if p:
                out = f"[M1 - Dynamic Array] Akses Indeks {idx:,} (O(1))\n"
                out += f"Detail Pesanan:\n"
                out += f" - OID        : {p.oid}\n - Pelanggan  : {p.pelanggan}\n - Restoran   : {p.resto}\n"
                out += f" - Menu       : {p.menu}\n - Harga      : Rp{p.harga:,}\n - Prioritas  : {p.prioritas_nama()}\n"
                out += f" - Status     : {p.status}\n\nWaktu Akses: {durasi:.3f} ms (Akses acak langsung O(1))"
            else:
                out = f"Indeks {idx} di luar rentang (Ukuran Array: {len(self.arr):,})."
            self._cetak_ke_terminal(out)
            self._log_command("M1 - Array", f"Lihat pesanan idx={idx}", f"Akses O(1)", f"{durasi:.3f} ms")

        elif key == "M1_LL_VIEW":
            idx = int(self.form_inputs["idx"].get())
            p = self.ll.get(idx)
            durasi = (time.perf_counter() - t0) * 1000
            if p:
                out = f"[M1 - Doubly LinkedList] Akses Indeks {idx:,} (O(n))\n"
                out += f"Detail Pesanan:\n"
                out += f" - OID        : {p.oid}\n - Pelanggan  : {p.pelanggan}\n - Restoran   : {p.resto}\n"
                out += f" - Menu       : {p.menu}\n - Harga      : Rp{p.harga:,}\n - Prioritas  : {p.prioritas_nama()}\n"
                out += f" - Status     : {p.status}\n\nWaktu Akses: {durasi:.3f} ms (Penelusuran sekuensial simpul O(n))"
            else:
                out = f"Indeks {idx} di luar rentang (Ukuran LinkedList: {len(self.ll):,})."
            self._cetak_ke_terminal(out)
            self._log_command("M1 - LinkedList", f"Lihat pesanan idx={idx}", f"Telusur simpul O(n)", f"{durasi:.3f} ms")

        elif key in ("M1_ARR_ADD_REG", "M1_ARR_ADD_PRIO", "M1_ARR_ADD_VIP"):
            prio = 3 if "REG" in key else (2 if "PRIO" in key else 1)
            p = Pesanan(self.form_inputs["oid"].get(), self.form_inputs["pelanggan"].get(),
                        self.form_inputs["resto"].get(), self.form_inputs["menu"].get(),
                        self.form_inputs["harga"].get(), prio, int(time.time()), status="ANTRE")
            sz_lama = len(self.arr)
            self.arr.insert_by_priority(p)
            durasi = (time.perf_counter() - t0) * 1000

            letak = "belakang (Amortized O(1))" if prio == 3 else ("tengah baris (O(n) geser elemen)" if prio == 2 else "urutan pertama (O(n) geser semua)")
            out = f"[M1 - Dynamic Array] Tambah Pesanan {p.prioritas_nama()}\n"
            out += f"Posisi Sisip : {letak}\nPanjang Array: {sz_lama:,} -> {len(self.arr):,}\nWaktu        : {durasi:.3f} ms\n\nDetail: {repr(p)}"
            self._cetak_ke_terminal(out)
            self._log_command("M1 - Array", f"Tambah {p.prioritas_nama()} ({p.oid})", letak, f"{durasi:.3f} ms")

        elif key in ("M1_LL_ADD_REG", "M1_LL_ADD_PRIO", "M1_LL_ADD_VIP"):
            prio = 3 if "REG" in key else (2 if "PRIO" in key else 1)
            p = Pesanan(self.form_inputs["oid"].get(), self.form_inputs["pelanggan"].get(),
                        self.form_inputs["resto"].get(), self.form_inputs["menu"].get(),
                        self.form_inputs["harga"].get(), prio, int(time.time()), status="ANTRE")
            sz_lama = len(self.ll)
            self.ll.insert_by_priority(p)
            durasi = (time.perf_counter() - t0) * 1000

            letak = "belakang Tail (O(1))" if prio == 3 else ("tengah (O(n) telusur, ganti pointer)" if prio == 2 else "paling depan Head (O(1))")
            out = f"[M1 - Doubly LinkedList] Tambah Pesanan {p.prioritas_nama()}\n"
            out += f"Posisi Sisip : {letak}\nPanjang List : {sz_lama:,} -> {len(self.ll):,}\nWaktu        : {durasi:.3f} ms\n\nDetail: {repr(p)}"
            self._cetak_ke_terminal(out)
            self._log_command("M1 - LinkedList", f"Tambah {p.prioritas_nama()} ({p.oid})", letak, f"{durasi:.3f} ms")

        elif key == "M1_ARR_DEL":
            idx = int(self.form_inputs["idx"].get())
            removed = self.arr.delete(idx)
            durasi = (time.perf_counter() - t0) * 1000
            if removed:
                out = f"[M1 - Dynamic Array] Hapus Pesanan Indeks {idx:,}\nPesanan Dihapus: {repr(removed)}\nPanjang Baru: {len(self.arr):,}\nWaktu: {durasi:.3f} ms (Menggeser seluruh elemen kanan)"
            else:
                out = f"Gagal menghapus: Indeks {idx} tidak valid."
            self._cetak_ke_terminal(out)
            self._log_command("M1 - Array", f"Hapus pesanan idx={idx}", f"O(n) geser", f"{durasi:.3f} ms")

        elif key == "M1_LL_DEL":
            idx = int(self.form_inputs["idx"].get())
            removed = self.ll.delete(idx)
            durasi = (time.perf_counter() - t0) * 1000
            if removed:
                out = f"[M1 - Doubly LinkedList] Hapus Pesanan Indeks {idx:,}\nPesanan Dihapus: {repr(removed)}\nPanjang Baru: {len(self.ll):,}\nWaktu: {durasi:.3f} ms (Menelusuri simpul & ubah pointer prev/next)"
            else:
                out = f"Gagal menghapus: Indeks {idx} tidak valid."
            self._cetak_ke_terminal(out)
            self._log_command("M1 - LinkedList", f"Hapus pesanan idx={idx}", f"O(n) telusur", f"{durasi:.3f} ms")

        # ==========================================
        # M2: Stack Kasir & Queue
        # ==========================================
        elif key == "M2_STACK_POSTFIX":
            expr = self.form_inputs["ekspresi"].get()
            tokens, post_str, langkah_konv = ke_postfix(expr)
            total, langkah_eval = hitung_postfix(tokens)
            durasi = (time.perf_counter() - t0) * 1000

            out = f"=======================================================================\n"
            out += f"  MESIN KASIR RESTORAN (INFIX -> POSTFIX -> EVALUASI NILAI)  \n"
            out += f"=======================================================================\n\n"
            out += f"Ekspresi Infix : {expr}\nPostfix        : {post_str}\nTOTAL          : Rp {int(total):,}\n\n"
            out += f"--- TAHAP 1: KONVERSI INFIX KE POSTFIX ---\n"
            out += f"{'Langkah':<8} {'Token':<8} {'Tindakan':<30} {'Isi Stack Operator':<22} {'Output'}\n"
            out += f"-" * 85 + "\n"
            step_no = 1
            for tok, act, st_snap, out_snap in langkah_konv:
                out += f"1.{step_no:<6} {tok:<8} {act:<30} {st_snap:<22} {out_snap}\n"
                step_no += 1

            out += f"\n--- TAHAP 2: EVALUASI POSTFIX DENGAN STACK NILAI ---\n"
            out += f"{'Langkah':<8} {'Token':<8} {'Tindakan Operasi':<42} {'Stack Nilai'}\n"
            out += f"-" * 75 + "\n"
            step_no = 1
            for tok, act, st_snap in langkah_eval:
                out += f"2.{step_no:<6} {tok:<8} {act:<42} {st_snap}\n"
                step_no += 1

            out += f"\nHASIL AKHIR: TOTAL = Rp {int(total):,}"
            self._cetak_ke_terminal(out)
            self._log_command("M2 - Stack", "Mesin Kasir Postfix", f"Total Rp{int(total):,}", f"{durasi:.3f} ms")

        elif key == "M2_QUEUE_ENQ":
            p = Pesanan(f"O-{len(self.arr)+1:06d}", self.form_inputs["pelanggan"].get(),
                        self.form_inputs["resto"].get(), self.form_inputs["menu"].get(),
                        self.form_inputs["harga"].get(), self.form_inputs["prioritas"].get(),
                        int(time.time()), status="ANTRE")
            self.q_naif.enqueue(p)
            self.q_circ.enqueue(p)
            self.arr.append(p)
            self.undo_manager.catat_aksi('ENQUEUE', p)
            durasi = (time.perf_counter() - t0) * 1000

            out = f"[M2 - Queue Enqueue] Satu pesanan baru masuk ke BELAKANG kedua antrean:\n"
            out += f"ID Pesanan    : {p.oid}\nPelanggan     : {p.pelanggan} ({p.resto} - {p.menu})\n"
            out += f"Panjang Antre : {len(self.q_circ):,} pesanan\n\n"
            out += f"Aksi dicatat ke Stack Undo (Tumpukan Undo: {self.undo_manager.stats()['undo_depth']}, Redo: 0)"
            self._cetak_ke_terminal(out)
            self._log_command("M2 - Queue", f"Enqueue {p.oid}", f"{len(self.q_circ):,} antre", f"{durasi:.3f} ms")

        elif key == "M2_QUEUE_DEQ_NAIF":
            n_deq = int(self.form_inputs["n_deq"].get())
            keluar_list = []
            geser_kumulatif = 0
            for _ in range(n_deq):
                p = self.q_naif.dequeue()
                if p:
                    keluar_list.append(p)
                    geser_kumulatif += self.q_naif.geseran_terakhir
            durasi = (time.perf_counter() - t0) * 1000

            out = f"[M2 - Antrean Naif] Melayani {len(keluar_list)} pesanan:\n"
            out += f"Jumlah Pesanan Keluar : {len(keluar_list)}\n"
            out += f"Total Elemen Digeser  : {geser_kumulatif:,} elemen (O(n) per pesanan)\n"
            out += f"Sisa Panjang Antrean  : {len(self.q_naif):,} pesanan\n"
            out += f"Waktu Eksekusi        : {durasi:.2f} ms\n\n"
            if keluar_list:
                out += f"Pesanan terlayani: {', '.join([p.oid for p in keluar_list[:5]])}{'...' if len(keluar_list) > 5 else ''}"
            self._cetak_ke_terminal(out)
            self._log_command("M2 - Queue Naif", f"Dequeue {len(keluar_list)} pesanan", f"{geser_kumulatif:,} elemen digeser", f"{durasi:.2f} ms")

        elif key == "M2_QUEUE_DEQ_CIRC":
            n_deq = int(self.form_inputs["n_deq"].get())
            keluar_list = []
            for _ in range(n_deq):
                p = self.q_circ.dequeue()
                if p:
                    keluar_list.append(p)
            durasi = (time.perf_counter() - t0) * 1000

            if keluar_list:
                self.undo_manager.catat_aksi('DEQUEUE', keluar_list)

            out = f"[M2 - Antrean Melingkar (Circular)] Melayani {len(keluar_list)} pesanan:\n"
            out += f"Jumlah Pesanan Keluar : {len(keluar_list)}\n"
            out += f"Total Elemen Digeser  : 0 elemen digeser (O(1) mutlak! Hanya front maju)\n"
            out += f"Pointer Posisi        : front={self.q_circ.front}, rear={self.q_circ.rear}, cap={self.q_circ.capacity}\n"
            out += f"Sisa Panjang Antrean  : {len(self.q_circ):,} pesanan\n"
            out += f"Waktu Eksekusi        : {durasi:.3f} ms\n\n"
            if keluar_list:
                out += f"Pesanan terlayani: {', '.join([p.oid for p in keluar_list[:5]])}{'...' if len(keluar_list) > 5 else ''}\n\n"
                out += f"Aksi dicatat ke Stack Undo (Tumpukan Undo: {self.undo_manager.stats()['undo_depth']})"
            self._cetak_ke_terminal(out)
            self._log_command("M2 - Queue Circular", f"Dequeue {len(keluar_list)} pesanan", "0 elemen digeser", f"{durasi:.3f} ms")

        elif key == "M2_STACK_UNDO":
            aksi, pesan = self.undo_manager.undo(self.q_naif, self.q_circ)
            durasi = (time.perf_counter() - t0) * 1000
            st = self.undo_manager.stats()
            out = f"[M2 - Stack UNDO]\n{pesan}\n\nPanjang Antrean Saat Ini: {len(self.q_circ):,}\nTumpukan: Undo={st['undo_depth']}, Redo={st['redo_depth']}"
            self._cetak_ke_terminal(out)
            self._log_command("M2 - Stack Undo", pesan, f"Undo={st['undo_depth']}, Redo={st['redo_depth']}", f"{durasi:.3f} ms")

        elif key == "M2_STACK_REDO":
            aksi, pesan = self.undo_manager.redo(self.q_naif, self.q_circ)
            durasi = (time.perf_counter() - t0) * 1000
            st = self.undo_manager.stats()
            out = f"[M2 - Stack REDO]\n{pesan}\n\nPanjang Antrean Saat Ini: {len(self.q_circ):,}\nTumpukan: Undo={st['undo_depth']}, Redo={st['redo_depth']}"
            self._cetak_ke_terminal(out)
            self._log_command("M2 - Stack Redo", pesan, f"Undo={st['undo_depth']}, Redo={st['redo_depth']}", f"{durasi:.3f} ms")

        # ==========================================
        # M3: Sort & Search
        # ==========================================
        elif key == "M3_SORT_INS":
            n = int(self.form_inputs["n_sort"].get())
            kunci = self.form_inputs["kunci_sort"].get()
            sub_arr = [self.arr.get(i) for i in range(min(n, len(self.arr)))]
            sorted_arr, comp, shifts, durasi, status = insertion_sort(sub_arr, kunci=kunci, max_limit=20000)

            if status != "Sukses":
                out = f"[M3 - Insertion Sort]\n{status}"
                self._cetak_ke_terminal(out)
                self._log_command("M3 - Insertion Sort", f"N={n:,} kunci={kunci}", status, f"{durasi:.2f} ms")
                return

            out = f"[M3 - Insertion Sort]\n"
            out += f"Data              : {len(sub_arr):,} pesanan | Kunci: {kunci}\n"
            out += f"Perbandingan (C)  : {comp:,}\nPergeseran (S)    : {shifts:,}\n"
            out += f"Waktu Eksekusi    : {durasi:.2f} ms\n\n"
            out += f"Sampel 10 Teratas Hasil Pengurutan (Stabil):\n"
            for i in range(min(10, len(sorted_arr))):
                out += f" {i+1}. {repr(sorted_arr[i])}\n"
            self._cetak_ke_terminal(out)
            self._log_command("M3 - Insertion Sort", f"N={len(sub_arr):,} kunci={kunci}", f"{comp:,} perbandingan", f"{durasi:.2f} ms")

        elif key == "M3_SORT_MRG":
            n = int(self.form_inputs["n_sort"].get())
            kunci = self.form_inputs["kunci_sort"].get()
            sub_arr = [self.arr.get(i) for i in range(min(n, len(self.arr)))]
            sorted_arr, comp, moves, durasi, status = merge_sort(sub_arr, kunci=kunci)

            out = f"[M3 - Merge Sort]\n"
            out += f"Data              : {len(sub_arr):,} pesanan | Kunci: {kunci}\n"
            out += f"Perbandingan (C)  : {comp:,}\nPemindahan (M)    : {moves:,}\n"
            out += f"Waktu Eksekusi    : {durasi:.2f} ms (O(n log n) divide and conquer)\n\n"
            out += f"Sampel 10 Teratas Hasil Pengurutan (Stabil):\n"
            for i in range(min(10, len(sorted_arr))):
                out += f" {i+1}. {repr(sorted_arr[i])}\n"
            self._cetak_ke_terminal(out)
            self._log_command("M3 - Merge Sort", f"N={len(sub_arr):,} kunci={kunci}", f"{comp:,} perbandingan", f"{durasi:.2f} ms")

        elif key == "M3_SEARCH_LIN":
            target = self.form_inputs["target_oid"].get()
            raw_list = self.arr.to_primitive_list()
            idx, p, comp, durasi = linear_search(raw_list, target)

            if p:
                out = f"[M3 - Linear Search] Target: {target}\n"
                out += f"Status        : DITEMUKAN pada indeks {idx:,}\n"
                out += f"Perbandingan  : {comp:,} perbandingan (O(n))\n"
                out += f"Waktu         : {durasi:.2f} ms\n\nDetail: {repr(p)}"
            else:
                out = f"[M3 - Linear Search] Target {target} TIDAK DITEMUKAN setelah {comp:,} perbandingan."
            self._cetak_ke_terminal(out)
            self._log_command("M3 - Linear Search", f"Target={target}", f"{comp:,} perbandingan", f"{durasi:.2f} ms")

        elif key == "M3_SEARCH_BIN":
            target = self.form_inputs["target_oid"].get()
            # Bangun list terurut OID jika belum ada
            if self.sorted_by_oid is None:
                t_b0 = time.perf_counter()
                self.sorted_by_oid, _, _, _, _ = merge_sort(self.arr.to_primitive_list(), kunci='oid')
                t_b_ms = (time.perf_counter() - t_b0) * 1000
                build_info = f"Daftar terurut OID dibangun sekali (merge sort): {t_b_ms:.2f} ms\n"
            else:
                build_info = "Daftar terurut OID siap dari cache memori.\n"

            idx, p, comp, durasi = binary_search(self.sorted_by_oid, target)

            if p:
                out = f"[M3 - Binary Search] Target: {target}\n"
                out += build_info
                out += f"Status        : DITEMUKAN pada baris {idx:,}\n"
                out += f"Perbandingan  : {comp} perbandingan (O(log n))\n"
                out += f"Waktu         : {durasi:.3f} ms\n\nDetail: {repr(p)}"
            else:
                out = f"[M3 - Binary Search] Target {target} TIDAK DITEMUKAN setelah {comp} perbandingan."
            self._cetak_ke_terminal(out)
            self._log_command("M3 - Binary Search", f"Target={target}", f"{comp} perbandingan", f"{durasi:.3f} ms")

        