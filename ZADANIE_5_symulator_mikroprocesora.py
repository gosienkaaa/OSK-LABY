import tkinter as tk
from tkinter import ttk, messagebox


class RejestrWidget(tk.Frame):
    def __init__(self, parent, nazwa_rejestru="A", label_position="left"):
        super().__init__(parent, bg="white", bd=1, relief="solid")
        self.nazwa_rejestru = nazwa_rejestru
        self.label_position = label_position
        self.wartosc = 0

        self.bity = []
        self.zbuduj_widget()

    def zbuduj_widget(self):
        start_row = 1 if self.label_position == "top" else 0

        if self.label_position == "left":
            tk.Label(
                self,
                text=self.nazwa_rejestru,
                font=("Arial", 20, "bold"),
                bg="white"
            ).grid(row=start_row, column=0, rowspan=2, padx=(5, 15))
        else:
            tk.Label(
                self,
                text=self.nazwa_rejestru,
                font=("Arial", 14, "bold"),
                bg="white"
            ).grid(row=0, column=0, columnspan=18, pady=(0, 5))

        for i in range(16):
            var = tk.IntVar(value=0)
            self.bity.append(var)

            kol = i + 1
            padx_val = (2, 10) if i == 7 else 2

            rb1 = tk.Radiobutton(
                self,
                variable=var,
                value=1,
                bg="white",
                indicatoron=True
            )
            rb1.grid(row=start_row, column=kol, padx=padx_val)

            rb0 = tk.Radiobutton(
                self,
                variable=var,
                value=0,
                bg="white",
                indicatoron=True
            )
            rb0.grid(row=start_row + 1, column=kol, padx=padx_val)

        tk.Label(self, text="1", bg="white", font=("Arial", 10, "bold")).grid(
            row=start_row, column=17, padx=(8, 2)
        )
        tk.Label(self, text="0", bg="white", font=("Arial", 10, "bold")).grid(
            row=start_row + 1, column=17, padx=(8, 2)
        )

        tk.Label(self, text="15-bit", bg="white", font=("Arial", 10)).grid(
            row=start_row + 2, column=1, columnspan=2, sticky="w"
        )
        tk.Label(self, text="0-bit", bg="white", font=("Arial", 10)).grid(
            row=start_row + 2, column=15, columnspan=2, sticky="e"
        )

        # pole AH
        self.entry_high = tk.Entry(
            self,
            width=8,
            font=("Courier New", 11, "bold"),
            justify="center"
        )
        self.entry_high.grid(row=start_row + 3, column=5, columnspan=2, pady=4, padx=(3, 0))

        # pole AL
        self.entry_low = tk.Entry(
            self,
            width=8,
            font=("Courier New", 11, "bold"),
            justify="center"
        )
        self.entry_low.grid(row=start_row + 3, column=7, columnspan=2, pady=4, padx=(0, 3))

        # przycisk WPISZ po prawej
        tk.Button(
            self,
            text="WPISZ",
            width=7,
            command=self.wpisz_do_rejestru
        ).grid(row=start_row + 3, column=9, padx=(6,0))

        # podpisy AH AL
        if self.label_position == "top":
            left_label = "in H"
            right_label = "in L"
        else:
            left_label = f"{self.nazwa_rejestru}H"
            right_label = f"{self.nazwa_rejestru}L"

        tk.Label(self, text=left_label, bg="white", font=("Arial", 9)).grid(
            row=start_row + 4, column=5, columnspan=2
        )

        tk.Label(self, text=right_label, bg="white", font=("Arial", 9)).grid(
            row=start_row + 4, column=7, columnspan=2
        )

        if self.label_position == "top":
            left_label = "in H"
            right_label = "in L"
        else:
            left_label = f"{self.nazwa_rejestru}H"
            right_label = f"{self.nazwa_rejestru}L"

        tk.Label(self, text=left_label, bg="white", font=("Arial", 11)).grid(
            row=start_row + 5, column=3, sticky="w"
        )
        tk.Label(self, text=right_label, bg="white", font=("Arial", 11)).grid(
            row=start_row + 5, column=10, sticky="e"
        )

        self.odswiez_pola()

    def wpisz_do_rejestru(self):
        wartosc = 0
        for i in range(16):
            bit = self.bity[i].get()
            pozycja = 15 - i
            wartosc |= (bit << pozycja)

        self.wartosc = wartosc & 0xFFFF
        self.odswiez_pola()

    def ustaw_wartosc(self, wartosc):
        self.wartosc = wartosc & 0xFFFF
        self.odswiez_pola_i_bity()

    def pobierz_wartosc(self):
        return self.wartosc

    def odswiez_pola(self):
        high = (self.wartosc >> 8) & 0xFF
        low = self.wartosc & 0xFF

        self.entry_high.delete(0, tk.END)
        self.entry_high.insert(0, f"{high:08b}")

        self.entry_low.delete(0, tk.END)
        self.entry_low.insert(0, f"{low:08b}")

    def odswiez_bity(self):
        for i in range(16):
            pozycja = 15 - i
            bit = (self.wartosc >> pozycja) & 1
            self.bity[i].set(bit)

    def odswiez_pola_i_bity(self):
        self.odswiez_pola()
        self.odswiez_bity()


class Aplikacja:
    def __init__(self, root):
        self.root = root
        self.root.title("Symulator rejestrów i operacji")
        self.root.configure(bg="white")
        self.root.state("zoomed")

        self.lista_instrukcji = []
        self.aktualny_krok = 0

        self.zbuduj_gui()

    def zbuduj_gui(self):
        content_frame = tk.Frame(self.root, bg="white")
        content_frame.pack(fill="both", expand=True)

        top_frame = tk.Frame(content_frame, bg="white")
        top_frame.pack(fill="both", expand=True, pady=(20, 10))

        left_frame = tk.Frame(top_frame, bg="white")
        left_frame.pack(side="left", padx=(20, 40), anchor="n")

        right_frame = tk.Frame(top_frame, bg="white")
        right_frame.pack(side="left", padx=(0, 20), anchor="n")

        self.rejestr_A = RejestrWidget(left_frame, "A", label_position="left")
        self.rejestr_A.pack(pady=(0, 15), anchor="nw")

        self.rejestr_B = RejestrWidget(left_frame, "B", label_position="left")
        self.rejestr_B.pack(anchor="nw")

        self.rejestr_natychmiastowy = RejestrWidget(
            left_frame,
            "Argument dla trybu natychmiastowego",
            label_position="top"
        )
        self.rejestr_natychmiastowy.pack(pady=(30, 0), anchor="nw")

        self.rejestr_C = RejestrWidget(right_frame, "C", label_position="left")
        self.rejestr_C.pack(pady=(0, 15), anchor="nw")

        self.rejestr_D = RejestrWidget(right_frame, "D", label_position="left")
        self.rejestr_D.pack(anchor="nw")

        # pole programu pod rejestrem D
        program_frame = tk.Frame(right_frame, bg="white", bd=2, relief="groove")
        program_frame.pack(pady=(20, 0), anchor="nw", fill="x")

        tk.Label(
            program_frame,
            text="Program",
            font=("Arial", 13, "bold"),
            bg="white"
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.pole_programu = tk.Text(
            program_frame,
            width=45,
            height=10,
            font=("Courier New", 11),
            wrap="none"
        )
        self.pole_programu.pack(padx=10, pady=(0, 10))
        self.pole_programu.tag_configure("aktualna_linia", background="yellow")

        self.label_aktualna_instrukcja = tk.Label(
            program_frame,
            text="Aktualna instrukcja: brak programu",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="darkgreen"
        )
        self.label_aktualna_instrukcja.pack(anchor="w", padx=10, pady=(0, 10))

        operacje_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        operacje_frame.pack(fill="x", padx=20, pady=(0, 20))

        tk.Label(
            operacje_frame,
            text="Wykonywanie operacji na rejestrach",
            font=("Arial", 14, "bold"),
            bg="white"
        ).grid(row=0, column=0, columnspan=10, pady=(10, 15))

        tk.Label(operacje_frame, text="Rozkaz:", font=("Arial", 11, "bold"), bg="white").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(operacje_frame, text="Źródło:", font=("Arial", 11, "bold"), bg="white").grid(row=1, column=1, padx=10, pady=5)
        tk.Label(operacje_frame, text="Tryb:", font=("Arial", 11, "bold"), bg="white").grid(row=1, column=2, padx=10, pady=5)
        tk.Label(operacje_frame, text="Cel:", font=("Arial", 11, "bold"), bg="white").grid(row=1, column=3, padx=10, pady=5)

        self.combo_operacja = ttk.Combobox(
            operacje_frame,
            values=["MOV", "ADD", "SUB"],
            state="readonly",
            width=10
        )
        self.combo_operacja.grid(row=2, column=0, padx=10, pady=5)
        self.combo_operacja.set("MOV")

        self.combo_zrodlo = ttk.Combobox(
            operacje_frame,
            values=["A", "B", "C", "D"],
            state="readonly",
            width=10
        )
        self.combo_zrodlo.grid(row=2, column=1, padx=10, pady=5)
        self.combo_zrodlo.set("B")

        self.combo_tryb_zrodla = ttk.Combobox(
            operacje_frame,
            values=["Rejestrowy", "Natychmiastowy"],
            state="readonly",
            width=15
        )
        self.combo_tryb_zrodla.grid(row=2, column=2, padx=10, pady=5)
        self.combo_tryb_zrodla.set("Rejestrowy")
        self.combo_tryb_zrodla.bind("<<ComboboxSelected>>", self.zmien_tryb_zrodla)

        self.combo_cel = ttk.Combobox(
            operacje_frame,
            values=["A", "B", "C", "D"],
            state="readonly",
            width=10
        )
        self.combo_cel.grid(row=2, column=3, padx=10, pady=5)
        self.combo_cel.set("A")

        tk.Button(
            operacje_frame,
            text="WYKONAJ OPERACJĘ",
            font=("Arial", 11, "bold"),
            command=self.wykonaj_operacje,
            width=20
        ).grid(row=2, column=4, padx=10, pady=5)

        tk.Button(
            operacje_frame,
            text="WPISZ DO PROGRAMU",
            font=("Arial", 11, "bold"),
            command=self.wpisz_do_programu,
            width=20
        ).grid(row=2, column=5, padx=10, pady=5)

        tk.Button(
            operacje_frame,
            text="WYKONAJ KROK",
            font=("Arial", 11, "bold"),
            command=self.wykonaj_krok_programu,
            width=18
        ).grid(row=2, column=6, padx=10, pady=5)

        tk.Button(
            operacje_frame,
            text="WYKONAJ PROGRAM",
            font=("Arial", 11, "bold"),
            command=self.wykonaj_caly_program,
            width=18
        ).grid(row=2, column=7, padx=10, pady=5)

        tk.Button(
            operacje_frame,
            text="RESET PROGRAMU",
            font=("Arial", 11, "bold"),
            command=self.reset_programu,
            width=18
        ).grid(row=2, column=8, padx=10, pady=5)

        self.label_info = tk.Label(
            operacje_frame,
            text="",
            font=("Arial", 11),
            bg="white",
            fg="blue"
        )
        self.label_info.grid(row=3, column=0, columnspan=10, pady=(10, 10))

        self.rejestr_A.ustaw_wartosc(0)
        self.rejestr_B.ustaw_wartosc(0)
        self.rejestr_C.ustaw_wartosc(0)
        self.rejestr_D.ustaw_wartosc(0)
        self.rejestr_natychmiastowy.ustaw_wartosc(0)

    def zmien_tryb_zrodla(self, event=None):
        tryb = self.combo_tryb_zrodla.get()

        if tryb == "Natychmiastowy":
            self.combo_zrodlo.config(state="disabled")
        else:
            self.combo_zrodlo.config(state="readonly")

    def pobierz_widget_rejestru(self, nazwa):
        mapa = {
            "A": self.rejestr_A,
            "B": self.rejestr_B,
            "C": self.rejestr_C,
            "D": self.rejestr_D
        }
        return mapa[nazwa]

    def nazwa_na_assembler(self, nazwa):
        mapa = {
            "A": "AX",
            "B": "BX",
            "C": "CX",
            "D": "DX"
        }
        return mapa[nazwa]

    def wykonaj_operacje(self):
        operacja = self.combo_operacja.get()
        tryb_zrodla = self.combo_tryb_zrodla.get()
        nazwa_celu = self.combo_cel.get()

        if not operacja or not tryb_zrodla or not nazwa_celu:
            messagebox.showwarning("Brak danych", "Uzupełnij wszystkie pola.")
            return

        rejestr_cel = self.pobierz_widget_rejestru(nazwa_celu)
        wartosc_celu = rejestr_cel.pobierz_wartosc()

        if tryb_zrodla == "Rejestrowy":
            nazwa_zrodla = self.combo_zrodlo.get()
            if not nazwa_zrodla:
                messagebox.showwarning("Brak danych", "Wybierz rejestr źródłowy.")
                return

            rejestr_zrodlo = self.pobierz_widget_rejestru(nazwa_zrodla)
            wartosc_zrodla = rejestr_zrodlo.pobierz_wartosc()
            opis_zrodla = nazwa_zrodla
        else:
            wartosc_zrodla = self.rejestr_natychmiastowy.pobierz_wartosc()
            opis_zrodla = "IMM"

        if operacja == "MOV":
            wynik = wartosc_zrodla
        elif operacja == "ADD":
            wynik = (wartosc_celu + wartosc_zrodla) & 0xFFFF
        elif operacja == "SUB":
            wynik = (wartosc_celu - wartosc_zrodla) & 0xFFFF
        else:
            messagebox.showerror("Błąd", "Nieznana operacja.")
            return

        rejestr_cel.ustaw_wartosc(wynik)

        self.label_info.config(
            text=f"Wykonano: {operacja} {opis_zrodla} -> {nazwa_celu}    |    wynik zapisano do rejestru {nazwa_celu}"
        )

    def wpisz_do_programu(self):
        operacja = self.combo_operacja.get()
        tryb_zrodla = self.combo_tryb_zrodla.get()
        nazwa_celu = self.combo_cel.get()

        if not operacja or not tryb_zrodla or not nazwa_celu:
            messagebox.showwarning("Brak danych", "Uzupełnij pola operacji.")
            return

        cel_asm = self.nazwa_na_assembler(nazwa_celu)

        if tryb_zrodla == "Rejestrowy":
            nazwa_zrodla = self.combo_zrodlo.get()
            if not nazwa_zrodla:
                messagebox.showwarning("Brak danych", "Wybierz rejestr źródłowy.")
                return
            zrodlo_asm = self.nazwa_na_assembler(nazwa_zrodla)
            instrukcja = f"{operacja} {cel_asm}, {zrodlo_asm}"
        else:
            wartosc_imm = self.rejestr_natychmiastowy.pobierz_wartosc()
            instrukcja = f"{operacja} {cel_asm}, {wartosc_imm}"

        self.pole_programu.insert(tk.END, instrukcja + "\n")
        self.label_info.config(text=f"Dodano do programu: {instrukcja}")

    def zaladuj_program_z_pola(self):
        tekst = self.pole_programu.get("1.0", tk.END)
        linie = [linia.strip() for linia in tekst.splitlines() if linia.strip()]

        self.lista_instrukcji = linie
        self.aktualny_krok = 0
        self.odswiez_podswietlenie()
        self.aktualizuj_label_instrukcji()

    def wykonaj_instrukcje_tekstowa(self, instrukcja):
        czesci = instrukcja.strip().split(maxsplit=1)
        if len(czesci) != 2:
            raise ValueError("Niepoprawna składnia instrukcji.")

        operacja = czesci[0].upper()
        argumenty = [a.strip().upper() for a in czesci[1].split(",")]

        if len(argumenty) != 2:
            raise ValueError("Instrukcja musi mieć dwa argumenty.")

        cel = argumenty[0]
        zrodlo = argumenty[1]

        mapa_rejestrow = {
            "AX": self.rejestr_A,
            "BX": self.rejestr_B,
            "CX": self.rejestr_C,
            "DX": self.rejestr_D
        }

        if cel not in mapa_rejestrow:
            raise ValueError(f"Nieznany rejestr docelowy: {cel}")

        rejestr_cel = mapa_rejestrow[cel]
        wartosc_celu = rejestr_cel.pobierz_wartosc()

        if zrodlo in mapa_rejestrow:
            wartosc_zrodla = mapa_rejestrow[zrodlo].pobierz_wartosc()
        else:
            try:
                wartosc_zrodla = int(zrodlo)
            except ValueError:
                raise ValueError(f"Niepoprawny argument źródłowy: {zrodlo}")

        if operacja == "MOV":
            wynik = wartosc_zrodla
        elif operacja == "ADD":
            wynik = wartosc_celu + wartosc_zrodla
        elif operacja == "SUB":
            wynik = wartosc_celu - wartosc_zrodla
        else:
            raise ValueError(f"Nieznana instrukcja: {operacja}")

        wynik &= 0xFFFF
        rejestr_cel.ustaw_wartosc(wynik)

    def wykonaj_krok_programu(self):
        if not self.lista_instrukcji:
            self.zaladuj_program_z_pola()

        if not self.lista_instrukcji:
            messagebox.showwarning("Brak programu", "Pole programu jest puste.")
            return

        if self.aktualny_krok >= len(self.lista_instrukcji):
            messagebox.showinfo("Koniec programu", "Wszystkie instrukcje zostały już wykonane.")
            return

        instrukcja = self.lista_instrukcji[self.aktualny_krok]

        try:
            self.wykonaj_instrukcje_tekstowa(instrukcja)
            self.aktualny_krok += 1
            self.odswiez_podswietlenie()
            self.aktualizuj_label_instrukcji()
            self.label_info.config(text=f"Wykonano krok: {instrukcja}")
        except Exception as e:
            messagebox.showerror(
                "Błąd wykonania",
                f"Błąd w instrukcji nr {self.aktualny_krok + 1}:\n{instrukcja}\n\n{e}"
            )

    def wykonaj_caly_program(self):
        if not self.lista_instrukcji:
            self.zaladuj_program_z_pola()

        if not self.lista_instrukcji:
            messagebox.showwarning("Brak programu", "Pole programu jest puste.")
            return

        while self.aktualny_krok < len(self.lista_instrukcji):
            instrukcja = self.lista_instrukcji[self.aktualny_krok]
            try:
                self.wykonaj_instrukcje_tekstowa(instrukcja)
                self.aktualny_krok += 1
            except Exception as e:
                self.odswiez_podswietlenie()
                self.aktualizuj_label_instrukcji()
                messagebox.showerror(
                    "Błąd wykonania",
                    f"Błąd w instrukcji nr {self.aktualny_krok + 1}:\n{instrukcja}\n\n{e}"
                )
                return

        self.odswiez_podswietlenie()
        self.aktualizuj_label_instrukcji()
        self.label_info.config(text="Program wykonano do końca.")
        messagebox.showinfo("Gotowe", "Program został wykonany.")

    def reset_programu(self):
        self.aktualny_krok = 0
        self.lista_instrukcji = []
        self.odswiez_podswietlenie()
        self.aktualizuj_label_instrukcji()
        self.label_info.config(text="Zresetowano stan wykonywania programu.")

    def odswiez_podswietlenie(self):
        self.pole_programu.tag_remove("aktualna_linia", "1.0", tk.END)

        if self.lista_instrukcji and self.aktualny_krok < len(self.lista_instrukcji):
            nr_linii = self.znajdz_rzeczywista_linie(self.aktualny_krok)
            self.pole_programu.tag_add("aktualna_linia", f"{nr_linii}.0", f"{nr_linii}.end")

    def znajdz_rzeczywista_linie(self, indeks_instrukcji):
        tekst = self.pole_programu.get("1.0", tk.END).splitlines()
        licznik = -1
        for i, linia in enumerate(tekst, start=1):
            if linia.strip():
                licznik += 1
                if licznik == indeks_instrukcji:
                    return i
        return 1

    def aktualizuj_label_instrukcji(self):
        if not self.lista_instrukcji:
            self.label_aktualna_instrukcja.config(text="Aktualna instrukcja: brak programu")
        elif self.aktualny_krok >= len(self.lista_instrukcji):
            self.label_aktualna_instrukcja.config(text="Aktualna instrukcja: koniec programu")
        else:
            self.label_aktualna_instrukcja.config(
                text=f"Aktualna instrukcja: {self.aktualny_krok + 1}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = Aplikacja(root)
    root.mainloop()