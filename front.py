import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# STRUCTDAT MODULE: M2_Stack-Queue
# ==========================================

class Stack:
    """Implementasi Stack LIFO (Last-In-First-Out)"""
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


def evaluate_postfix(expression_str):
    """
    Evaluasi ekspresi matematika Postfix (RPN) menggunakan Stack.
    Contoh: "10 5 + 0.9 *" -> (10 + 5) * 0.9 = 13.5
    """
    stack = Stack()
    tokens = expression_str.strip().split()
    
    for token in tokens:
        if token in ("+", "-", "*", "/", "%", "^"):
            val2 = stack.pop()
            val1 = stack.pop()
            if val1 is None or val2 is None:
                raise ValueError("Invalid Postfix Expression")
            
            if token == "+":
                res = val1 + val2
            elif token == "-":
                res = val1 - val2
            elif token == "*":
                res = val1 * val2
            elif token == "/":
                res = val1 / val2 if val2 != 0 else 0
            elif token == "%":
                res = val1 % val2
            elif token == "^":
                res = val1 ** val2
            stack.push(res)
        else:
            try:
                stack.push(float(token))
            except ValueError:
                raise ValueError(f"Invalid token: {token}")

    if stack.size() != 1:
        raise ValueError("Invalid Postfix Expression")
    return stack.pop()


class NaiveQueue:
    """
    Implementasi Queue Naif (Linear FIFO Queue)
    Operasi Dequeue memindahkan seluruh elemen setelah index 0.
    """
    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            return None
        return self._items.pop(0)

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def get_all(self):
        return list(self._items)


class CircularQueue:
    """
    Implementasi Circular Queue (Fixed Capacity Ring Buffer)
    Memanfaatkan pointer front & rear dengan operasi modulo O(1).
    """
    def __init__(self, capacity=5):
        self.capacity = capacity
        self._queue = [None] * capacity
        self.front = -1
        self.rear = -1
        self.count = 0

    def is_full(self):
        return self.count == self.capacity

    def is_empty(self):
        return self.count == 0

    def enqueue(self, item):
        if self.is_full():
            self.dequeue()  # Rotasi saat penuh
        
        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity

        self._queue[self.rear] = item
        self.count += 1

    def dequeue(self):
        if self.is_empty():
            return None
        
        item = self._queue[self.front]
        self._queue[self.front] = None
        
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
            
        self.count -= 1
        return item

    def get_all(self):
        if self.is_empty():
            return []
        res = []
        idx = self.front
        for _ in range(self.count):
            res.append(self._queue[idx])
            idx = (idx + 1) % self.capacity
        return res


# ==========================================
# GUI APPLICATION (JavaCafeApp)
# ==========================================

class JavaCafeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Java Café - Food & Coffee Delivery")
        self.geometry("430x820")
        self.resizable(False, False)
        self.configure(bg="#1E1E24")

        # Color Palette
        self.colors = {
            "bg": "#121216",            
            "card_bg": "#1C1C24",       
            "card_inner": "#252532",    
            "accent": "#C67C4E",        
            "accent_light": "#EDA97A",  
            "text_white": "#FFFFFF",
            "text_muted": "#A2A2AD",
            "star_gold": "#FBBE21",     
            "nav_bg": "#1A1A22",        
            "search_bg": "#252530",
            "badge_green": "#2ECC71"
        }

        # Data Structures Integration
        self.cart_stack = Stack()
        self.cart_items = []
        self.order_naive_queue = NaiveQueue()
        self.recent_activity_circular = CircularQueue(capacity=4)

        self.categories = ["All Coffee", "Espresso", "Latte", "Cappuccino", "Cold Brew"]
        self.selected_category = "All Coffee"

        self.products = [
            {"id": 1, "name": "Caffe Mocha", "subtitle": "Deep Chocolate & Milk", "price": 4.50, "rating": 4.8, "category": "Espresso", "icon": "☕"},
            {"id": 2, "name": "Flat White", "subtitle": "Espresso & Microfoam", "price": 3.90, "rating": 4.7, "category": "Latte", "icon": "🥛"},
            {"id": 3, "name": "Caramel Macchiato", "subtitle": "Vanilla & Caramel Drizzle", "price": 4.99, "rating": 4.9, "category": "Latte", "icon": "🍯"},
            {"id": 4, "name": "Cold Brew Cream", "subtitle": "Smooth Cold Brew Coffee", "price": 4.20, "rating": 4.6, "category": "Cold Brew", "icon": "🧊"},
            {"id": 5, "name": "Classic Cappuccino", "subtitle": "Rich Foam & Espresso", "price": 3.75, "rating": 4.5, "category": "Cappuccino", "icon": "☕"}
        ]

        self._build_ui()

    def _build_ui(self):
        main_container = tk.Frame(self, bg=self.colors["bg"])
        main_container.pack(fill="both", expand=True)

        header_frame = tk.Frame(main_container, bg=self.colors["bg"], padx=20, pady=15)
        header_frame.pack(fill="x")

        loc_sub = tk.Label(header_frame, text="LOCATION", font=("Segoe UI", 8, "bold"), fg=self.colors["text_muted"], bg=self.colors["bg"], anchor="w")
        loc_sub.pack(fill="x")

        loc_title = tk.Label(header_frame, text="Surabaya, East Java 📍", font=("Segoe UI", 12, "bold"), fg=self.colors["text_white"], bg=self.colors["bg"], anchor="w")
        loc_title.pack(fill="x")

        avatar_btn = tk.Button(header_frame, text="☕", font=("Segoe UI", 14), bg=self.colors["card_inner"], fg=self.colors["accent"], bd=0, relief="flat", cursor="hand2")
        avatar_btn.place(relx=1.0, rely=0.1, anchor="ne", width=40, height=40)

        # Notebook Tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=self.colors["bg"], borderwidth=0)
        style.configure('TNotebook.Tab', background=self.colors["card_bg"], foreground="white", padding=[10, 6])
        style.map('TNotebook.Tab', background=[('selected', self.colors["accent"])])

        self.tab_home = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.tab_cart = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.tab_queue = tk.Frame(self.notebook, bg=self.colors["bg"])

        self.notebook.add(self.tab_home, text=" Menu ")
        self.notebook.add(self.tab_cart, text=" Cart & Postfix ")
        self.notebook.add(self.tab_queue, text=" Kitchen & Tracker ")

        self._build_home_tab()
        self._build_cart_tab()
        self._build_queue_tab()

    def _build_home_tab(self):
        search_frame = tk.Frame(self.tab_home, bg=self.colors["search_bg"], padx=10, pady=6)
        search_frame.pack(fill="x", padx=15, pady=(10, 10))

        search_icon = tk.Label(search_frame, text="🔍", font=("Segoe UI", 11), fg=self.colors["text_muted"], bg=self.colors["search_bg"])
        search_icon.pack(side="left", padx=(4, 8))

        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), bg=self.colors["search_bg"], fg=self.colors["text_white"], bd=0, insertbackground=self.colors["text_white"])
        self.search_entry.insert(0, "Search coffee, drinks...")
        self.search_entry.bind("<FocusIn>", self._clear_placeholder)
        self.search_entry.bind("<KeyRelease>", self._filter_products)
        self.search_entry.pack(side="left", fill="x", expand=True)

        filter_btn = tk.Button(search_frame, text="⚙", font=("Segoe UI", 10), bg=self.colors["accent"], fg="white", bd=0, width=3, height=1, cursor="hand2")
        filter_btn.pack(side="right")

        cat_frame = tk.Frame(self.tab_home, bg=self.colors["bg"])
        cat_frame.pack(fill="x", padx=15, pady=(0, 10))

        self.cat_buttons = []
        for cat in self.categories:
            is_active = (cat == self.selected_category)
            btn = tk.Button(cat_frame, text=cat, font=("Segoe UI", 8, "bold" if is_active else "normal"), bg=self.colors["accent"] if is_active else self.colors["card_bg"], fg="white" if is_active else self.colors["text_muted"], bd=0, padx=8, pady=4, cursor="hand2", command=lambda c=cat: self._select_category(c))
            btn.pack(side="left", padx=(0, 5))
            self.cat_buttons.append((cat, btn))

        grid_container = tk.Frame(self.tab_home, bg=self.colors["bg"])
        grid_container.pack(fill="both", expand=True, padx=15)

        canvas = tk.Canvas(grid_container, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(grid_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.colors["bg"])

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.products_frame = self.scrollable_frame
        self._render_products(self.products)

    def _clear_placeholder(self, event):
        if self.search_entry.get() == "Search coffee, drinks...":
            self.search_entry.delete(0, tk.END)

    def _select_category(self, category_name):
        self.selected_category = category_name
        for cat, btn in self.cat_buttons:
            if cat == category_name:
                btn.configure(bg=self.colors["accent"], fg="white", font=("Segoe UI", 8, "bold"))
            else:
                btn.configure(bg=self.colors["card_bg"], fg=self.colors["text_muted"], font=("Segoe UI", 8, "normal"))

        filtered = self.products if category_name == "All Coffee" else [p for p in self.products if p["category"] == category_name]
        self._render_products(filtered)

    def _filter_products(self, event):
        query = self.search_entry.get().lower()
        if query == "search coffee, drinks...":
            query = ""
        filtered = [p for p in self.products if query in p["name"].lower() or query in p["subtitle"].lower()]
        self._render_products(filtered)

    def _render_products(self, product_list):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        col_count = 2
        for idx, prod in enumerate(product_list):
            row = idx // col_count
            col = idx % col_count

            card = tk.Frame(self.products_frame, bg=self.colors["card_bg"], padx=8, pady=8, width=175, height=210)
            card.grid(row=row, column=col, padx=5, pady=6, sticky="nsew")
            card.grid_propagate(False)

            img_box = tk.Frame(card, bg=self.colors["card_inner"], height=90)
            img_box.pack(fill="x")
            img_box.pack_propagate(False)

            icon_lbl = tk.Label(img_box, text=prod["icon"], font=("Segoe UI", 32), bg=self.colors["card_inner"])
            icon_lbl.pack(expand=True)

            rating_lbl = tk.Label(img_box, text=f"★ {prod['rating']}", font=("Segoe UI", 8, "bold"), fg=self.colors["star_gold"], bg="#2C2C38", padx=4, pady=1)
            rating_lbl.place(x=4, y=4)

            title_lbl = tk.Label(card, text=prod["name"], font=("Segoe UI", 9, "bold"), fg=self.colors["text_white"], bg=self.colors["card_bg"], anchor="w")
            title_lbl.pack(fill="x", pady=(6, 2))

            sub_lbl = tk.Label(card, text=prod["subtitle"], font=("Segoe UI", 7), fg=self.colors["text_muted"], bg=self.colors["card_bg"], anchor="w")
            sub_lbl.pack(fill="x")

            bottom_row = tk.Frame(card, bg=self.colors["card_bg"])
            bottom_row.pack(fill="x", pady=(8, 0), side="bottom")

            price_lbl = tk.Label(bottom_row, text=f"${prod['price']:.2f}", font=("Segoe UI", 10, "bold"), fg=self.colors["text_white"], bg=self.colors["card_bg"])
            price_lbl.pack(side="left")

            add_btn = tk.Button(bottom_row, text="+", font=("Segoe UI", 10, "bold"), bg=self.colors["accent"], fg="white", bd=0, width=3, height=1, cursor="hand2", command=lambda p=prod: self._add_to_cart(p))
            add_btn.pack(side="right")

    def _build_cart_tab(self):
        container = tk.Frame(self.tab_cart, bg=self.colors["bg"], padx=15, pady=15)
        container.pack(fill="both", expand=True)

        lbl_cart = tk.Label(container, text="🛒 Active Cart (Stack Backtracking)", font=("Segoe UI", 11, "bold"), fg=self.colors["text_white"], bg=self.colors["bg"])
        lbl_cart.pack(anchor="w")

        self.cart_listbox = tk.Listbox(container, bg=self.colors["card_bg"], fg="white", bd=0, highlightthickness=0, font=("Segoe UI", 10), height=6)
        self.cart_listbox.pack(fill="x", pady=8)

        btn_row = tk.Frame(container, bg=self.colors["bg"])
        btn_row.pack(fill="x", pady=(0, 15))

        undo_btn = tk.Button(btn_row, text="↩ Pop Last Item (Stack Undo)", bg="#E74C3C", fg="white", bd=0, padx=10, pady=5, font=("Segoe UI", 9, "bold"), command=self._undo_cart_stack)
        undo_btn.pack(side="left")

        postfix_frame = tk.LabelFrame(container, text=" 🧮 Postfix Discount & Total Calculation ", bg=self.colors["card_bg"], fg=self.colors["accent"], font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        postfix_frame.pack(fill="x", pady=10)

        info_lbl = tk.Label(postfix_frame, text="Masukkan rumus postfix (misal: '15 0.9 *' = diskon 10%):\nContoh default: [Subtotal] 0.9 *", font=("Segoe UI", 8), fg=self.colors["text_muted"], bg=self.colors["card_bg"], justify="left")
        info_lbl.pack(anchor="w", pady=(0, 5))

        self.postfix_entry = tk.Entry(postfix_frame, font=("Segoe UI", 10), bg=self.colors["search_bg"], fg="white", bd=0)
        self.postfix_entry.insert(0, "10 5 + 0.9 *")
        self.postfix_entry.pack(fill="x", pady=5)

        calc_btn = tk.Button(postfix_frame, text="Hitung Total via Postfix Stack", bg=self.colors["accent"], fg="white", bd=0, font=("Segoe UI", 9, "bold"), command=self._calculate_postfix_bill)
        calc_btn.pack(fill="x", pady=5)

        self.lbl_subtotal = tk.Label(postfix_frame, text="Subtotal: $0.00", font=("Segoe UI", 10), fg="white", bg=self.colors["card_bg"])
        self.lbl_subtotal.pack(anchor="w", pady=(5, 0))

        self.lbl_postfix_result = tk.Label(postfix_frame, text="Total Setelah Postfix: $0.00", font=("Segoe UI", 11, "bold"), fg=self.colors["badge_green"], bg=self.colors["card_bg"])
        self.lbl_postfix_result.pack(anchor="w")

        checkout_btn = tk.Button(container, text="🚀 Checkout Order -> Enqueue ke Dapur", bg=self.colors["badge_green"], fg="black", bd=0, font=("Segoe UI", 11, "bold"), pady=8, command=self._checkout_to_naive_queue)
        checkout_btn.pack(fill="x", side="bottom", pady=10)

    def _build_queue_tab(self):
        container = tk.Frame(self.tab_queue, bg=self.colors["bg"], padx=15, pady=15)
        container.pack(fill="both", expand=True)

        lbl_q1 = tk.Label(container, text="👨‍🍳 Dapur: Order Processing Queue (Naive FIFO)", font=("Segoe UI", 10, "bold"), fg=self.colors["text_white"], bg=self.colors["bg"])
        lbl_q1.pack(anchor="w")

        self.naive_queue_list = tk.Listbox(container, bg=self.colors["card_bg"], fg="white", bd=0, highlightthickness=0, font=("Segoe UI", 9), height=5)
        self.naive_queue_list.pack(fill="x", pady=5)

        deq_naive_btn = tk.Button(container, text="⚡ Dequeue Naive (Proses Pesanan Paling Depan)", bg=self.colors["accent"], fg="white", bd=0, font=("Segoe UI", 9, "bold"), pady=5, command=self._dequeue_naive_order)
        deq_naive_btn.pack(fill="x", pady=(0, 15))

        lbl_q2 = tk.Label(container, text="🔄 Order History Tracker (Circular Queue / Ring Buffer)", font=("Segoe UI", 10, "bold"), fg=self.colors["text_white"], bg=self.colors["bg"])
        lbl_q2.pack(anchor="w")

        lbl_q2_sub = tk.Label(container, text="Mencatat maksimal 4 aktivitas pesanan terakhir secara berputar (Cap: 4)", font=("Segoe UI", 8), fg=self.colors["text_muted"], bg=self.colors["bg"])
        lbl_q2_sub.pack(anchor="w")

        self.circular_queue_list = tk.Listbox(container, bg=self.colors["card_bg"], fg=self.colors["star_gold"], bd=0, highlightthickness=0, font=("Segoe UI", 9), height=5)
        self.circular_queue_list.pack(fill="x", pady=5)

        deq_circ_btn = tk.Button(container, text="🗑️ Dequeue Circular Buffer (Hapus Status Tertua)", bg="#9B59B6", fg="white", bd=0, font=("Segoe UI", 9, "bold"), pady=5, command=self._dequeue_circular_tracker)
        deq_circ_btn.pack(fill="x", pady=5)

    def _add_to_cart(self, product):
        self.cart_stack.push(product)
        self.cart_items.append(product)
        self._refresh_cart_ui()
        messagebox.showinfo("Cart Update", f"Pushed '{product['name']}' to Stack Cart!")

    def _undo_cart_stack(self):
        popped = self.cart_stack.pop()
        if popped:
            self.cart_items.remove(popped)
            self._refresh_cart_ui()
            messagebox.showinfo("Stack Pop", f"Popped/Undid '{popped['name']}' from Cart!")
        else:
            messagebox.showwarning("Stack Empty", "Keranjang kosong!")

    def _refresh_cart_ui(self):
        self.cart_listbox.delete(0, tk.END)
        subtotal = 0.0
        for idx, item in enumerate(self.cart_items, 1):
            self.cart_listbox.insert(tk.END, f"{idx}. {item['name']} - ${item['price']:.2f}")
            subtotal += item["price"]

        self.lbl_subtotal.config(text=f"Subtotal: ${subtotal:.2f}")
        if subtotal > 0:
            self.postfix_entry.delete(0, tk.END)
            self.postfix_entry.insert(0, f"{subtotal:.2f} 0.9 *")

    def _calculate_postfix_bill(self):
        expr = self.postfix_entry.get()
        try:
            total = evaluate_postfix(expr)
            self.lbl_postfix_result.config(text=f"Total Setelah Postfix: ${total:.2f}")
        except Exception as e:
            messagebox.showerror("Postfix Error", f"Ekspresi Postfix Tidak Valid:\n{str(e)}")

    def _checkout_to_naive_queue(self):
        if not self.cart_items:
            messagebox.showwarning("Empty Cart", "Keranjang kosong!")
            return

        items_summary = ", ".join([p["name"] for p in self.cart_items])
        order_data = f"Order #{self.order_naive_queue.size() + 1}: [{items_summary}]"
        
        self.order_naive_queue.enqueue(order_data)
        
        self.cart_items.clear()
        self.cart_stack = Stack()
        self._refresh_cart_ui()

        self._refresh_queue_ui()
        messagebox.showinfo("Checkout Success", "Pesanan berhasil di-enqueue ke Antrean Dapur (Naive Queue)!")

    def _dequeue_naive_order(self):
        processed = self.order_naive_queue.dequeue()
        if processed:
            self.recent_activity_circular.enqueue(f"Completed: {processed}")
            self._refresh_queue_ui()
            messagebox.showinfo("Naive Dequeue", f"Diproses: {processed}\nStatus dikirim ke Circular Tracker!")
        else:
            messagebox.showwarning("Queue Empty", "Tidak ada antrean pesanan di Dapur.")

    def _dequeue_circular_tracker(self):
        removed = self.recent_activity_circular.dequeue()
        if removed:
            self._refresh_queue_ui()
            messagebox.showinfo("Circular Dequeue", f"Dihapus dari Ring Buffer: {removed}")
        else:
            messagebox.showwarning("Circular Empty", "Circular Queue Tracker kosong.")

    def _refresh_queue_ui(self):
        self.naive_queue_list.delete(0, tk.END)
        for order in self.order_naive_queue.get_all():
            self.naive_queue_list.insert(tk.END, f"⏳ {order}")

        self.circular_queue_list.delete(0, tk.END)
        for act in self.recent_activity_circular.get_all():
            self.circular_queue_list.insert(tk.END, f"✅ {act}")

if __name__ == "__main__":
    app = JavaCafeApp()
    app.mainloop()