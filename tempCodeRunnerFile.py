import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QDateEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont


class KeuanganApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Keuangan Pribadi")
        self.resize(900, 1000)

        # Font utama
        self.font_label = QFont("Product Sans", 14)
        self.font_input = QFont("Product Sans", 14)
        self.font_title = QFont("Product Sans", 18, QFont.Bold)

        layout = QVBoxLayout()

        # Judul
        title = QLabel("Aplikasi Keuangan Pribadi")
        title.setFont(self.font_title)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Bagian Form
        form_layout = QVBoxLayout()

        # Tanggal
        hbox_tanggal = QHBoxLayout()
        lbl_tanggal = QLabel("Tanggal:")
        lbl_tanggal.setFont(self.font_label)
        self.input_tanggal = QDateEdit()
        self.input_tanggal.setDate(QDate.currentDate())
        self.input_tanggal.setCalendarPopup(True)
        self.input_tanggal.setFont(self.font_input)
        self.input_tanggal.setFixedHeight(40)
        hbox_tanggal.addWidget(lbl_tanggal, 1)
        hbox_tanggal.addWidget(self.input_tanggal, 3)
        form_layout.addLayout(hbox_tanggal)

        # Kategori
        hbox_kategori = QHBoxLayout()
        lbl_kategori = QLabel("Kategori:")
        lbl_kategori.setFont(self.font_label)
        self.input_kategori = QComboBox()
        self.input_kategori.addItems(["Pemasukan", "Pengeluaran"])
        self.input_kategori.setFont(self.font_input)
        self.input_kategori.setFixedHeight(40)
        hbox_kategori.addWidget(lbl_kategori, 1)
        hbox_kategori.addWidget(self.input_kategori, 3)
        form_layout.addLayout(hbox_kategori)

        # Keterangan
        hbox_keterangan = QHBoxLayout()
        lbl_keterangan = QLabel("Keterangan:")
        lbl_keterangan.setFont(self.font_label)
        self.input_keterangan = QTextEdit()
        self.input_keterangan.setFont(self.font_input)
        self.input_keterangan.setFixedHeight(60)
        hbox_keterangan.addWidget(lbl_keterangan, 1)
        hbox_keterangan.addWidget(self.input_keterangan, 3)
        form_layout.addLayout(hbox_keterangan)

        # Jumlah
        hbox_jumlah = QHBoxLayout()
        lbl_jumlah = QLabel("Jumlah:")
        lbl_jumlah.setFont(self.font_label)
        self.input_jumlah = QLineEdit()
        self.input_jumlah.setFont(self.font_input)
        self.input_jumlah.setFixedHeight(40)
        self.input_jumlah.setPlaceholderText("Masukkan angka...")
        hbox_jumlah.addWidget(lbl_jumlah, 1)
        hbox_jumlah.addWidget(self.input_jumlah, 3)
        form_layout.addLayout(hbox_jumlah)

        # Tombol Tambah (lebih dekat ke form)
        self.btn_tambah = QPushButton("Tambah")
        self.btn_tambah.setFont(QFont("Product Sans", 14, QFont.Bold))
        self.btn_tambah.setFixedHeight(45)
        self.btn_tambah.clicked.connect(self.tambah_data)
        form_layout.addWidget(self.btn_tambah, alignment=Qt.AlignRight)

        layout.addLayout(form_layout)

        # Filter
        filter_layout = QHBoxLayout()
        lbl_filter = QLabel("Filter:")
        lbl_filter.setFont(self.font_label)
        self.filter_kategori = QComboBox()
        self.filter_kategori.addItems(["Semua", "Pemasukan", "Pengeluaran"])
        self.filter_kategori.setFont(self.font_input)
        self.filter_kategori.setFixedHeight(35)
        self.filter_kategori.currentIndexChanged.connect(self.terapkan_filter)
        filter_layout.addWidget(lbl_filter)
        filter_layout.addWidget(self.filter_kategori)
        layout.addLayout(filter_layout)

        # Tabel Data
        self.tabel = QTableWidget()
        self.tabel.setColumnCount(4)
        self.tabel.setHorizontalHeaderLabels(["Tanggal", "Kategori", "Keterangan", "Jumlah"])
        self.tabel.setFont(QFont("Product Sans", 12))
        self.tabel.setFixedHeight(250)
        layout.addWidget(self.tabel)

        self.setLayout(layout)

        # Data disimpan di list
        self.data = []

    def tambah_data(self):
        """Validasi & Tambah Data ke Tabel"""
        tanggal = self.input_tanggal.date().toString("dd/MM/yyyy")
        kategori = self.input_kategori.currentText()
        keterangan = self.input_keterangan.toPlainText().strip()
        jumlah = self.input_jumlah.text().strip()

        # Validasi input
        if not keterangan or not jumlah:
            QMessageBox.warning(self, "Input Kosong", "Keterangan dan Jumlah harus diisi!")
            return

        if not jumlah.isdigit():
            QMessageBox.warning(self, "Format Salah", "Jumlah harus berupa angka!")
            return

        # Simpan data ke list
        self.data.append({
            "tanggal": tanggal,
            "kategori": kategori,
            "keterangan": keterangan,
            "jumlah": int(jumlah)
        })

        # Reset input
        self.input_keterangan.clear()
        self.input_jumlah.clear()

        # Update tabel
        self.tampilkan_data()

    def tampilkan_data(self, kategori_filter="Semua"):
        """Menampilkan data di tabel"""
        self.tabel.setRowCount(0)  # reset tabel

        for item in self.data:
            if kategori_filter != "Semua" and item["kategori"] != kategori_filter:
                continue

            row_position = self.tabel.rowCount()
            self.tabel.insertRow(row_position)
            self.tabel.setItem(row_position, 0, QTableWidgetItem(item["tanggal"]))
            self.tabel.setItem(row_position, 1, QTableWidgetItem(item["kategori"]))
            self.tabel.setItem(row_position, 2, QTableWidgetItem(item["keterangan"]))
            self.tabel.setItem(row_position, 3, QTableWidgetItem(f"Rp {item['jumlah']:,}".replace(",", ".")))

    def terapkan_filter(self):
        """Filter data berdasarkan kategori"""
        kategori = self.filter_kategori.currentText()
        self.tampilkan_data(kategori)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeuanganApp()
    window.show()
    sys.exit(app.exec_())
