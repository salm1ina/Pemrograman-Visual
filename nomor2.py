# Bendera Serbia
print("\033c")       # Clear
import numpy as np
import matplotlib.pyplot as plt

row = int(1080)
col = int(1920)

# area merah 
Rrow1 = int(0.25*row)
Rrow2 = int(0.416*row)   
Rcol1 = int(0.25*col)
Rcol2 = int(0.75*col)

# area biru (tengah)
Brow1 = int(0.416*row) + 1
Brow2 = int(0.583*row)
Bcol1 = int(0.25*col)
Bcol2 = int(0.75*col)

# area putih (bawah)
Wrow1 = int(0.583*row) + 1
Wrow2 = int(0.75*row)
Wcol1 = int(0.25*col)
Wcol2 = int(0.75*col)

Gambar = np.zeros(shape=(row, col, 3), dtype=np.int16)

for i in range(Rrow1, Rrow2+1):
    for j in range(Rcol1, Rcol2):
        Gambar[i, j, 0] = 255  

for i in range(Brow1, Brow2+1):
    for j in range(Bcol1, Bcol2):
        Gambar[i, j, 2] = 255  

for i in range(Wrow1, Wrow2+1):
    for j in range(Wcol1, Wcol2):
        Gambar[i, j, :] = 255  

# --- ROTASI hanya bendera ---
# ambil potongan bendera
flag = Gambar[Rrow1:Wrow2+1, Rcol1:Wcol2, :]

# rotasi 90 derajat searah jarum jam
flag_rot = np.rot90(flag, k=3)

# buat canvas baru (tetap hitam)
Gambar2 = np.zeros_like(Gambar)

# cari posisi tengah untuk tempel flag_rot
fr, fc, _ = flag_rot.shape
start_r = (row - fr) // 2
start_c = (col - fc) // 2

# tempelkan bendera yang sudah diputar
Gambar2[start_r:start_r+fr, start_c:start_c+fc, :] = flag_rot

plt.figure()
plt.imshow(Gambar2)
plt.show()

