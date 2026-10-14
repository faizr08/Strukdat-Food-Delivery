"""Titik masuk aplikasi 2EZ4U (M1: Array vs LinkList).

  python3 app.py            memakai data/pesanan.csv
  python3 app.py <csv>      memakai berkas CSV lain
"""

import sys
import tkinter as tk
from frontend import ui


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else ui.CSV_BAWAAN
    jendela = tk.Tk()
    ui.buka(jendela, path)
    jendela.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
