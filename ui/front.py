"""
ui/front.py - Antarmuka Pengguna Tkinter "2EZ4U APP" (Integrasi M1, M2, M3)
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from backend.M1_Pesanan import muat_data_pesanan
from backend.M2_Antrean import StackCart, PostfixEvaluator, NaiveQueue, CircularQueue
from backend.M3_Laporan import insertion_sort, merge_sort, linear_search, binary_search


class App2EZ4U:
    def __init__(self, root):
        self.root = root
        self.root.title("2EZ4U APP - Food Delivery & Data Engine")
        self.root.geometry("1050x700")

        self.dataset_pesanan = muat_data_pesanan(os.path.join(root_dir, "Data", "pesanan.csv"))
        self.cached_sorted_data = None

        self.setup_styles()
        self.create_layout()
        self.refresh_data_view()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=[12, 8])

    def create_layout(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_dataset = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_dataset, text="📁 M1 & M3 (Data, Sort & Search)")
        self.init_tab_dataset(self.tab_dataset)

        self.tab_m2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_m2, text="⚙️ M2 (Cart, Queue & RPN)")
        self.init_tab_m2(self.tab_m2)

    def init_tab_dataset(self, parent):
        control_frame = ttk.LabelFrame(parent, text=" Algoritma Sorting & Searching (M3) ", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Kunci:").grid(row=0, column=0, sticky="w", padx=5)
        self.sort_key_combo = ttk.Combobox(control_frame, values=["harga", "t_selesai_detik", "oid"], width=15, state="readonly")
        self.sort_key_combo.current(0)
        self.sort_key_combo.grid(row=0, column=1, padx=5)

        ttk.Button(control_frame, text="Insertion Sort O(n²)", command=self.run_insertion_sort).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Merge Sort O(n log n)", command=self.run_merge_sort).grid(row=0, column=3, padx=5)

        ttk.Separator(control_frame, orient=tk.VERTICAL).grid(row=0, column=4, sticky="ns", padx=10)

        ttk.Label(control_frame, text="Cari OID:").grid(row=0, column=5, sticky="w", padx=5)
        self.search_entry = ttk.Entry(control_frame, width=15)
        self.search_entry.grid(row=0, column=6, padx=5)

        ttk.Button(control_frame, text="Linear Search", command=self.run_linear_search).grid(row=0, column=7, padx=5)
        ttk.Button(control_frame, text="Binary Search", command=self.run_binary_search).grid(row=0, column=8, padx=5)

        table_frame = ttk.Frame(parent, padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("No", "OID", "Pelanggan", "Menu", "Harga", "Waktu (detik)")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="center")
        self.tree.column("Pelanggan", width=180, anchor="w")
        self.tree.column("Menu", width=220, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def init_tab_m2(self, parent):
        m2_frame = ttk.LabelFrame(parent, text=" Simulasi Struktur Data M2 ", padding=15)
        m2_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        ttk.Label(m2_frame, text="Evaluator Ekspresi RPN (Postfix):", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.rpn_entry = ttk.Entry(m2_frame, width=40)
        self.rpn_entry.insert(0, "50 20 + 3 *")
        self.rpn_entry.grid(row=1, column=0, padx=5, sticky="w")
        
        ttk.Button(m2_frame, text="Hitung RPN", command=self.evaluate_rpn).grid(row=1, column=1, padx=5, sticky="w")

        self.rpn_result_label = ttk.Label(m2_frame, text="Hasil: -", font=("Arial", 10))
        self.rpn_result_label.grid(row=2, column=0, sticky="w", pady=10)

    def refresh_data_view(self, data_source=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        source = data_source if data_source is not None else self.dataset_pesanan
        n = source.size if hasattr(source, 'size') else len(source)

        for i in range(min(n, 500)):
            item = source.get(i) if hasattr(source, 'get') else source[i]
            self.tree.insert("", tk.END, values=(
                i + 1,
                getattr(item, 'oid', ''),
                getattr(item, 'nama_pelanggan', ''),
                getattr(item, 'menu', ''),
                f"Rp {getattr(item, 'harga', 0):,.0f}",
                getattr(item, 't_selesai_detik', 0)
            ))

    def run_insertion_sort(self):
        kunci = self.sort_key_combo.get()
        sorted_arr, comp, mov = insertion_sort(self.dataset_pesanan, kunci=kunci)
        self.cached_sorted_data = sorted_arr
        self.refresh_data_view(sorted_arr)
        messagebox.showinfo("Insertion Sort Selesai", f"Perbandingan: {comp:,}\nPemindahan: {mov:,}")

    def run_merge_sort(self):
        kunci = self.sort_key_combo.get()
        sorted_arr, comp, mov = merge_sort(self.dataset_pesanan, kunci=kunci)
        self.cached_sorted_data = sorted_arr
        self.refresh_data_view(sorted_arr)
        messagebox.showinfo("Merge Sort Selesai", f"Perbandingan: {comp:,}\nPemindahan: {mov:,}")

    def run_linear_search(self):
        target = self.search_entry.get().strip()
        if not target:
            messagebox.showwarning("Peringatan", "Masukkan OID yang ingin dicari!")
            return
        idx, item, comp = linear_search(self.dataset_pesanan, target)
        if idx != -1:
            messagebox.showinfo("Ditemukan (Linear Search)", f"Data ditemukan pada indeks {idx}\nPerbandingan: {comp}\nPelanggan: {item.nama_pelanggan}")
        else:
            messagebox.showwarning("Tidak Ditemukan", f"OID {target} tidak ditemukan.\nTotal Perbandingan: {comp}")

    def run_binary_search(self):
        target = self.search_entry.get().strip()
        if not target:
            messagebox.showwarning("Peringatan", "Masukkan OID yang ingin dicari!")
            return
        
        if self.cached_sorted_data is None:
            self.cached_sorted_data, _, _ = merge_sort(self.dataset_pesanan, kunci='oid')

        idx, item, comp = binary_search(self.cached_sorted_data, target)
        if idx != -1:
            messagebox.showinfo("Ditemukan (Binary Search)", f"Data ditemukan pada indeks terurut {idx}\nPerbandingan: {comp}\nPelanggan: {item.nama_pelanggan}")
        else:
            messagebox.showwarning("Tidak Ditemukan", f"OID {target} tidak ditemukan.\nTotal Perbandingan: {comp}")

    def evaluate_rpn(self):
        expr = self.rpn_entry.get().strip()
        try:
            hasil = PostfixEvaluator.evaluate(expr)
            self.rpn_result_label.config(text=f"Hasil: {hasil}")
        except Exception as e:
            messagebox.showerror("Error RPN", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = App2EZ4U(root)
    root.mainloop()
