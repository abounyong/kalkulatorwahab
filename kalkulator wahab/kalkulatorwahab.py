import tkinter as tk     # Mengimpor Tkinter untuk GUI dasar
from tkinter import ttk  # Mengimpor ttk untuk scrollbar modern

# ============================================================
#  KELAS UTAMA KALKULATOR
# ============================================================
class SimpleCalculator:
    def __init__(self, root):  # Konstruktor menerima root window
        self.root = root  # Simpan referensi window utama
        self.root.title("Kalkulator item merah wahab")  # Judul window
        self.root.geometry("900x600")  # Ukuran window
        self.root.configure(bg="#1a1a1a")  # Background gelap

        # ============================================================
        #  VARIABEL PERHITUNGAN
        # ============================================================
        self.current_value = ""       # Angka saat ini di display
        self.previous_value = ""      # Angka sebelumnya sebelum operator
        self.operation = None         # Operator aktif (+,-,x,÷)
        self.should_reset_display = False  # Flag untuk reset display setelah hasil
        self.history_string = ""      # String untuk menyimpan history perhitungan

        # ============================================================
        #  FRAME UTAMA (KIRI = KALKULATOR, KANAN = HISTORY + NOTE)
        # ============================================================
        self.main_frame = tk.Frame(self.root, bg="#1a1a1a")  # Frame utama
        self.main_frame.pack(fill=tk.BOTH, expand=True)  # Memenuhi window

        # ============================================================
        #  FRAME KIRI — KALKULATOR (50% LEBAR)
        # ============================================================
        self.left_frame = tk.Frame(self.main_frame, bg="#1a1a1a")  # Frame kiri
        self.left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1.0)  # Tetap 50% lebar

        # ---------------- DISPLAY ----------------
        self.display_frame = tk.Frame(self.left_frame, bg="black", height=120)  # Display frame
        self.display_frame.pack(fill=tk.X)  # Horizontal penuh
        self.display_frame.pack_propagate(False)  # Ukuran tetap

        self.display_label = tk.Label(
            self.display_frame,
            text="0",  # Teks awal
            fg="red",  # Warna teks
            bg="black",  # Background
            font=("Arial", 48, "bold"),  # Font besar
            anchor="e"  # Rata kanan
        )
        self.display_label.pack(fill=tk.BOTH, padx=10, pady=10)  # Padding agar nyaman

        # ---------------- FRAME TOMBOL ----------------
        self.buttons_frame = tk.Frame(self.left_frame, bg="#000000")  # Frame tombol
        self.buttons_frame.pack(fill=tk.BOTH, expand=True)  # Full frame kiri

        button_layout = [  # Layout grid tombol
            ["C", "%", "÷", "+"],
            ["7", "8", "9", "-"],
            ["4", "5", "6", "x"],
            ["1", "2", "3", "="],
            ["0", "000", ".", "⌫"]
        ]

        for r, row in enumerate(button_layout):  # Loop tiap baris
            for c, text in enumerate(row):  # Loop tiap kolom
                self.create_button(text, r, c)  # Buat tombol

        # ============================================================
        #  FRAME KANAN — HISTORY + NOTE (50% LEBAR)
        # ============================================================
        self.right_frame = tk.Frame(self.main_frame, bg="#1a1a1a")  # Frame kanan
        self.right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1.0)  # Tetap 50%

        # ================= HISTORY FRAME =================
        self.history_frame = tk.LabelFrame(
            self.right_frame,
            text="History",  # Judul
            fg="red",
            bg="#1a1a1a",
            font=("Arial", 12, "bold")
        )
        self.history_frame.place(relx=0, rely=0, relwidth=1, relheight=0.5)  # Setengah atas

        self.clear_history_button = tk.Button(
            self.history_frame,
            text="Clear History",  # Tombol hapus
            bg="red",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.clear_history  # Memanggil fungsi clear_history
        )
        self.clear_history_button.pack(fill=tk.X, padx=5, pady=3)  # Full width tombol

        self.history_text = tk.Listbox(
            self.history_frame,
            bg="black",  # Background hitam
            fg="red",  # Teks merah
            font=("Courier", 12),  # Monospace agar rapi
            selectbackground="#333333"  # Highlight warna gelap
        )
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)  # Full frame

        self.history_scroll = ttk.Scrollbar(
            self.history_frame,
            orient=tk.VERTICAL,
            command=self.history_text.yview  # Scroll kontrol Listbox
        )
        self.history_scroll.pack(side=tk.RIGHT, fill=tk.Y)  # Scroll di kanan
        self.history_text.config(yscrollcommand=self.history_scroll.set)  # Sinkron scroll

        # ================= NOTE FRAME =================
        self.note_frame = tk.LabelFrame(
            self.right_frame,
            text="Note",  # Judul
            fg="red",
            bg="#1a1a1a",
            font=("Arial", 12, "bold")
        )
        self.note_frame.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)  # Setengah bawah

        self.note_text = tk.Text(
            self.note_frame,
            bg="black",
            fg="white",
            font=("Arial", 12),
            relief=tk.FLAT
        )
        self.note_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Bisa diketik bebas

    # ============================================================
    #  FUNGSI MEMBUAT TOMBOL
    # ============================================================
    def create_button(self, text, row, col):  # Membuat tombol
        if text in ["÷", "x", "-", "+", "=", "C", "%"]:  # Operator & fungsi
            bg = "#400000"
            fg = "red"
        elif text == "⌫":  # Tombol delete
            bg = "#600000"
            fg = "#FF4444"
        else:  # Angka
            bg = "red"
            fg = "black"

        btn = tk.Button(
            self.buttons_frame,
            text=text,
            bg=bg,
            fg=fg,
            font=("Arial", 22, "bold"),
            border=0,
            command=lambda t=text: self.button_click(t)  # Fungsi saat ditekan
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)  # Posisi grid
        self.buttons_frame.grid_rowconfigure(row, weight=1)  # Responsive baris
        self.buttons_frame.grid_columnconfigure(col, weight=1)  # Responsive kolom

    # ============================================================
    #  LOGIKA KALKULATOR
    # ============================================================
    def button_click(self, text):
        if text.isdigit() or text == ".":  # Angka atau titik
            self.append_number(text)
        elif text == "C":  # Reset display saja
            self.clear()
        elif text == "=":  # Hitung
            self.calculate()
        elif text == "⌫":  # Hapus terakhir
            self.delete_last()
        elif text == "%":  # Persen
            self.percent()
        else:  # Operator
            self.operation_click(text)

    def append_number(self, num):  # Menambahkan angka di display
        if self.should_reset_display:
            self.current_value = num
            self.should_reset_display = False
        else:
            if num == "." and "." in self.current_value:
                return
            if self.current_value == "" or self.current_value == "0":
                self.current_value = num
            else:
                self.current_value += num
        self.update_display()  # Update tampilan

    def operation_click(self, op):  # Saat operator ditekan
        if op == "-" and self.current_value == "":  # Negatif di awal
            self.current_value = "-"
            self.update_display()
            return
        if self.current_value != "":
            self.previous_value = self.current_value  # Simpan angka sebelumnya
            self.current_value = ""  # Reset display
        self.operation = op

    def calculate(self):  # Hitung saat "=" ditekan
        if not self.operation or self.previous_value == "" or self.current_value == "":
            return
        prev = float(self.previous_value)
        curr = float(self.current_value)
        if self.operation == "+": result = prev + curr
        elif self.operation == "-": result = prev - curr
        elif self.operation == "x": result = prev * curr
        elif self.operation == "÷": result = prev / curr if curr != 0 else 0
        else: return
        result_str = str(result).rstrip("0").rstrip(".")
        hist = f"{self.previous_value} {self.operation} {self.current_value} = {result_str}"
        self.history_text.insert(tk.END, hist)  # Masukkan ke history Listbox
        self.history_text.see(tk.END)  # Scroll otomatis ke bawah
        self.current_value = result_str  # Update display dengan hasil
        self.operation = None
        self.previous_value = ""
        self.update_display()

    def clear(self):  # Reset display saja
        self.current_value = ""
        self.update_display()

    def clear_history(self):  # Hapus semua history
        self.history_text.delete(0, tk.END)

    def delete_last(self):  # Hapus karakter terakhir
        self.current_value = self.current_value[:-1]
        if self.current_value == "":
            self.current_value = "0"
        self.update_display()

    def percent(self):  # Mengubah angka menjadi persen
        try:
            self.current_value = str(float(self.current_value) / 100)
        except:
            self.current_value = "0"
        self.update_display()

    def update_display(self):  # Update display label
        if self.current_value == "":
            self.display_label.config(text="0")
        else:
            self.display_label.config(text=self.current_value)

# ============================================================
#  RUN PROGRAM
# ============================================================
root = tk.Tk()  # Buat window Tkinter
SimpleCalculator(root)  # Buat instance kalkulator
root.mainloop()  # Loop utama GUI
