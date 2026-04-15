import tkinter as tk
from tkinter import messagebox
import re
import os

SLOWNIK_PLIK = "slownik.txt"

if not os.path.exists(SLOWNIK_PLIK):
    with open(SLOWNIK_PLIK, "w", encoding="utf-8") as f:
        f.write("kurcze\ncholera\nmotyła noga\n")

def wczytaj_slownik():
    try:
        with open(SLOWNIK_PLIK, "r", encoding="utf-8") as f:
            return [linia.strip().lower() for linia in f if linia.strip()]
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie można wczytać słownika: {e}")
        return []

def cenzoruj_tekst(tekst, slownik):
    ocenzurowany = tekst
    for slowo in slownik:
        pattern = re.compile(re.escape(slowo), re.IGNORECASE)
        ocenzurowany = pattern.sub(lambda m: '*' * len(m.group()), ocenzurowany)
    return ocenzurowany

def koduj_rs232(tekst):
    strumien_bitow = ""
    for znak in tekst:
        kod_ascii = ord(znak) & 0xFF
        bin_msb_lsb = format(kod_ascii, '08b')
        bin_lsb_msb = bin_msb_lsb[::-1]
        ramka = '0' + bin_lsb_msb + '11'
        strumien_bitow += ramka
    return strumien_bitow

def dekoduj_rs232(strumien_bitow):
    zdekodowany_tekst = ""
    for i in range(0, len(strumien_bitow), 11):
        ramka = strumien_bitow[i:i+11]
        if len(ramka) == 11:
            bity_danych_lsb = ramka[1:9]
            bity_danych_msb = bity_danych_lsb[::-1]
            znak = chr(int(bity_danych_msb, 2))
            zdekodowany_tekst += znak
    return zdekodowany_tekst

class RS232Symulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Symulator Transmisji RS232")
        self.root.geometry("600x650")
        self.slownik = wczytaj_slownik()
        
        self.root.grid_columnconfigure(0, weight=1)

        
        tk.Label(root, text="--- NADAJNIK ---", font=("Helvetica", 16, "bold"), fg="blue").grid(row=0, column=0, pady=(20, 10))
        
        tk.Label(root, text="Wpisz tekst do wysłania (ASCII):").grid(row=1, column=0, sticky="w", padx=20)
        self.wejscie_tekst = tk.Entry(root)
        self.wejscie_tekst.grid(row=2, column=0, sticky="ew", padx=20, pady=5)

        tk.Button(root, text="Wykoduj i Wyślij >>", command=self.nadaj_sygnal).grid(row=3, column=0, pady=15)

        tk.Label(root, text="Strumień bitów (1 Start(0) | 8 Danych LSB->MSB | 2 Stop(11)):").grid(row=4, column=0, sticky="w", padx=20)
        self.wyjscie_bity_nadajnik = tk.Text(root, height=4)
        self.wyjscie_bity_nadajnik.grid(row=5, column=0, sticky="ew", padx=20, pady=5)

        self.kanal_transmisyjny = ""

        tk.Label(root, text="--- ODBIORNIK ---", font=("Helvetica", 16, "bold"), fg="green").grid(row=6, column=0, pady=(30, 10))
        
        tk.Label(root, text="Odebrany strumień bitów:").grid(row=7, column=0, sticky="w", padx=20)
        self.wejscie_bity_odbiornik = tk.Text(root, height=4)
        self.wejscie_bity_odbiornik.grid(row=8, column=0, sticky="ew", padx=20, pady=5)

        tk.Label(root, text="Zdekodowany tekst:").grid(row=9, column=0, sticky="w", padx=20)
        self.wyjscie_tekst = tk.Entry(root)
        self.wyjscie_tekst.grid(row=10, column=0, sticky="ew", padx=20, pady=5)

    def nadaj_sygnal(self):
        surowy_tekst = self.wejscie_tekst.get()
        if not surowy_tekst:
            messagebox.showwarning("Puste pole", "Wpisz tekst do wysłania!")
            return

        tekst_do_wyslania = cenzoruj_tekst(surowy_tekst, self.slownik)
        strumien = koduj_rs232(tekst_do_wyslania)
        
        self.wyjscie_bity_nadajnik.delete(1.0, tk.END)
        self.wyjscie_bity_nadajnik.insert(tk.END, strumien)

        self.kanal_transmisyjny = strumien
        self.odbierz_sygnal()

    def odbierz_sygnal(self):
        strumien = self.kanal_transmisyjny
        
        self.wejscie_bity_odbiornik.delete(1.0, tk.END)
        self.wejscie_bity_odbiornik.insert(tk.END, strumien)

        zdekodowany_tekst = dekoduj_rs232(strumien)
        czysty_tekst = cenzoruj_tekst(zdekodowany_tekst, self.slownik)

        self.wyjscie_tekst.delete(0, tk.END)
        self.wyjscie_tekst.insert(0, czysty_tekst)

if __name__ == "__main__":
    root = tk.Tk()
    app = RS232Symulator(root)
    root.mainloop()