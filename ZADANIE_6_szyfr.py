import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

class SteganografiaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganografia LSB")
        self.root.geometry("600x700")
        self.root.grid_columnconfigure(0, weight=1)

        self.DELIMITER = "#####"

        self.sciezka_szyfr = None
        self.sciezka_deszyfr = None

        tk.Label(root, text="--- UKRYJ WIADOMOŚĆ ---", font=("Helvetica", 16, "bold"), fg="#b30000").grid(row=0, column=0, pady=(20, 10))
        
        tk.Button(root, text="1. Wczytaj zdjęcie bazowe", command=self.wczytaj_dla_szyfrowania).grid(row=1, column=0, pady=5)
        
        self.lbl_potwierdzenie_szyfr = tk.Label(root, text="Nie wybrano pliku", fg="gray")
        self.lbl_potwierdzenie_szyfr.grid(row=2, column=0)

        tk.Label(root, text="2. Wpisz tajną wiadomość:").grid(row=3, column=0, sticky="w", padx=20, pady=(10,0))
        self.wejscie_tekst = tk.Entry(root)
        self.wejscie_tekst.grid(row=4, column=0, sticky="ew", padx=20, pady=5)

        tk.Button(root, text="3. Ukryj tekst i Zapisz jako...", command=self.ukryj_wiadomosc).grid(row=5, column=0, pady=15)

        tk.Label(root, text="--- ODCZYTAJ WIADOMOŚĆ ---", font=("Helvetica", 16, "bold"), fg="#0066cc").grid(row=6, column=0, pady=(30, 10))
        
        tk.Button(root, text="1. Wczytaj zdjęcie z wiadomością", command=self.wczytaj_dla_deszyfrowania).grid(row=7, column=0, pady=5)
        
        self.lbl_potwierdzenie_deszyfr = tk.Label(root, text="Nie wybrano pliku", fg="gray")
        self.lbl_potwierdzenie_deszyfr.grid(row=8, column=0)

        tk.Button(root, text="2. Ekstrakcja tajnych danych", command=self.odczytaj_wiadomosc).grid(row=9, column=0, pady=15)

        tk.Label(root, text="Odkryta wiadomość:").grid(row=10, column=0, sticky="w", padx=20)
        self.wyjscie_tekst = tk.Text(root, height=4)
        self.wyjscie_tekst.grid(row=11, column=0, sticky="ew", padx=20, pady=5)

    def wczytaj_dla_szyfrowania(self):
        sciezka = filedialog.askopenfilename(filetypes=[("Obrazy", "*.png;*.jpg;*.jpeg;*.bmp")])
        if sciezka:
            self.sciezka_szyfr = sciezka
            nazwa = os.path.basename(sciezka)
            self.lbl_potwierdzenie_szyfr.config(text=f"WYBRANO: {nazwa}", fg="green")

    def wczytaj_dla_deszyfrowania(self):
        sciezka = filedialog.askopenfilename(filetypes=[("Obrazy", "*.png;*.jpg;*.jpeg;*.bmp")])
        if sciezka:
            self.sciezka_deszyfr = sciezka
            nazwa = os.path.basename(sciezka)
            self.lbl_potwierdzenie_deszyfr.config(text=f"WYBRANO: {nazwa}", fg="green")

    def tekst_na_bity(self, tekst):
        return ''.join([format(ord(z), '08b') for z in tekst])

    def bity_na_tekst(self, bity):
        znaki = [chr(int(bity[i:i+8], 2)) for i in range(0, len(bity), 8)]
        return ''.join(znaki)

    def ukryj_wiadomosc(self):
        if not self.sciezka_szyfr:
            messagebox.showwarning("Błąd", "Wczytaj obraz bazowy!")
            return
        
        tekst = self.wejscie_tekst.get() + self.DELIMITER
        strumien_bitow = self.tekst_na_bity(tekst)

        obraz = Image.open(self.sciezka_szyfr).convert("RGB")
        piksele = obraz.load()
        szer, wys = obraz.size

        if len(strumien_bitow) > szer * wys:
            messagebox.showerror("Błąd", "Za krótki obraz na tak długą wiadomość!")
            return

        indeks = 0
        for y in range(wys):
            for x in range(szer):
                if indeks < len(strumien_bitow):
                    r, g, b = piksele[x, y]
                    r = (r & ~1) | int(strumien_bitow[indeks])
                    piksele[x, y] = (r, g, b)
                    indeks += 1

        sciezka_zapisu = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if sciezka_zapisu:
            obraz.save(sciezka_zapisu)
            messagebox.showinfo("Sukces", "Zapisano!")

    def odczytaj_wiadomosc(self):
        if not self.sciezka_deszyfr:
            messagebox.showwarning("Błąd", "Wczytaj obraz z wiadomością!")
            return

        obraz = Image.open(self.sciezka_deszyfr).convert("RGB")
        piksele = obraz.load()
        szer, wys = obraz.size

        odczytane_bity = ""
        caly_tekst = ""

        for y in range(wys):
            for x in range(szer):
                r, g, b = piksele[x, y]
                odczytane_bity += str(r & 1)

                if len(odczytane_bity) >= 8 and len(odczytane_bity) % 8 == 0:
                    znak = self.bity_na_tekst(odczytane_bity[-8:])
                    caly_tekst += znak
                    
                    if caly_tekst.endswith(self.DELIMITER):
                        wynik = caly_tekst[:-len(self.DELIMITER)]
                        self.wyjscie_tekst.delete(1.0, tk.END)
                        self.wyjscie_tekst.insert(tk.END, wynik)
                        return
                    
        messagebox.showinfo("Koniec", "Nie znaleziono ukrytej wiadomości.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganografiaApp(root)
    root.mainloop()