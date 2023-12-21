import os
import pandas as pd
from prettytable import PrettyTable
from .db_controller import Controller

class History:
    """
    A class used to represent a History.

    Attributes:
        - _controller (Controller): An instance of the Controller class.
        - _menu_controller (Controller): An instance of the Controller class.

    Methods:
        - __init__(): Initializes the History class.
        - show_history(): Display the transaction history.
    """
    def __init__(self) -> None:
        self._controller = Controller("data_transaksi")
        self._menu_controller = Controller("data_menu")

    def show_history(self):
        os.system("cls")
        data_all = self._controller.read_data()
        data_menu = self._menu_controller.read_data()
        if data_all.empty:
            print("Data masih kosong.")
        else:
            print("-"*47)
            print("|{:^45}|".format("Riwayat Transaksi"))
            print("-"*47)
            data_riwayat = data_all.groupby(by="Tanggal").agg({
                'No. Pembelian': 'first',
                'Total': 'sum'
            }).reset_index()

            table = PrettyTable()
            table.field_names = ["Tanggal Order", "No. Order", "Pemasukan"]
            table.align["Tanggal Order"] = "l"
            table.align["No. Order"] = "c"
            table.align["Pemasukan"] = "r"

            for row in data_riwayat.values:
                table.add_row(row)
            print(table)

            print("-"*47)
            print("|{:^32}|{:>12}|".format("Total Pemasukan", data_riwayat['Total'].sum()))
            print("-"*47)
            
            # Riwayat Transaksi per menu
            table_menu = PrettyTable()

            merge_data = pd.merge(data_all, data_menu, on="Nama Menu", how= 'right').fillna(0)
            merge_data.drop(columns=['No. Pembelian', 'Harga_x', 'Jenis Menu', 'Tanggal'], inplace=True)
            merge_data.rename(columns={'Harga_y': 'Harga', 'Stok': 'Sisa Persediaan'}, inplace=True)
            merge_data[['Jumlah', 'Total']] = merge_data[['Jumlah', 'Total']].astype('int64')

            merge_data = merge_data.groupby(by="Nama Menu").agg({
                'Jumlah': 'sum',
                'Total': 'sum',
                'Sisa Persediaan': 'first',
                'Harga': 'first'
            }).reset_index()

            table_menu.field_names = merge_data.columns
            for row in merge_data.values:
                table_menu.add_row(row)
            print(table_menu)

            print("-"*59)
            print("|{:^44}|{:>12}|".format("Total Pemasukan", merge_data['Total'].sum()))
            print("-"*59)
            input("Enter untuk lanjut")
