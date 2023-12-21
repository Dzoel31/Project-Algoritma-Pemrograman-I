import os
from .db_controller import Controller

class InputData:
    """
    A class used to represent an InputData.

    Attributes:
        - _controller (Controller): An instance of the Controller class.

    Methods:
        - input_data(): Input data to the data file.
        - update_data(): Update data in the data file.
        - delete_data(): Delete data from the data file.
        - show_data(): Display data from the data file.
    """
    def __init__(self) -> None:
        self._controller = Controller("data_menu")
        self._columns_name = ["Nama Menu", "Jenis Menu", "Harga" , "Stok"]
    
    def add_data(self) -> None:
        '''
        Input data to the data file.
        
        Args:
            - nama_menu (str): The name of the menu.
            - jenis_menu (str): The type of the menu.
            - harga_menu (int): The price of the menu.
            - stok_menu (int): The stock of the menu.
        '''

        nama_menu = input("Masukkan nama menu: ")
        jenis_menu = input("Masukkan jenis [Makanan/Minuman]: ")
        harga_menu = input("Masukkan harga: ")
        stok_menu = input("Masukkan stok: ")

        if self._controller.convert_types(harga_menu, int):
            harga_menu = int(harga_menu)
        else:
            print("Harga harus berupa angka.")
            return
        self._controller.read_data(self._columns_name)
        data = [nama_menu, jenis_menu, harga_menu, stok_menu]

        self._controller.add_data(data)
        print("Data berhasil ditambahkan")
    
    def update_data(self) -> None:
        '''
        Update data in the data file.

        Args:
            - index (int): The index of the data to be updated.
            - nama_menu (str): The name of the menu.
            - jenis_menu (str): The type of the menu.
            - harga_menu (int): The price of the menu.
            - stok_menu (int): The stock of the menu.
        '''
        if self._controller.is_data_empty():
            print("Data masih kosong.")
            return
        
        self._controller.show_data()
        
        index = input("Masukkan nomor menu yang ingin diubah: ")
        nama_menu = input("Masukkan nama menu: ")
        jenis_menu = input("Masukkan jenis [Makanan/Minuman]: ")
        harga_menu = input("Masukkan harga: ")
        stok_menu = input("Masukkan stok: ")

        index = self._controller.convert_types(index, int)
        harga_menu = self._controller.convert_types(harga_menu, int)
        stok_menu = self._controller.convert_types(stok_menu, int)

        data = [nama_menu, jenis_menu, harga_menu, stok_menu]

        self._controller.update_data(index, data)
        print("Data berhasil diubah")

    def delete_data(self) -> None:
        '''
        Delete data from the data file.

        Args:
            - index (int): The index of the data to be deleted.
        '''
        if self._controller.is_data_empty():
            print("Data masih kosong.")

        
        self._controller.show_data()
        
        index = input("Masukkan nomor menu yang ingin dihapus: ")

        index = self._controller.convert_types(index, int)
    
        self._controller.delete_data(index)
        print("Data berhasil dihapus")

    def show_data(self) -> None:
        if self._controller.is_data_empty():
            print("Data masih kosong.")
        
        self._controller.show_data()

def menu():
    status= "Y"
    while status != "N":        
        os.system("cls")
        print("1. Tambah data")
        print("2. Ubah data")
        print("3. Hapus data")
        print("4. Tampilkan data")
        print("5. Keluar")
        print("------------------")
        menu = int(input("Pilih menu >>> "))

        if menu == 1:
            InputData().add_data()
        elif menu == 2:
            InputData().update_data()
        elif menu == 3:
            InputData().delete_data()
        elif menu == 4:
            InputData().show_data()
        elif menu == 5:
            return
        else:
            print("Menu tidak tersedia.")

        status = input("Apakah anda ingin melanjutkan? [Y/N]: ").upper()