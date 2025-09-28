import sys
import csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QGridLayout, QLabel, QComboBox, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QMessageBox, QHBoxLayout, QDateEdit, QFrame)
from PyQt5.QtCore import Qt, QDate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_keuangan = []
        self.load_from_csv()
        self.init_ui()

    def format_rp(self, angka):
        return f"Rp {angka:,.0f}"

    def load_from_csv(self):
        try:
            with open('data_keuangan.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)
                self.data_keuangan = [{k: int(v) if k == 'jumlah' else v for k, v in row.items()} for row in reader]
        except FileNotFoundError:
            self.data_keuangan = []
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data: {str(e)}")

    def save_to_csv(self):
        try:
            with open('data_keuangan.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["tanggal", "kategori", "keterangan", "jumlah"])
                writer.writerows([[d["tanggal"], d["kategori"], d["keterangan"], d["jumlah"]] for d in self.data_keuangan])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan data: {str(e)}")

    def update_totals(self):
        pemasukan = sum(d["jumlah"] for d in self.data_keuangan if d["kategori"] == "Pemasukan")
        pengeluaran = sum(d["jumlah"] for d in self.data_keuangan if d["kategori"] == "Pengeluaran")
        saldo = pemasukan - pengeluaran
        
        self.label_pemasukan.setText(f"Total Pemasukan: {self.format_rp(pemasukan)}")
        self.label_pengeluaran.setText(f"Total Pengeluaran: {self.format_rp(pengeluaran)}")
        self.label_saldo.setText(f"Total Saldo: {self.format_rp(saldo)}")
        
        if saldo < 0:
            self.label_saldo.setStyleSheet("font: bold 18px Product Sans; padding: 15px; background-color: #ffebee; border: 1px solid #f44336; border-radius: 4px; color: #d32f2f;")
        else:
            self.label_saldo.setStyleSheet("font: bold 18px Product Sans; padding: 15px; background-color: #e8f5e8; border: 1px solid #4CAF50; border-radius: 4px;")

    def populate_table(self, filter_type=None):
        self.table.setRowCount(0)
        filtered_data = [d for d in self.data_keuangan if not filter_type or d["kategori"] == filter_type]
        for data in filtered_data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(data["tanggal"]))
            self.table.item(row, 0).setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, QTableWidgetItem(data["kategori"]))
            self.table.item(row, 1).setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, QTableWidgetItem(data["keterangan"]))
            self.table.item(row, 2).setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 3, QTableWidgetItem(self.format_rp(data["jumlah"])))
            self.table.item(row, 3).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.table.resizeColumnsToContents()
        self.table.setWordWrap(True)
        self.update_totals()

    def apply_filter(self):
        filter_text = self.combo_filter.currentText()
        filter_type = filter_text if filter_text != "Semua" else None
        self.populate_table(filter_type)

    def tambah_data(self):
        try:
            kategori = self.combo_kategori.currentText()
            tanggal = self.date_edit.date().toString("dd/MM/yyyy")
            keterangan = self.entry_keterangan.text()
            jumlah = int(self.entry_jumlah.text())

            if not keterangan or not kategori:
                QMessageBox.warning(self, "Peringatan", "Lengkapi semua data!")
                return

            new_data = {"tanggal": tanggal, "kategori": kategori, "keterangan": keterangan, "jumlah": jumlah}
            self.data_keuangan.append(new_data)
            self.save_to_csv()
            self.apply_filter()

            self.combo_kategori.setCurrentIndex(0)
            self.date_edit.setDate(QDate.currentDate())
            self.entry_keterangan.clear()
            self.entry_jumlah.clear()
        except ValueError:
            QMessageBox.critical(self, "Error", "Jumlah harus berupa angka!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def init_ui(self):
        self.setWindowTitle("FinKos")
        self.resize(1300, 1000)  
        self.setStyleSheet("""
            background-color: #f5f5f5; 
            QLabel { background-color: #f5f5f5; font-size: 12px; }
            QLineEdit, QComboBox, QDateEdit { 
            font-size: 26px; 
            padding: 20px; 
            border: 20px solid #aaa; 
            border-radius: 6px; 
            min-width: 250px;
}

            QTableWidget { 
                gridline-color: #ddd; font-size: 11px; 
                alternate-background-color: #f9f9f9; background-color: white;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)

        title_label = QLabel("Aplikasi Catatan Keuangan Sederhana 💸")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 40px; 
            font-weight: bold; 
            color: #2c3e50; 
            padding: 15px;
        """)
        main_layout.addWidget(title_label)

        frame_input = QFrame()
        input_layout = QGridLayout(frame_input)
        input_layout.setColumnStretch(1, 1)
        
        inputs = [
            ("Kategori:", QComboBox, ["Pemasukan", "Pengeluaran"], "combo_kategori"),
            ("Tanggal:", QDateEdit, None, "date_edit"),
            ("Keterangan:", QLineEdit, None, "entry_keterangan"),
            ("Jumlah:", QLineEdit, None, "entry_jumlah")
        ]
        
        for i, (label_text, widget_class, items, attr_name) in enumerate(inputs):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 20px; font-weight: bold;")  
            widget = widget_class()
            if items:
                widget.addItems(items)
            elif issubclass(widget_class, QDateEdit):
                widget.setDate(QDate.currentDate())
                widget.setDisplayFormat("dd/MM/yyyy")
                widget.setCalendarPopup(True)
            else:
                widget.setPlaceholderText(f"Masukkan {label_text.lower()}")
            setattr(self, attr_name, widget)
            input_layout.addWidget(label, i, 0)
            input_layout.addWidget(widget, i, 1)

        self.btn_tambah = QPushButton("Tambah Data")
        self.btn_tambah.setStyleSheet("background-color: #4CAF50; color: white; padding: 12px; font-weight: bold; font-size: 19px; border-radius: 4px;")  
        self.btn_tambah.clicked.connect(self.tambah_data)
        input_layout.addWidget(self.btn_tambah, 4, 0, 1, 2)
        main_layout.addWidget(frame_input)

        frame_filter = QFrame()
        filter_layout = QHBoxLayout(frame_filter)
        filter_label = QLabel("Filter:")
        filter_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        filter_layout.addWidget(filter_label)
        self.combo_filter = QComboBox()
        self.combo_filter.addItems(["Semua", "Pemasukan", "Pengeluaran"])
        self.combo_filter.currentIndexChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.combo_filter)
        filter_layout.addStretch()
        main_layout.addWidget(frame_filter)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Tanggal", "Kategori", "Keterangan", "Jumlah"])
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 120)  # Tetap
        self.table.setColumnWidth(1, 150)  # Tetap
        self.table.setColumnWidth(2, 550)  # Dibuat lebih lebar untuk ukuran baru
        self.table.setColumnWidth(3, 200)  # Dibuat sedikit lebih lebar
        main_layout.addWidget(self.table, stretch=1)

        frame_totals = QFrame()
        totals_layout = QHBoxLayout(frame_totals)
        totals_layout.setSpacing(20)
        totals_layout.setContentsMargins(0, 13, 0, 13)
        
        total_configs = [
            ("Total Pemasukan: Rp 0", "font: bold 18px Product Sans; padding: 15px; background-color: #e8f5e8; border: 1px solid #4CAF50; border-radius: 5px;", "label_pemasukan"),
            ("Total Pengeluaran: Rp 0", "font: bold 18px Product Sans; padding: 15px; background-color: #ffebee; border: 1px solid #f44336; border-radius: 5px; color: #d32f2f;", "label_pengeluaran"),
            ("Total Saldo: Rp 0", "font: bold 18px Product Sans; padding: 15px; background-color: #e8f5e8; border: 1px solid #4CAF50; border-radius: 5px;", "label_saldo")
        ]
        
        for text, style, attr_name in total_configs:
            label = QLabel(text)
            label.setStyleSheet(style)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(300)
            setattr(self, attr_name, label)
            totals_layout.addWidget(label)
        
        totals_layout.addStretch()
        totals_layout.addStretch()
        main_layout.addWidget(frame_totals, alignment=Qt.AlignHCenter)
        main_layout.addSpacing(10)

        self.populate_table()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())