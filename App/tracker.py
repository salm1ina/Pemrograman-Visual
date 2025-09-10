import tkinter as tk
from tkinter import ttk, messagebox

#List untuk menyimpan data keuangan
data_keuangan = []

#Fungsi untuk menghitung n upgrade total saldo
def update_saldo():
    "Menghitung total saldo dari data_keuangan dan memperbarui label."
    try:
        total = sum([jumlah for _, jumlah in data_keuangan])

        label_saldo.config(text=f"Total saldo: Rp {total:,.0f}")
    except (ValueError, IndexError):
        label_saldo.config(text="Total saldo: Rp 0")

#Fungsi untuk menambahkan data ke dalam tabel dan list 
def tambah_data():
    "Mengambil input, memvalidasi, lalu menambahkan data ke list dan tabel."
    kategori = entry_kategori.get()
    jumlah_str = entry_jumlah.get()

    #Validasi Input
    if not kategori or not jumlah_str:
        messagebox.showwarning("Alert", "Kategori dan Jumlah harus diisi!!")
        return
    
    try: 
        jumlah_str_cleaned = jumlah_str.replace(",", ".").replace(".", "")
        jumlah = float(jumlah_str_cleaned)
    except ValueError:
        messagebox.showerror("Error", "Jumlah harus berupa angka!")
        return
    
 # Tambahkan data ke list
    data_keuangan.append((kategori, jumlah))
    
    # Tambahkan data ke tabel
    tabel.insert("", "end", values=(kategori, jumlah))

    # Kosongkan kolom input setelah data ditambahkan
    entry_kategori.delete(0, tk.END)
    entry_jumlah.delete(0, tk.END)
    
    # Panggil fungsi untuk memperbarui saldo
    update_saldo() 

#Membuat windownya dan atur ukurannya
window = tk.Tk()
lebar =600
tinggi =600
#x =500
#y =100

#Judul dan nama aplikasi
window.title("Expense Tracker")
label_judul = tk.Label(window, text="Aplikasi Catatan Keuangan Sederhana 𐔌՞꜆. ̫.꜀՞𐦯", font=("Product Sans", 16, "bold"))
label_judul.pack(pady=20)

#Frame inputan
frame_input = tk.Frame(window)
frame_input.pack(pady=8)

tk.Label(frame_input, text="Kategori:").grid(row=0, column=0, padx=5, pady=5)
entry_kategori = tk.Entry(frame_input)
entry_kategori.grid(row=0, column=1, padx= 10, pady=10)

tk.Label(frame_input, text="Jumlah:").grid(row=1, column=0, padx=5, pady=5)
entry_jumlah = tk.Entry(frame_input)
entry_jumlah.grid(row=1, column=1, padx=5, pady=5)

#Button
btn_tambah = tk.Button(frame_input, text="Tambah", command=tambah_data)
btn_tambah.grid(row=2, columnspan=2, pady=5)

#Tabel 
tabel = ttk.Treeview(window, columns=("Kategori", "Jumlah"), show="headings")
tabel.heading("Kategori", text="Kategori")
tabel.heading("Jumlah", text="Jumlah (Rp)")
tabel.pack(pady=10, fill="x")

#Label Saldo
label_saldo = tk.Label(window, text="Total Saldo: Rp 0", font=("Arial", 12, "bold"))
label_saldo.pack(pady=10)

#Label untuk menampilkan saldo
label_saldo = tk.Label(window, text="Total Saldo: Rp 0", font=("Product Sans", 12, "bold"))
label_saldo.pack(pady=10)

#Mengatur windownya akan muncul ditengah layar
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
newx = int((screenwidth/2) - (lebar/2))
newy = int((screenheight/2) - (tinggi/2))

window.geometry(f"{lebar}x{tinggi}+{newx}+{newy}")

window.mainloop() 