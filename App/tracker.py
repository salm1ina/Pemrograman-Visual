import tkinter as tk
from tkinter import ttk, messagebox

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



#Mengatur windownya akan muncul ditengah layar
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
newx = int((screenwidth/2) - (lebar/2))
newy = int((screenheight/2) - (tinggi/2))

window.geometry(f"{lebar}x{tinggi}+{newx}+{newy}")



window.mainloop()