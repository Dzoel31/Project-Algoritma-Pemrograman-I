import os
import pandas as pd
from .db_controller import Controller
from prettytable import PrettyTable


class Transaction:
    """
    A class used to represent a Transaction.

    Attributes:
        - _Transaction (Controller): An instance of the Controller class.
        - _data_menu (Controller): An instance of the Controller class.
        - _columns_name (list): A list of column names.

    Methods:
        - __init__(): Initializes the Transaction class.
        - transaction_date(): Get the current date and time.
        - transaction_change(): Calculate the change.
        - transaction(): Make a transaction.
    """

    def __init__(self) -> None:
        self._Transaction = Controller("data_transaksi")
        self._data_menu = Controller("data_menu")
        self._columns_name = [
            "No. Pembelian",
            "Nama Menu",
            "Harga",
            "Jumlah",
            "Total",
            "Tanggal"]

    def transaction_date(self):
        now = pd.Timestamp.now()
        date = now.strftime("%d-%m-%Y %H:%M:%S")
        return date

    def transaction_change(self, total, bayar):
        if bayar < total:
            print("Uang anda kurang")
            bayar = int(input("Bayar: "))
            self.transaction_change(total, bayar)
            return
        elif bayar == total:
            return 0
        else:
            kembalian = bayar - total
            return kembalian

    def transaction(self):
        data_transaksi = self._Transaction.read_data(self._columns_name)

        nomor_order = data_transaksi['No. Pembelian'].max()
        if pd.isna(nomor_order):
            nomor_order = 1
        else:
            nomor_order += 1

        timestamp = self.transaction_date()

        orders = pd.DataFrame(columns=self._columns_name)

        while True:
            os.system("cls")
            data_menu = self._data_menu.read_data()
            self._data_menu.show_data()
            print("=" * 15)
            menu, jumlah = input(
                "Masukkan menu dan jumlah yang ingin dibeli (pisahkan dengan koma): ").split(",")
            if data_menu['Nama Menu'].str.contains(menu).any():
                harga = data_menu.loc[data_menu['Nama Menu']
                                      == menu, 'Harga'].iloc[0]
                jumlah = self._data_menu.convert_types(jumlah, int)
                total_harga = harga * jumlah

                orders.loc[len(orders)] = [nomor_order, menu,
                                           harga, jumlah, total_harga, timestamp]

                # Update stok
                stok = data_menu.loc[data_menu['Nama Menu']
                                     == menu, 'Stok'].iloc[0]
                stok -= int(jumlah)
                row_index = data_menu[data_menu['Nama Menu'] == menu].index[0]
                self._data_menu.update_data(row_index, stok, 'Stok')
                tambah_menu = input("Tambah menu? (y/n): ").upper()
                if tambah_menu == "Y":
                    continue
                else:
                    break
            else:
                print("Menu tidak tersedia")
                continue

        print("\n{:^76}".format("Struk Pembelian"))
        print("-" * 76)

        table = PrettyTable()
        orders_to_display = orders.groupby(by=['No. Pembelian', 'Nama Menu']).aggregate({
            'Harga': 'first',
            'Jumlah': 'sum',
            'Total': 'sum',
            'Tanggal': 'first'
        }).reset_index()

        table.field_names = orders_to_display.columns
        for row in orders_to_display.values:
            table.add_row(row)
        print(table)
        print("-" * 76)

        total = orders_to_display['Total'].sum()
        print(f"Total harga: {total}")
        print("-" * 76)
        bayar = int(input("Bayar: "))
        kembalian = self.transaction_change(total, bayar)
        print(f"Kembalian: {kembalian}")
        print("=" * 76)

        save_orders = orders_to_display.values.tolist()
        self._Transaction.add_data(save_orders)
        input("Tekan enter untuk melanjutkan...")
