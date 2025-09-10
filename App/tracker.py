import tkinter as tk

#Membuat windownya dan atur ukurannya
window= tk.Tk()
lebar =600
tinggi =600
x =500
y =100

window.title("Expense Tracker") 

#Mengatur windownya akan muncul ditengah
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
newx = int((screenwidth/2) - (lebar/2))
newy = int((screenheight/2) - (tinggi/2))

window.geometry(f"{lebar}x{tinggi}+{newx}+{newy}")

window.mainloop()