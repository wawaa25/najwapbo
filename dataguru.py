from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk

class Data_Guru(Tk):
    def __init__(self):
        super().__init__()
        self.title("Registrasi Data Guru")
        self.geometry("850x600")

        # Koneksi ke database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="registrasi"
        )

        # Membuat kursor
        self.cursor = self.db.cursor()

        # Membuat dan menampilkan GUI
        self.tampilan_gui()

    def tampilan_gui(self):

        Label(self, text="Kode Guru").grid(row=0, column=0, padx=10, pady=10)
        self.kode_guru_entry = Entry(self, width=50)
        self.kode_guru_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(self, text="Nama Guru").grid(row=1, column=0, padx=10, pady=10)
        self.nama_guru_entry = Entry(self, width=50)
        self.nama_guru_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(self, text="Kelompok Guru").grid(row=2, column=0, padx=10, pady=10)
        self.kelompok_guru_entry = Entry(self, width=50)
        self.kelompok_guru_entry.grid(row=2, column=1, padx=10, pady=10)

        Label(self, text="Mata Pelajaran").grid(row=3, column=0, padx=10, pady=10)
        self.mata_pelajaran_entry = Text(self, width=37, height=5)
        self.mata_pelajaran_entry.grid(row=3, column=1, padx=10, pady=10)

        Button(self, text="Simpan Data",
        command=self.simpan_data).grid(row=4, column=0,
                                       columnspan=2, pady=10)

        # Menambahkan Treeview
        self.tree = ttk.Treeview(self, columns=("kode_guru", "nama_guru", "kelompok_guru", "mata_pelajaran"), show="headings")
        self.tree.heading("kode_guru", text="Kode Guru")
        self.tree.heading("nama_guru", text="Nama Guru")
        self.tree.heading("kelompok_guru", text="Kelompok Guru")
        self.tree.heading("mata_pelajaran", text="Mata Pelajaran")
        self.tree.grid(row=5, column=0, columnspan=8, pady=10, padx=10)

        # Menambahkan tombol refresh data
        Button(self, text="Refresh Data", command=self.tampilkan_data).grid(row=6, 
        column=0, columnspan=2, pady=10,padx=10)

        # Menambahkan tombol delete data
        Button(self, text="Delete Data", command=self.hapus_data).grid(row=6,
        column=1, columnspan=2, pady=10, padx=10)
        
        # Menambahkan tombol update data
        Button(self, text="Update Data", command=self.update_data).grid(row=6,column=2, columnspan=2, pady=10, padx=10)
        self.tampilkan_data()

    def simpan_data(self):
        kode_guru = self.kode_guru_entry.get()
        nama_guru = self.nama_guru_entry.get()
        kelompok_guru = self.kelompok_guru_entry.get()
        mata_pelajaran = self.mata_pelajaran_entry.get("1.0", END)

        query = "INSERT INTO guru (kode_guru, nama_guru, kelompok_guru, mata_pelajaran) VALUES (%s,%s, %s, %s)"
        values = (kode_guru, nama_guru, kelompok_guru, mata_pelajaran)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Sukses", "Data berhasil disimpan!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

        self.kode_guru_entry.delete(0, END)
        self.nama_guru_entry.delete(0, END)
        self.kelompok_guru_entry.delete(0, END)
        self.mata_pelajaran_entry.delete("1.0", END)

    def tampilkan_data(self):
        # Hapus data pada treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Ambil data dari database
        self.cursor.execute("SELECT * FROM guru")
        data = self.cursor.fetchall()

        # Masukkan data ke treeview
        for row in data:
            self.tree.insert("", "end", values=row)

    def update_data(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang akan diupdate.")
            return
            
        # Ambil data terpilih dari treeview
        data = self.tree.item(selected_item[0], 'values')

        # Tampilkan form update dengan data terpilih
        self.kode_guru_entry.insert(0, data[0])
        self.nama_guru_entry.insert(0, data[1])
        self.kelompok_guru_entry.insert(0, data[2])
        self._entry.insert("1.0", data[3])

        # Menambahkan tombol update di form
        Button(self, text="Update", command=lambda: self.proses_update(data[0])).grid(row=4, column=1, columnspan=2, pady=10)
            
    def proses_update(self, nis_to_update):
            kode_guru = self.kode_guru_entry.get()
            nama_guru = self.nama_guru_entry.get()
            kelompok_guru = self.kelompok_guru_entry.get()
            mata_pelajaran = self.mata_pelajaran_entry.get("1.0", END)

            query = "UPDATE guru SET kode guru=%s, nama guru=%s, kelompok guru=%s, mata pelajaran=%s WHERE nis=%s"
            values = (kode_guru, nama_guru, kelompok_guru, mata_pelajaran, nis_to_update)

            try:
                self.cursor.execute(query, values)
                self.db.commit()
                messagebox.showinfo("Sukses", "Data berhasil diupdate!")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

            # Bersihkan form setelah update
            self.kode_guru_entry.delete(0, END)
            self.nama_guru_entry.delete(0, END)
            self.kelompok_guru_entry.delete(0, END)
            self.mata_pelajaran_entry.delete("1.0", END)

            # Tampilkan kembali data setelah diupdate
            self.tampilkan_data()

    def hapus_data(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus.")
            return
        
        confirmation = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?")

        if confirmation:
            for item in selected_item:
                data = self.tree.item(item, 'values')
                kode_guru = data[0]
                query = "DELETE FROM guru WHERE kode_guru = %s"
                values = (kode_guru,)

                try:
                    self.cursor.execute(query, values)
                    self.db.commit()
                    messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                except Exception as e:
                    messagebox.showerror("Error", "Terjadi kesalahan: {str(e)}")
            self.tampilkan_data()

if __name__ == "__main__":
    app = Data_Guru()
    app.mainloop()