import tkinter as tk                    #import modul tkinter untuk GUI
from tkinter import ttk, messagebox     #import ttk (widget modern) & messagebox (popup)

#List untuk menyimpan data keuangan
data_keuangan = []

def format_rp(angka):
    return f"Rp {angka:,.0f}"   #fungsi utk format angka jadi Rupiah

#Fungsi untuk menghitung dan update total saldo
def update_saldo():
    try:
        total_pemasukan = sum(jumlah for kategori, _, jumlah in data_keuangan if kategori == "Pemasukan")
        total_pengeluaran = sum(jumlah for kategori, _, jumlah in data_keuangan if kategori == "Pengeluaran")
        sisa = total_pemasukan - total_pengeluaran

        label_pemasukan.config(text=f"Total Pemasukan: {format_rp(total_pemasukan)}")
        label_pengeluaran.config(text=f"Total Pengeluaran: {format_rp(total_pengeluaran)}")
        label_sisa.config(text=f"Sisa Saldo: {format_rp(sisa)}")

    except (ValueError, IndexError):
        label_pemasukan.config(text="Total Pemasukan: Rp 0")
        label_pengeluaran.config(text="Total Pengeluaran: Rp 0")
        label_sisa.config(text="Sisa Saldo: Rp 0")


#Fungsi untuk menambahkan data ke dalam tabel dan list 
def tambah_data():
    kategori = combo_kategori.get()
    keterangan = entry_keterangan.get()
    jumlah_str = entry_jumlah.get()
   
    # Validasi Input
    if not kategori or not jumlah_str or not keterangan:
        messagebox.showwarning("Alert", "Kategori, Keterangan dan Jumlah harus diisi!!")
        return
   
    try:
        jumlah_str_cleaned = jumlah_str.replace(",", "").replace(".", "")
        jumlah = float(jumlah_str_cleaned)
    except ValueError:
        messagebox.showerror("Error", "Jumlah harus berupa angka!")
        return

    #Tambahkan data ke list
    data_keuangan.append((kategori, keterangan, jumlah))
   
    #Tambahkan data ke tabel
    tabel.insert("", "end", values=(kategori, keterangan, format_rp(jumlah)))

    #Kosongkan kolom input setelah data ditambahkan
    combo_kategori.set("")
    entry_keterangan.delete(0, tk.END)
    entry_jumlah.delete(0, tk.END)
   
    #Panggil fungsi untuk memperbarui saldo
    update_saldo() 

#Membuat windownya dan atur ukurannya
window = tk.Tk()
lebar =650
tinggi =600
#x =500
#y =100

#Judul dan nama aplikasi
window.title("FinKos")
label_judul = tk.Label(window, text="Aplikasi Catatan Keuangan Sederhana 𐔌՞꜆. ̫.꜀՞𐦯", font=("Product Sans", 16, "bold"))
label_judul.pack(pady=20)

#Frame input
frame_input = tk.Frame(window)
frame_input.pack(pady=8)

tk.Label(frame_input, text="Kategori:").grid(row=0, column=0, padx=5, pady=5)
combo_kategori = ttk.Combobox(frame_input, values=["Pemasukan", "Pengeluaran"], state="readonly")
combo_kategori.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame_input, text="Keterangan:").grid(row=1, column=0, padx=5, pady=5)
entry_keterangan = tk.Entry(frame_input)
entry_keterangan.grid(row=1, column=1, padx=10, pady=10)

tk.Label(frame_input, text="Jumlah:").grid(row=2, column=0, padx=5, pady=5)
entry_jumlah = tk.Entry(frame_input)
entry_jumlah.grid(row=2, column=1, padx=5, pady=5)

btn_tambah = tk.Button(frame_input, text="Tambah", command=tambah_data)
btn_tambah.grid(row=3, columnspan=2, pady=5)

#Tabel
tabel = ttk.Treeview(window, columns=("Kategori", "Keterangan", "Jumlah"), show="headings")
tabel.heading("Kategori", text="Kategori")
tabel.heading("Keterangan", text="Keterangan")
tabel.heading("Jumlah", text="Jumlah (Rp)")

#Biar rapi, semua kolom sama lebar
tabel.column("Kategori", width=200, anchor="center")
tabel.column("Keterangan", width=200, anchor="w")
tabel.column("Jumlah", width=200, anchor="e")

tabel.pack(pady=10, fill="x")

#Label untuk menampilkan saldo
frame_saldo = tk.Frame(window)
frame_saldo.pack(pady=10)

label_pemasukan = tk.Label(frame_saldo, text="Total Pemasukan: Rp 0", font=("Product Sans", 12, "bold"))
label_pemasukan.pack(anchor="center", pady=3)

label_pengeluaran = tk.Label(frame_saldo, text="Total Pengeluaran: Rp 0", font=("Product Sans", 12, "bold"))
label_pengeluaran.pack(anchor="center", pady=3)

label_sisa = tk.Label(frame_saldo, text="Sisa Saldo: Rp 0", font=("Product Sans", 12, "bold"))
label_sisa.pack(anchor="center", pady=3)

#Mengatur windownya akan muncul ditengah layar
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
newx = int((screenwidth/2) - (lebar/2))
newy = int((screenheight/2) - (tinggi/2))

window.geometry(f"{lebar}x{tinggi}+{newx}+{newy}")

window.mainloop()