import os
from modulekasir import *


def main():
    os.system("cls")
    print("Selamat Datang di Menu Restoran Laperpedia")
    print("Apa yang ingin Anda lakukan?")
    print("=" * 28)
    print("[1] Edit Data Menu Restoran")
    print("[2] Hitung Pembelian")
    print("[3] Lihat Daftar Pengunjung")
    print("[0] Exit")
    print("=" * 28)
    try:
        pilih_menu = int(input("Pilih menu >> "))

        if pilih_menu == 1:
            inputdata.menu()
            main()
        elif pilih_menu == 2:
            Transaction().transaction()
            main()
        elif pilih_menu == 3:
            History().show_history()
            main()
        elif pilih_menu == 0:
            exit()
        else:
            input("Input tidak valid! Tekan enter untuk kembali...")
            main()
    except ValueError:
        input("Input tidak valid! Tekan enter untuk kembali...")
        main()


main()
