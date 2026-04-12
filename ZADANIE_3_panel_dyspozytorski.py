import time
import random
import tkinter as tk
from tkinter import messagebox
import psutil
import math

# =========================================================
# UŻYTKOWNICY
# =========================================================

uzytkownicy = {
    "admin": "admin"
}


# =========================================================
# DIAGNOSTYKA SYSTEMOWA KOMPUTERA
# =========================================================

def uzycie_CPU():
    return psutil.cpu_percent(interval=1) # Zmieniono na interval=1, aby uzyskać aktualne dane o obciążeniu CPU

def wykorzystanie_RAM():
    return psutil.virtual_memory().percent

def predkosc_CPU():
    cpu_freq = psutil.cpu_freq()
    if cpu_freq is not None:
        return cpu_freq.current
    return 0.0


# =========================================================
# URZĄDZENIA
# =========================================================

class Urzadzenie:
    def __init__(self, nazwa, stan="OFF"):
        self.nazwa = nazwa
        self.stan = stan

    def sprawdzenie_zalaczenia_urzadzenia(self):
        return self.stan


class Silnik(Urzadzenie):
    def __init__(self, nazwa, stan="ON"):
        super().__init__(nazwa, stan)
        self.temperatura = self.temperatura_startowa()
        self.obroty = self.obroty_startowe()

    def temperatura_startowa(self):
        if self.nazwa == "silnik":
            return random.uniform(45.0, 55.0)
        elif "pompa_chlodnicza" in self.nazwa:
            return random.uniform(22.0, 32.0)
        return random.uniform(25.0, 40.0)

    def obroty_startowe(self):
        if self.nazwa == "silnik":
            return random.uniform(1400.0, 1800.0)
        elif "pompa_chlodnicza" in self.nazwa:
            return random.uniform(1100.0, 1500.0)
        return 0.0

    def monitorowanie_temperatury(self):
        return self.temperatura

    def monitorowanie_obrotow(self):
        return self.obroty

    def aktualizuj_temperature(self, linia_dziala, intensywnosc_pracy=1.0):
        if self.stan != "ON":
            self.temperatura -= random.uniform(0.1, 0.3)
            self.obroty = 0.0
        else:
            if self.nazwa == "silnik":
                if linia_dziala:
                    self.obroty += random.uniform(-40, 80) * intensywnosc_pracy
                    self.temperatura += random.uniform(0.15, 0.45) * intensywnosc_pracy
                else:
                    self.obroty += random.uniform(-30, 20)
                    self.temperatura -= random.uniform(0.05, 0.15)
                self.obroty = max(900.0, min(self.obroty, 3000.0))

            elif "pompa_chlodnicza" in self.nazwa:
                if linia_dziala:
                    self.obroty += random.uniform(-30, 60) * intensywnosc_pracy
                    self.temperatura += random.uniform(0.15, 0.45) * intensywnosc_pracy
                else:
                    self.obroty += random.uniform(-20, 15)
                    self.temperatura -= random.uniform(0.05, 0.15)
                self.obroty = max(700.0, min(self.obroty, 2600.0))

        if self.nazwa == "silnik":
            self.temperatura = max(35.0, min(self.temperatura, 95.0))
        else:
            self.temperatura = max(18.0, min(self.temperatura, 75.0))

class Wentylator(Urzadzenie):
    def __init__(self, nazwa, stan="ON"):
        super().__init__(nazwa, stan)
        self.obroty_wentylatora = self.predkosc_wentylatora()

    def predkosc_wentylatora(self):
        if self.nazwa == "wentylator_chlodzenia":
            return random.uniform(1800.0, 2300.0)
        elif self.nazwa == "filtr_powietrza":
            return random.uniform(700.0, 1100.0)
        return 0.0

    def wydajnosc_wentylatora(self):
        if self.nazwa == "wentylator_chlodzenia":
            return self.obroty_wentylatora * 0.1
        elif self.nazwa == "filtr_powietrza":
            return self.obroty_wentylatora * 0.05
        return 0.0

    def aktualizuj_obroty(self, linia_dziala):
        if self.stan != "ON":
            self.obroty_wentylatora = 0.0
            return

        if self.nazwa == "wentylator_chlodzenia":
            if linia_dziala:
                self.obroty_wentylatora += random.uniform(-40, 60)
            else:
                self.obroty_wentylatora += random.uniform(-20, 20)
            self.obroty_wentylatora = max(1400.0, min(self.obroty_wentylatora, 3200.0))

        elif self.nazwa == "filtr_powietrza":
            if linia_dziala:
                self.obroty_wentylatora += random.uniform(-20, 25)
            else:
                self.obroty_wentylatora += random.uniform(-10, 10)
            self.obroty_wentylatora = max(600.0, min(self.obroty_wentylatora, 1500.0))


class LampkaStatusu(tk.Frame):
    def __init__(self, parent, podpis=""):
        super().__init__(parent, bg="white")
        self.canvas = tk.Canvas(self, width=34, height=34, bg="white", highlightthickness=0)
        self.canvas.pack()
        self.oval = self.canvas.create_oval(4, 4, 30, 30, fill="red", outline="gray30", width=2)

        if podpis:
            self.label = tk.Label(self, text=podpis, font=("Arial", 9), bg="white")
            self.label.pack()

    def ustaw_stan(self, stan):
        kolor = "green" if stan in ("ON", "zamknięte", "aktywne") else "red"
        self.canvas.itemconfig(self.oval, fill=kolor)


class PionowySlupek(tk.Frame):
    def __init__(self, parent, podpis="Parametr", min_val=0, max_val=100, jednostka=""):
        super().__init__(parent, bg="white")
        self.min_val = min_val
        self.max_val = max_val
        self.jednostka = jednostka
        self.podpis = podpis

        self.label_tytul = tk.Label(self, text=podpis, font=("Arial", 10, "bold"), bg="white")
        self.label_tytul.pack()

        self.canvas = tk.Canvas(self, width=60, height=180, bg="white", highlightthickness=0)
        self.canvas.pack()

        # obramowanie słupka
        self.canvas.create_rectangle(20, 20, 50, 180, outline="black", width=2)

        # segmenty tła
        self.canvas.create_rectangle(21, 140, 49, 179, fill="#4CAF50", outline="")
        self.canvas.create_rectangle(21, 100, 49, 139, fill="#CDDC39", outline="")
        self.canvas.create_rectangle(21, 60, 49, 99, fill="#FFC107", outline="")
        self.canvas.create_rectangle(21, 21, 49, 59, fill="#F44336", outline="")

        # wypełnienie dynamiczne
        self.fill_rect = self.canvas.create_rectangle(21, 179, 49, 179, fill="blue", outline="")

        self.label_wartosc = tk.Label(self, text=f"0 {jednostka}", font=("Arial", 10), bg="white")
        self.label_wartosc.pack()

    def aktualizuj(self, wartosc):
        wartosc = max(self.min_val, min(wartosc, self.max_val))
        procent = (wartosc - self.min_val) / (self.max_val - self.min_val)

        y_bottom = 179
        y_top = 20
        wysokosc = y_bottom - y_top
        nowy_y = y_bottom - (procent * wysokosc)

        # kolor dynamiczny
        if procent < 0.5:
            kolor = "green"
        elif procent < 0.75:
            kolor = "orange"
        else:
            kolor = "red"

        self.canvas.coords(self.fill_rect, 21, nowy_y, 49, y_bottom)
        self.canvas.itemconfig(self.fill_rect, fill=kolor)
        self.label_wartosc.config(text=f"{wartosc:.1f} {self.jednostka}")


class PoziomyPasek(tk.Frame):
    def __init__(self, parent, podpis="Parametr", min_val=0, max_val=100, jednostka=""):
        super().__init__(parent, bg="white")
        self.min_val = min_val
        self.max_val = max_val
        self.jednostka = jednostka

        self.label_tytul = tk.Label(self, text=podpis, font=("Arial", 10, "bold"), bg="white")
        self.label_tytul.pack(anchor="w")

        self.canvas = tk.Canvas(self, width=150, height=30, bg="white", highlightthickness=0)
        self.canvas.pack()

        # tło paska
        self.canvas.create_rectangle(10, 8, 160, 22, outline="black", width=1)
        self.canvas.create_rectangle(11, 9, 60, 21, fill="#4CAF50", outline="")
        self.canvas.create_rectangle(61, 9, 110, 21, fill="#FFC107", outline="")
        self.canvas.create_rectangle(111, 9, 159, 21, fill="#F44336", outline="")

        self.fill_rect = self.canvas.create_rectangle(11, 9, 11, 21, fill="green", outline="")

        self.label_wartosc = tk.Label(self, text=f"0 {jednostka}", font=("Arial", 10), bg="white")
        self.label_wartosc.pack(anchor="w")

    def aktualizuj(self, wartosc):
        wartosc = max(self.min_val, min(wartosc, self.max_val))
        procent = (wartosc - self.min_val) / (self.max_val - self.min_val)

        x_start = 11
        x_end = 159
        nowy_x = x_start + (x_end - x_start) * procent

        if procent < 0.5:
            kolor = "green"
        elif procent < 0.75:
            kolor = "orange"
        else:
            kolor = "red"

        self.canvas.coords(self.fill_rect, x_start, 9, nowy_x, 21)
        self.canvas.itemconfig(self.fill_rect, fill=kolor)
        self.label_wartosc.config(text=f"{wartosc:.1f} {self.jednostka}")


class PolkolistyWskaznik(tk.Frame):
    def __init__(self, parent, podpis="Obroty", min_val=0, max_val=3000, jednostka="RPM"):
        super().__init__(parent, bg="white")

        self.min_val = min_val
        self.max_val = max_val
        self.jednostka = jednostka

        self.szer = 220
        self.wys = 170
        self.cx = 110
        self.cy = 115
        self.r = 70
        self.r_igla = 58

        self.canvas = tk.Canvas(self, width=self.szer, height=self.wys, bg="white", highlightthickness=0)
        self.canvas.pack()

        def punkt_na_luku(kat_stopnie, promien):
            kat = math.radians(kat_stopnie)
            x = self.cx + promien * math.cos(kat)
            y = self.cy - promien * math.sin(kat)
            return x, y

        def narysuj_segment(kat_od, kat_do, kolor, grubosc=24, krok=3):
            punkty = []
            for kat in range(kat_od, kat_do - 1, -krok):
                punkty.extend(punkt_na_luku(kat, self.r))
            self.canvas.create_line(
                *punkty,
                fill=kolor,
                width=grubosc,
                smooth=True,
                capstyle=tk.ROUND
            )

        # szare tło półkola - GÓRA
        narysuj_segment(180, 0, "#d9d9d9", grubosc=24, krok=2)

        # kolorowe segmenty - GÓRA od lewej do prawej
        narysuj_segment(180, 126, "#1faa4a")
        narysuj_segment(126, 90, "#8ac926")
        narysuj_segment(90, 54, "#ffca3a")
        narysuj_segment(54, 27, "#ff924c")
        narysuj_segment(27, 0, "#e63946")

        # wewnętrzne jasne półkole
        punkty_wew = []
        for kat in range(180, -1, -3):
            punkty_wew.extend(punkt_na_luku(kat, 52))
        self.canvas.create_line(
            *punkty_wew,
            fill="#f2f2f2",
            width=16,
            smooth=True,
            capstyle=tk.ROUND
        )

        # podziałki
        for kat_stopnie in [180, 144, 108, 72, 36, 0]:
            x1, y1 = punkt_na_luku(kat_stopnie, 50)
            x2, y2 = punkt_na_luku(kat_stopnie, 82)
            self.canvas.create_line(x1, y1, x2, y2, fill="#b0b0b0", width=2)

        # igła
        self.igla = self.canvas.create_line(self.cx, self.cy, self.cx, self.cy - self.r_igla, width=4, fill="black")

        # środek
        self.canvas.create_oval(self.cx - 7, self.cy - 7, self.cx + 7, self.cy + 7,
                                fill="#333333", outline="black")

        self.label_podpis = tk.Label(self, text=podpis, font=("Arial", 10, "bold"), bg="white")
        self.label_podpis.pack()

        self.label_wartosc = tk.Label(self, text=f"0 {jednostka}", font=("Arial", 10), bg="white")
        self.label_wartosc.pack()

    def aktualizuj(self, wartosc):
        wartosc = max(self.min_val, min(wartosc, self.max_val))
        procent = (wartosc - self.min_val) / (self.max_val - self.min_val)

        kat_stopnie = 180 - (180 * procent)
        kat = math.radians(kat_stopnie)

        x1 = self.cx + self.r_igla * math.cos(kat)
        y1 = self.cy - self.r_igla * math.sin(kat)

        self.canvas.coords(self.igla, self.cx, self.cy, x1, y1)
        self.label_wartosc.config(text=f"{wartosc:.0f} {self.jednostka}")


class KafelekUrzadzenia(tk.Frame):
    def __init__(self, parent, nazwa, temp_min=0, temp_max=100, obroty_min=0, obroty_max=3000):
        super().__init__(parent, bg="white", bd=2, relief="groove")

        self.configure(padx=10, pady=10)

        # górny pasek: lampka + nazwa
        top = tk.Frame(self, bg="white")
        top.pack(fill="x", pady=(0, 10))

        self.lampka = LampkaStatusu(top, "")
        self.lampka.pack(side="left", padx=(0, 10))

        self.label_nazwa = tk.Label(
            top,
            text=nazwa,
            font=("Arial", 14, "bold"),
            bg="white",
            anchor="w"
        )
        self.label_nazwa.pack(side="left")

        # środek: temperatura + obroty
        middle = tk.Frame(self, bg="white")
        middle.pack()

        self.slupek_temp = PionowySlupek(
            middle,
            podpis="temperatura obudowy",
            min_val=temp_min,
            max_val=temp_max,
            jednostka="°C"
        )
        self.slupek_temp.pack(side="left", padx=6)

        self.wsk_obroty = PolkolistyWskaznik(
            middle,
            podpis="obroty",
            min_val=obroty_min,
            max_val=obroty_max,
            jednostka="RPM"
        )
        self.wsk_obroty.pack(side="left", padx=6)

    def aktualizuj(self, stan, temperatura, obroty):
        self.lampka.ustaw_stan(stan)
        self.slupek_temp.aktualizuj(temperatura)
        self.wsk_obroty.aktualizuj(obroty)


class KafelekWentylatora(tk.Frame):
    def __init__(self, parent, nazwa, wydajnosc_min=0, wydajnosc_max=350, obroty_min=0, obroty_max=3200):
        super().__init__(parent, bg="white", bd=2, relief="groove")
        self.configure(padx=10, pady=10)

        top = tk.Frame(self, bg="white")
        top.pack(fill="x", pady=(0, 10))

        self.lampka = LampkaStatusu(top, "")
        self.lampka.pack(side="left", padx=(0, 10))

        self.label_nazwa = tk.Label(
            top,
            text=nazwa,
            font=("Arial", 14, "bold"),
            bg="white",
            anchor="w"
        )
        self.label_nazwa.pack(side="left")

        middle = tk.Frame(self, bg="white")
        middle.pack()

        self.pasek_wydajnosci = PoziomyPasek(
            middle,
            podpis="wydajność",
            min_val=wydajnosc_min,
            max_val=wydajnosc_max,
            jednostka="m³/h"
        )
        self.pasek_wydajnosci.pack(side="left", padx=3, pady=8)

        self.wsk_obroty = PolkolistyWskaznik(
            middle,
            podpis="obroty",
            min_val=obroty_min,
            max_val=obroty_max,
            jednostka="RPM"
        )
        self.wsk_obroty.pack(side="left", padx=8)

    def aktualizuj(self, stan, wydajnosc, obroty):
        self.lampka.ustaw_stan(stan)
        self.pasek_wydajnosci.aktualizuj(wydajnosc)
        self.wsk_obroty.aktualizuj(obroty)


class KafelekStatusu(tk.Frame):
    def __init__(self, parent, nazwa):
        super().__init__(parent, bg="white", bd=2, relief="groove")
        self.configure(padx=12, pady=12)

        top = tk.Frame(self, bg="white")
        top.pack()

        self.lampka = LampkaStatusu(top, "")
        self.lampka.pack(side="left", padx=(0, 8))

        self.label_nazwa = tk.Label(
            top,
            text=nazwa,
            font=("Arial", 12, "bold"),
            bg="white"
        )
        self.label_nazwa.pack(side="left")

        self.label_stan = tk.Label(
            self,
            text="",
            font=("Arial", 11),
            bg="white"
        )
        self.label_stan.pack(pady=(8, 0))

    def aktualizuj(self, stan):
        self.lampka.ustaw_stan(stan)
        self.label_stan.config(text=f"Stan: {stan}")


from tkinter import ttk


class KafelekKPI(tk.Frame):
    def __init__(self, parent, tytul, wartosc="0", szer=220, wys=110):
        super().__init__(parent, bg="white", bd=2, relief="groove")
        self.configure(width=szer, height=wys)
        self.pack_propagate(False)

        self.label_tytul = tk.Label(
            self,
            text=tytul,
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333333"
        )
        self.label_tytul.pack(pady=(12, 6))

        self.label_wartosc = tk.Label(
            self,
            text=wartosc,
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#0b5394"
        )
        self.label_wartosc.pack(pady=(0, 10))

    def ustaw_wartosc(self, tekst, kolor="#0b5394"):
        self.label_wartosc.config(text=tekst, fg=kolor)


class PasekParametru(tk.Frame):
    def __init__(self, parent, tytul, max_val=100, jednostka="%"):
        super().__init__(parent, bg="white", bd=2, relief="groove")
        self.max_val = max_val
        self.jednostka = jednostka

        self.label_tytul = tk.Label(
            self,
            text=tytul,
            font=("Arial", 12, "bold"),
            bg="white"
        )
        self.label_tytul.pack(anchor="w", padx=10, pady=(10, 4))

        self.label_wartosc = tk.Label(
            self,
            text=f"0 {jednostka}",
            font=("Arial", 11),
            bg="white"
        )
        self.label_wartosc.pack(anchor="w", padx=10)

        self.progress = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
            length=320,
            maximum=max_val
        )
        self.progress.pack(fill="x", padx=10, pady=(8, 12))

    def ustaw_wartosc(self, wartosc, tekst=None):
        wartosc = max(0, min(wartosc, self.max_val))
        self.progress["value"] = wartosc
        if tekst is None:
            tekst = f"{wartosc:.1f} {self.jednostka}"
        self.label_wartosc.config(text=tekst)



# =========================================================
# PARAMETRY CHŁODZENIA
# =========================================================

PROG_WLACZENIA_POMPY2 = 40.0
PROG_WYLACZENIA_POMPY2 = 35.0


# urządzenia instalacji
zasilanie_glowne = Urzadzenie("zasilanie główne", "ON")
zasilanie_awaryjne = Urzadzenie("zasilanie awaryjne", "OFF")
drzwi_bezpieczenstwa = Urzadzenie("drzwi bezpieczeństwa", "zamknięte")
czujnik_obecnosci = Urzadzenie("czujnik obecności operatora", "aktywne")
naped_pneumatyczny = Urzadzenie("napęd pneumatyczny", "ON")

silnik = Silnik("silnik", "ON")
pompa_chlodnicza1 = Silnik("pompa_chlodnicza1", "ON")
pompa_chlodnicza2 = Silnik("pompa_chlodnicza2", "OFF")

wentylator1 = Wentylator("wentylator_chlodzenia", "ON")
wentylator2 = Wentylator("wentylator_chlodzenia", "OFF")
filtr_powietrza1 = Wentylator("filtr_powietrza", "ON")
filtr_powietrza2 = Wentylator("filtr_powietrza", "ON")


# =========================================================
# STAN PRODUKCJI
# =========================================================

linia_uruchomiona = False
czas_startu_linii = None
ostatnia_aktualizacja_produkcji = None

awaryjne_zatrzymanie = False
komunikat_awaryjny = ""

bazowa_wydajnosc_na_godzine = 120.0
mnoznik_predkosci_linii = 1.0

stan_produkcji = {
    "liczba_jednostek": 0.0,
    "czas_pracy_h": 0.0,
    "wydajnosc_procentowa": 0.0,
    "czas_cyklu_min": 0.0,
    "zuzycie_surowcow_kg": 0.0,
    "wadliwe_jednostki": 0,
    "odpady_procent": 0.0,
    "zuzycie_energii_kwh": 0.0,
    "wydajnosc_energetyczna": 0.0,
    "aktualna_wydajnosc_h": 0.0
}


def resetuj_stan_produkcji():
    for key in stan_produkcji:
        stan_produkcji[key] = 0.0 if isinstance(stan_produkcji[key], float) else 0


def czy_mozna_uruchomic_linie():
    if drzwi_bezpieczenstwa.stan != "zamknięte":
        return False, "Nie można uruchomić linii: drzwi bezpieczeństwa są otwarte."

    if czujnik_obecnosci.stan == "wykryto obecność":
        return False, "Nie można uruchomić linii: wykryto obecność operatora w strefie niebezpiecznej."

    if zasilanie_glowne.stan != "ON" and zasilanie_awaryjne.stan != "ON":
        return False, "Nie można uruchomić linii: brak zasilania głównego i awaryjnego."

    if naped_pneumatyczny.stan != "ON":
        return False, "Nie można uruchomić linii: napęd pneumatyczny jest wyłączony."

    return True, "Warunki startu spełnione."


def steruj_pompami_chlodniczymi():
    if pompa_chlodnicza1.temperatura > PROG_WLACZENIA_POMPY2 and pompa_chlodnicza2.stan == "OFF":
        pompa_chlodnicza2.stan = "ON"
        dodaj_zdarzenie(
            f"INFO: temperatura pompy chłodniczej 1 przekroczyła {PROG_WLACZENIA_POMPY2}°C. "
            f"Włączono pompę chłodniczą 2."
        )

    elif pompa_chlodnicza1.temperatura < PROG_WYLACZENIA_POMPY2 and pompa_chlodnicza2.stan == "ON":
        pompa_chlodnicza2.stan = "OFF"
        dodaj_zdarzenie(
            f"INFO: temperatura pompy chłodniczej 1 spadła poniżej {PROG_WYLACZENIA_POMPY2}°C. "
            f"Wyłączono pompę chłodniczą 2."
        )


def aktualizuj_urzadzenia():
    intensywnosc = mnoznik_predkosci_linii if linia_uruchomiona else 0.0

    # aktualizacja temperatury silnika
    silnik.aktualizuj_temperature(linia_uruchomiona, intensywnosc_pracy=max(intensywnosc, 0.5))

    # sterowanie wentylatorem 2 na podstawie temperatury silnika
    if silnik.temperatura > PROG_WLACZENIA_WENTYLATORA2 and wentylator2.stan == "OFF":
        wentylator2.stan = "ON"
        dodaj_zdarzenie("INFO: wysoka temperatura silnika - włączono wentylator 2")

    elif silnik.temperatura < PROG_WYLACZENIA_WENTYLATORA2 and wentylator2.stan == "ON":
        wentylator2.stan = "OFF"
        dodaj_zdarzenie("INFO: temperatura silnika spadła - wyłączono wentylator 2")

    # chłodzenie silnika przez wentylatory
    if wentylator1.stan == "ON":
        silnik.temperatura -= random.uniform(0.03, 0.10)

    if wentylator2.stan == "ON":
        silnik.temperatura -= random.uniform(0.20, 0.45)

    # ograniczenia temperatury silnika po chłodzeniu
    silnik.temperatura = max(35.0, min(silnik.temperatura, 95.0))

    # pozostałe urządzenia
    pompa_chlodnicza1.aktualizuj_temperature(linia_uruchomiona, intensywnosc_pracy=max(intensywnosc, 0.4))
    pompa_chlodnicza2.aktualizuj_temperature(linia_uruchomiona, intensywnosc_pracy=max(intensywnosc, 0.4))

    steruj_pompami_chlodniczymi()
    wentylator1.aktualizuj_obroty(linia_uruchomiona)

    # wentylator 2 aktualizuje obroty tylko gdy jest włączony
    if wentylator2.stan == "ON":
        wentylator2.aktualizuj_obroty(linia_uruchomiona)
    else:
        wentylator2.obroty_wentylatora = 0.0

    filtr_powietrza1.aktualizuj_obroty(linia_uruchomiona)
    filtr_powietrza2.aktualizuj_obroty(linia_uruchomiona)


def aktualizuj_stan_produkcji():
    global ostatnia_aktualizacja_produkcji

    if not linia_uruchomiona or czas_startu_linii is None:
        return

    teraz = time.time()

    if ostatnia_aktualizacja_produkcji is None:
        ostatnia_aktualizacja_produkcji = teraz
        return

    dt = teraz - ostatnia_aktualizacja_produkcji
    ostatnia_aktualizacja_produkcji = teraz

    stan_produkcji["czas_pracy_h"] = (teraz - czas_startu_linii) / 3600.0

    odchylenie = random.uniform(-5.0, 5.0)
    aktualna_wydajnosc = (bazowa_wydajnosc_na_godzine + odchylenie) * mnoznik_predkosci_linii
    aktualna_wydajnosc = max(40.0, aktualna_wydajnosc)

    stan_produkcji["aktualna_wydajnosc_h"] = aktualna_wydajnosc
    stan_produkcji["wydajnosc_procentowa"] = round((aktualna_wydajnosc / bazowa_wydajnosc_na_godzine) * 100, 1)
    stan_produkcji["czas_cyklu_min"] = round(60.0 / aktualna_wydajnosc, 2)

    przyrost_jednostek = aktualna_wydajnosc * (dt / 3600.0)
    stan_produkcji["liczba_jednostek"] += przyrost_jednostek

    stan_produkcji["zuzycie_surowcow_kg"] = round(stan_produkcji["liczba_jednostek"] * 0.5, 2)

    procent_brakow = random.uniform(1.0, 3.0)
    przewidywane_wadliwe = int(stan_produkcji["liczba_jednostek"] * procent_brakow / 100.0)
    stan_produkcji["wadliwe_jednostki"] = przewidywane_wadliwe

    if stan_produkcji["liczba_jednostek"] > 0:
        stan_produkcji["odpady_procent"] = round(
            (stan_produkcji["wadliwe_jednostki"] / stan_produkcji["liczba_jednostek"]) * 100.0, 2
        )

    liczba_aktywnych_pomp = 0
    if pompa_chlodnicza1.stan == "ON":
        liczba_aktywnych_pomp += 1
    if pompa_chlodnicza2.stan == "ON":
        liczba_aktywnych_pomp += 1

    moc_chwilowa_kw = random.uniform(18.0, 24.0) * mnoznik_predkosci_linii
    moc_chwilowa_kw += liczba_aktywnych_pomp * 1.5

    if silnik.temperatura > 80:
        moc_chwilowa_kw += 3.0

    stan_produkcji["zuzycie_energii_kwh"] += moc_chwilowa_kw * (dt / 3600.0)
    stan_produkcji["zuzycie_energii_kwh"] = round(stan_produkcji["zuzycie_energii_kwh"], 2)

    if stan_produkcji["zuzycie_energii_kwh"] > 0:
        stan_produkcji["wydajnosc_energetyczna"] = round(
            stan_produkcji["liczba_jednostek"] / stan_produkcji["zuzycie_energii_kwh"], 2
        )


def pobierz_dane_produkcji():
    return {
        "stan_linii": "URUCHOMIONA" if linia_uruchomiona else "ZATRZYMANA",
        "liczba_jednostek": int(stan_produkcji["liczba_jednostek"]),
        "czas_pracy_h": round(stan_produkcji["czas_pracy_h"], 2),
        "wydajnosc_procentowa": stan_produkcji["wydajnosc_procentowa"],
        "czas_cyklu_min": stan_produkcji["czas_cyklu_min"],
        "zuzycie_surowcow_kg": stan_produkcji["zuzycie_surowcow_kg"],
        "wadliwe_jednostki": stan_produkcji["wadliwe_jednostki"],
        "odpady_procent": stan_produkcji["odpady_procent"],
        "zuzycie_energii_kwh": stan_produkcji["zuzycie_energii_kwh"],
        "wydajnosc_energetyczna": stan_produkcji["wydajnosc_energetyczna"],
        "aktualna_wydajnosc_h": round(stan_produkcji["aktualna_wydajnosc_h"], 2)
    }


# =========================================================
# ALARMY I HISTORIA ZDARZEŃ
# =========================================================

aktywny_alarm = []
historia_zdarzen = []

PROG_TEMP_SILNIKA = 80.0
PROG_TEMP_POMPY = 60.0
PROG_MIN_OBROTY_WENTYLATORA = 1500.0
PROG_CPU = 85.0
PROG_WLACZENIA_WENTYLATORA2 = 60.0
PROG_WYLACZENIA_WENTYLATORA2 = 55.0
SZANSA_AWARII_WENTYLATORA2 = 0.01

SZANSA_AWARII_ZASILANIA = 0.02
SZANSA_OTWARCIA_DRZWI = 0.015
SZANSA_WYKRYCIA_OBECNOSCI = 0.015
CZAS_TRWANIA_ZDARZENIA_MS = 5000

def dodaj_zdarzenie(tresc):
    znacznik_czasu = time.strftime("%H:%M:%S")
    wpis = f"[{znacznik_czasu}] {tresc}"

    if not historia_zdarzen or historia_zdarzen[-1] != wpis:
        historia_zdarzen.append(wpis)

    if len(historia_zdarzen) > 50:
        historia_zdarzen.pop(0)

def przywroc_drzwi_do_normy():
    drzwi_bezpieczenstwa.stan = "zamknięte"
    dodaj_zdarzenie("INFO: drzwi bezpieczeństwa ponownie zamknięte.")

def przywroc_czujnik_obecnosci():
    czujnik_obecnosci.stan = "aktywne"
    dodaj_zdarzenie("INFO: strefa niebezpieczna jest pusta, czujnik wrócił do stanu normalnego.")

def przywroc_zasilanie_glowne():
    zasilanie_glowne.stan = "ON"
    zasilanie_awaryjne.stan = "OFF"
    dodaj_zdarzenie("INFO: przywrócono zasilanie główne, wyłączono zasilanie awaryjne.")


def napraw_naped_pneumatyczny():
    global aktywny_alarm

    naped_pneumatyczny.stan = "ON"

    aktywny_alarm = [
        alarm for alarm in aktywny_alarm
        if alarm != "Awaria napędu pneumatycznego"
    ]

    dodaj_zdarzenie("INFO: napęd pneumatyczny został naprawiony i ponownie uruchomiony.")

def zatrzymaj_linie_awaryjnie(powod):
    global linia_uruchomiona, ostatnia_aktualizacja_produkcji
    global awaryjne_zatrzymanie, komunikat_awaryjny

    if linia_uruchomiona:
        linia_uruchomiona = False
        ostatnia_aktualizacja_produkcji = None
        awaryjne_zatrzymanie = True
        komunikat_awaryjny = powod
        dodaj_zdarzenie(f"ALARM KRYTYCZNY: {powod}. Linia została zatrzymana.")

def sprawdz_i_obsluz_awarie():
    global aktywny_alarm, linia_uruchomiona, mnoznik_predkosci_linii
    nowe_alarmy = []

    mnoznik_predkosci_linii = 1.0

        # automatyczne zwolnienie linii przy wysokiej temperaturze silnika
    if silnik.temperatura > PROG_TEMP_SILNIKA and linia_uruchomiona:
        mnoznik_predkosci_linii = 0.7
        dodaj_zdarzenie("OSTRZEŻENIE: temperatura silnika jest wysoka. Zwolniono tempo pracy linii.")

    # losowa awaria wentylatora 2
    if wentylator2.stan == "ON" and random.random() < SZANSA_AWARII_WENTYLATORA2:
        wentylator2.stan = "OFF"
        wentylator2.obroty_wentylatora = 0.0
        nowe_alarmy.append("Awaria wentylatora 2")
        dodaj_zdarzenie("ALARM: losowa awaria wentylatora 2.")

    if silnik.temperatura > PROG_TEMP_SILNIKA:
        nowe_alarmy.append("Przekroczona temperatura silnika")
        wentylator1.stan = "ON"

        if wentylator2.stan == "ON":
            wentylator1.obroty_wentylatora = min(3200.0, wentylator1.obroty_wentylatora + 250)
            wentylator2.obroty_wentylatora = min(3200.0, wentylator2.obroty_wentylatora + 250)
        else:
            wentylator1.obroty_wentylatora = min(3200.0, wentylator1.obroty_wentylatora + 250)

        dodaj_zdarzenie("ALARM: temperatura silnika przekroczyła próg. Uruchomiono chłodzenie i ograniczono pracę linii.")

    pompa_alarm = False
    if pompa_chlodnicza1.temperatura > PROG_TEMP_POMPY:
        nowe_alarmy.append("Wysoka temperatura pompy chłodniczej 1")
        pompa_alarm = True

    if pompa_chlodnicza2.stan == "ON" and pompa_chlodnicza2.temperatura > PROG_TEMP_POMPY:
        nowe_alarmy.append("Wysoka temperatura pompy chłodniczej 2")
        pompa_alarm = True

    if pompa_alarm and linia_uruchomiona:
        mnoznik_predkosci_linii = 0.8
        dodaj_zdarzenie("OSTRZEŻENIE: wysoka temperatura pomp chłodniczych. Zwolniono tempo pracy linii.")

    if wentylator1.stan == "ON" and wentylator1.obroty_wentylatora < PROG_MIN_OBROTY_WENTYLATORA:
        nowe_alarmy.append("Zbyt niskie obroty wentylatora 1")
        dodaj_zdarzenie("ALARM: zbyt niskie obroty wentylatora 1.")

    if wentylator2.stan == "ON" and wentylator2.obroty_wentylatora < PROG_MIN_OBROTY_WENTYLATORA:
        nowe_alarmy.append("Zbyt niskie obroty wentylatora 2")
        dodaj_zdarzenie("ALARM: zbyt niskie obroty wentylatora 2.")

    if linia_uruchomiona and drzwi_bezpieczenstwa.stan != "zamknięte":
        nowe_alarmy.append("Otwarte drzwi bezpieczeństwa podczas pracy")
        zatrzymaj_linie_awaryjnie("Otwarto drzwi bezpieczeństwa")

        # 5. wykryto obecność w strefie niebezpiecznej -> stop linii
    if linia_uruchomiona and czujnik_obecnosci.stan == "wykryto obecność":
        nowe_alarmy.append("Wykryto obecność operatora w strefie niebezpiecznej")
        zatrzymaj_linie_awaryjnie("Wykryto obecność w strefie niebezpiecznej")

       # 6. awaria zasilania głównego
    if zasilanie_glowne.stan != "ON" and zasilanie_awaryjne.stan == "ON":
        nowe_alarmy.append("Awaria zasilania głównego - praca na zasilaniu awaryjnym")

    if zasilanie_glowne.stan != "ON" and zasilanie_awaryjne.stan != "ON":
        nowe_alarmy.append("Brak zasilania głównego i awaryjnego")
        zatrzymaj_linie_awaryjnie("Brak zasilania głównego i awaryjnego")

    cpu = uzycie_CPU()
    if cpu > PROG_CPU:
        nowe_alarmy.append("Wysokie obciążenie CPU komputera")
        dodaj_zdarzenie("OSTRZEŻENIE: obciążenie CPU przekroczyło bezpieczny próg.")

    if linia_uruchomiona and random.random() < 0.002:
        naped_pneumatyczny.stan = "OFF"
        nowe_alarmy.append("Awaria napędu pneumatycznego")
        zatrzymaj_linie_awaryjnie("Awaria napędu pneumatycznego")

    aktywny_alarm = list(dict.fromkeys(nowe_alarmy))


def symulacja_awarii():
    if not aktywny_alarm:
        return ["Brak aktywnych awarii"]
    return aktywny_alarm


# =========================================================
# PANEL DYSPOZYTORSKI
# =========================================================

class PanelDyspozytorski:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel dyspozytorski")
        self.root.state("zoomed")
        self.root.configure(bg="lightgray")

        self.aktualny_widok = None
        self.czy_pokazano_komunikat_awarii = False

        self.okno_potwierdzenia = None
        self.operator_potwierdzil_obecnosc = False
        self.interwal_sprawdzenia_ms = 60000
        self.czas_na_potwierdzenie_ms = 30000

        self.main_frame = tk.Frame(self.root, bg="lightgray")
        self.main_frame.pack(fill="both", expand=True)

        self.menu_frame = tk.Frame(self.main_frame, bg="#d9d9d9", width=280, bd=2, relief="solid")
        self.menu_frame.pack(side="left", fill="y")
        self.menu_frame.pack_propagate(False)

        self.content_outer = tk.Frame(self.main_frame, bg="white", bd=2, relief="solid")
        self.content_outer.pack(side="right", fill="both", expand=True)

        self.canvas_content = tk.Canvas(self.content_outer, bg="white", highlightthickness=0)
        self.scrollbar_y = tk.Scrollbar(self.content_outer, orient="vertical", command=self.canvas_content.yview)
        self.canvas_content.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_y.pack(side="right", fill="y")
        self.canvas_content.pack(side="left", fill="both", expand=True)

        self.content_frame = tk.Frame(self.canvas_content, bg="white")
        self.canvas_window = self.canvas_content.create_window((0, 0), window=self.content_frame, anchor="nw")

        def _on_frame_configure(event):
            self.canvas_content.configure(scrollregion=self.canvas_content.bbox("all"))

        def _on_canvas_configure(event):
            self.canvas_content.itemconfig(self.canvas_window, width=event.width)

        self.content_frame.bind("<Configure>", _on_frame_configure)
        self.canvas_content.bind("<Configure>", _on_canvas_configure)

        self.canvas_content.bind_all("<MouseWheel>", self._scroll_mousewheel)

        tk.Button(
            self.menu_frame, text="Stan urządzeń", font=("Arial", 14), height=2,
            command=self.pokaz_stan_urzadzen
        ).pack(fill="x", pady=2)

        tk.Button(
            self.menu_frame, text="Stan produkcji", font=("Arial", 14), height=2,
            command=self.pokaz_stan_produkcji
        ).pack(fill="x", pady=2)

        tk.Button(
            self.menu_frame, text="Awarie i komunikaty", font=("Arial", 14), height=2,
            command=self.pokaz_awarie
        ).pack(fill="x", pady=2)

        tk.Button(
            self.menu_frame, text="Stan komputera", font=("Arial", 14), height=2,
            command=self.pokaz_stan_komputera
        ).pack(fill="x", pady=2)

        self.btn_linia = tk.Button(
            self.menu_frame, text="Uruchom linię produkcyjną", font=("Arial", 14),
            height=2, bg="#b6e3b6", command=self.przelacz_linie
        )
        self.btn_linia.pack(fill="x", pady=(20, 2))

        tk.Button(
            self.menu_frame,
            text="Napraw napęd pneumatyczny",
            font=("Arial", 14),
            height=2,
            bg="#cfe2f3",
            command=self.napraw_naped
        ).pack(fill="x", pady=2)

        tk.Button(
            self.menu_frame, text="Wyloguj", font=("Arial", 14), height=2,
            bg="#f0b2b2", command=self.wyloguj
        ).pack(fill="x", pady=2)

        self.status_linii_label = tk.Label(
            self.menu_frame,
            text="Status linii: ZATRZYMANA",
            font=("Arial", 12, "bold"),
            bg="#d9d9d9",
            fg="red"
        )
        self.status_linii_label.pack(pady=20)

        self.pokaz_stan_urzadzen()
        self.petla_glowna_aktualizacji()
        self.root.after(self.interwal_sprawdzenia_ms, self.wyswietl_sprawdzenie_obecnosci)

    def _scroll_mousewheel(self, event):
        self.canvas_content.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def wyczysc_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def petla_glowna_aktualizacji(self):
                # losowa awaria zasilania głównego
        if zasilanie_glowne.stan == "ON" and random.random() < SZANSA_AWARII_ZASILANIA:
            zasilanie_glowne.stan = "OFF"
            zasilanie_awaryjne.stan = "ON"
            dodaj_zdarzenie("ALARM: awaria zasilania głównego. Załączono zasilanie awaryjne podtrzymujące pracę linii.")
            self.root.after(CZAS_TRWANIA_ZDARZENIA_MS, przywroc_zasilanie_glowne)

        # losowe otwarcie drzwi bezpieczeństwa
        if drzwi_bezpieczenstwa.stan == "zamknięte" and random.random() < SZANSA_OTWARCIA_DRZWI:
            drzwi_bezpieczenstwa.stan = "otwarte"
            dodaj_zdarzenie("ALARM KRYTYCZNY: drzwi bezpieczeństwa nie są zamknięte.")
            self.root.after(CZAS_TRWANIA_ZDARZENIA_MS, przywroc_drzwi_do_normy)

        # losowe wykrycie obecności w strefie niebezpiecznej
        if czujnik_obecnosci.stan == "aktywne" and random.random() < SZANSA_WYKRYCIA_OBECNOSCI:
            czujnik_obecnosci.stan = "wykryto obecność"
            dodaj_zdarzenie("ALARM KRYTYCZNY: czujnik obecności wykrył człowieka w strefie niebezpiecznej.")
            self.root.after(CZAS_TRWANIA_ZDARZENIA_MS, przywroc_czujnik_obecnosci)

        aktualizuj_urzadzenia()
        aktualizuj_stan_produkcji()
        sprawdz_i_obsluz_awarie()

        global awaryjne_zatrzymanie, komunikat_awaryjny

        if awaryjne_zatrzymanie and not self.czy_pokazano_komunikat_awarii:
            messagebox.showwarning(
                "Awaryjne zatrzymanie linii",
                f"Linia została zatrzymana awaryjnie.\n\nPowód: {komunikat_awaryjny}\n\n"
                f"Po usunięciu problemu należy ponownie uruchomić linię."
            )
            self.czy_pokazano_komunikat_awarii = True

        if not awaryjne_zatrzymanie:
            self.czy_pokazano_komunikat_awarii = False

        if self.aktualny_widok == "urzadzenia":
            self.odswiez_stan_urzadzen()
        elif self.aktualny_widok == "produkcja":
            self.odswiez_stan_produkcji()
        elif self.aktualny_widok == "awarie":
            self.odswiez_awarie()
        elif self.aktualny_widok == "komputer":
            self.odswiez_stan_komputera()

        self.aktualizuj_status_linii()
        self.root.after(1000, self.petla_glowna_aktualizacji)

    def aktualizuj_status_linii(self):
        if linia_uruchomiona:
            self.status_linii_label.config(text="Status linii: URUCHOMIONA", fg="green")
            self.btn_linia.config(text="Zatrzymaj linię produkcyjną", bg="#f3d48b")
        else:
            self.status_linii_label.config(text="Status linii: ZATRZYMANA", fg="red")
            self.btn_linia.config(text="Uruchom linię produkcyjną", bg="#b6e3b6")

    def przelacz_linie(self):
        global linia_uruchomiona, czas_startu_linii, ostatnia_aktualizacja_produkcji
        global awaryjne_zatrzymanie, komunikat_awaryjny

        if not linia_uruchomiona:
            mozna_uruchomic, komunikat = czy_mozna_uruchomic_linie()

            if not mozna_uruchomic:
                messagebox.showwarning("Brak możliwości uruchomienia", komunikat)
                return

            linia_uruchomiona = True

            # jeśli to pierwszy start -> ustaw początek i wyzeruj stan
            if czas_startu_linii is None and not awaryjne_zatrzymanie:
                czas_startu_linii = time.time()
                resetuj_stan_produkcji()

            # jeśli było zatrzymanie awaryjne -> nie resetuj produkcji
            elif awaryjne_zatrzymanie:
                # koryguj czas ostatniej aktualizacji, żeby nie doliczyło postoju jako pracy
                czas_startu_linii = time.time() - (stan_produkcji["czas_pracy_h"] * 3600.0)

            ostatnia_aktualizacja_produkcji = time.time()

            if awaryjne_zatrzymanie:
                dodaj_zdarzenie("INFO: operator ponownie uruchomił linię po zatrzymaniu awaryjnym.")
                messagebox.showinfo(
                    "Ponowne uruchomienie linii",
                    "Linia została ponownie uruchomiona po zatrzymaniu awaryjnym.\n"
                    "Parametry produkcji zostały zachowane."
                )
                awaryjne_zatrzymanie = False
                komunikat_awaryjny = ""
            else:
                dodaj_zdarzenie("INFO: operator uruchomił linię produkcyjną.")
                messagebox.showinfo("Linia produkcyjna", "Linia produkcyjna została uruchomiona.")
        else:
            linia_uruchomiona = False
            czas_startu_linii = None
            ostatnia_aktualizacja_produkcji = None
            awaryjne_zatrzymanie = False
            komunikat_awaryjny = ""
            resetuj_stan_produkcji()
            dodaj_zdarzenie("INFO: operator zatrzymał linię produkcyjną.")
            messagebox.showinfo("Linia produkcyjna", "Linia produkcyjna została zatrzymana.")

        self.aktualizuj_status_linii()


    def wyloguj(self):
        odpowiedz = messagebox.askyesno("Wylogowanie", "Czy na pewno chcesz się wylogować?")
        if odpowiedz:
            self.root.destroy()
            pokaz_okno_logowania()

    def napraw_naped(self):
        if naped_pneumatyczny.stan == "ON":
            messagebox.showinfo("Napęd pneumatyczny", "Napęd pneumatyczny działa poprawnie.")
            return

        napraw_naped_pneumatyczny()
        messagebox.showinfo(
            "Napęd pneumatyczny",
            "Napęd pneumatyczny został naprawiony.\nMożna ponownie uruchomić linię."
        )

        if self.aktualny_widok == "urzadzenia":
            self.odswiez_stan_urzadzen()

    def pokaz_stan_urzadzen(self):
        self.aktualny_widok = "urzadzenia"
        self.wyczysc_content()

        tk.Label(
            self.content_frame,
            text="Stan urządzeń",
            font=("Arial", 22, "bold"),
            bg="white"
        ).pack(pady=10)

        self.urzadzenia_main = tk.Frame(self.content_frame, bg="white")
        self.urzadzenia_main.pack(fill="both", expand=True, padx=10, pady=10)

        # siatka kafelków
        self.kafelek_silnik = KafelekUrzadzenia(
            self.urzadzenia_main,
            "Silnik",
            temp_min=35,
            temp_max=95,
            obroty_min=0,
            obroty_max=3000
        )
        self.kafelek_silnik.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

        self.kafelek_pompa1 = KafelekUrzadzenia(
            self.urzadzenia_main,
            "Pompa chłodnicza 1",
            temp_min=18,
            temp_max=75,
            obroty_min=0,
            obroty_max=2600
        )
        self.kafelek_pompa1.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

        self.kafelek_pompa2 = KafelekUrzadzenia(
            self.urzadzenia_main,
            "Pompa chłodnicza 2",
            temp_min=18,
            temp_max=75,
            obroty_min=0,
            obroty_max=2600
        )
        self.kafelek_pompa2.grid(row=0, column=2, padx=8, pady=8, sticky="nsew")

        self.kafelek_went1 = KafelekWentylatora(
            self.urzadzenia_main,
            "Wentylator 1",
            wydajnosc_min=0,
            wydajnosc_max=350,
            obroty_min=0,
            obroty_max=3200
        )
        self.kafelek_went1.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")

        self.kafelek_went2 = KafelekWentylatora(
            self.urzadzenia_main,
            "Wentylator 2",
            wydajnosc_min=0,
            wydajnosc_max=350,
            obroty_min=0,
            obroty_max=3200
        )
        self.kafelek_went2.grid(row=1, column=1, padx=8, pady=8, sticky="nsew")

            # ==========================================
    # SEKCJA POZOSTAŁYCH ELEMENTÓW - tylko lampki
    # ==========================================
        self.label_pozostale = tk.Label(
            self.urzadzenia_main,
            text="Pozostałe elementy",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        self.label_pozostale.grid(row=2, column=0, columnspan=3, pady=(15, 8), sticky="w")

        self.pozostale_frame = tk.Frame(self.urzadzenia_main, bg="white")
        self.pozostale_frame.grid(row=3, column=0, columnspan=3, sticky="w", pady=(0, 8))

        self.kafelek_zasilanie_glowne = KafelekStatusu(self.pozostale_frame, "Zasilanie główne")
        self.kafelek_zasilanie_glowne.grid(row=0, column=0, padx=8, pady=8, sticky="w")

        self.kafelek_zasilanie_awaryjne = KafelekStatusu(self.pozostale_frame, "Zasilanie awaryjne")
        self.kafelek_zasilanie_awaryjne.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        self.kafelek_drzwi = KafelekStatusu(self.pozostale_frame, "Drzwi bezpieczeństwa")
        self.kafelek_drzwi.grid(row=0, column=2, padx=8, pady=8, sticky="w")

        self.kafelek_czujnik = KafelekStatusu(self.pozostale_frame, "Czujnik obecności")
        self.kafelek_czujnik.grid(row=1, column=0, padx=8, pady=8, sticky="w")

        self.kafelek_naped = KafelekStatusu(self.pozostale_frame, "Napęd pneumatyczny")
        self.kafelek_naped.grid(row=1, column=1, padx=8, pady=8, sticky="w")


        self.opis_stanow = tk.Label(
            self.urzadzenia_main,
            text="",
            font=("Arial", 11),
            bg="white",
            justify="left"
        )
        self.opis_stanow.grid(row=4, column=0, columnspan=3, pady=8, sticky="w")

        for col in range(3):
            self.urzadzenia_main.grid_columnconfigure(col, weight=1)

        self.odswiez_stan_urzadzen()

    def odswiez_stan_urzadzen(self):
        if self.aktualny_widok != "urzadzenia":
            return

        self.kafelek_silnik.aktualizuj(
            silnik.stan,
            silnik.monitorowanie_temperatury(),
            silnik.monitorowanie_obrotow()
        )

        self.kafelek_pompa1.aktualizuj(
            pompa_chlodnicza1.stan,
            pompa_chlodnicza1.monitorowanie_temperatury(),
            pompa_chlodnicza1.monitorowanie_obrotow()
        )

        self.kafelek_pompa2.aktualizuj(
            pompa_chlodnicza2.stan,
            pompa_chlodnicza2.monitorowanie_temperatury(),
            pompa_chlodnicza2.monitorowanie_obrotow()
        )
    
        self.kafelek_went1.aktualizuj(
            wentylator1.stan,
            wentylator1.wydajnosc_wentylatora(),
            wentylator1.obroty_wentylatora
        )

        self.kafelek_went2.aktualizuj(
            wentylator2.stan,
            wentylator2.wydajnosc_wentylatora(),
            wentylator2.obroty_wentylatora
        )

        self.kafelek_zasilanie_glowne.aktualizuj(zasilanie_glowne.stan)
        self.kafelek_zasilanie_awaryjne.aktualizuj(zasilanie_awaryjne.stan)
        self.kafelek_drzwi.aktualizuj(drzwi_bezpieczenstwa.stan)
        self.kafelek_czujnik.aktualizuj(czujnik_obecnosci.stan)
        self.kafelek_naped.aktualizuj(naped_pneumatyczny.stan)

        tekst = (
            f"Zasilanie główne: {zasilanie_glowne.stan} | "
            f"Zasilanie awaryjne: {zasilanie_awaryjne.stan} | "
            f"Drzwi bezpieczeństwa: {drzwi_bezpieczenstwa.stan} | "
            f"Czujnik obecności: {czujnik_obecnosci.stan} | "
            f"Napęd pneumatyczny: {naped_pneumatyczny.stan}"
        )
        self.opis_stanow.config(text=tekst)


    def pokaz_stan_produkcji(self):
        self.aktualny_widok = "produkcja"
        self.wyczysc_content()

        tk.Label(
            self.content_frame,
            text="Stan produkcji",
            font=("Arial", 22, "bold"),
            bg="white"
        ).pack(pady=10)

        self.produkcja_main = tk.Frame(self.content_frame, bg="white")
        self.produkcja_main.pack(fill="both", expand=True, padx=10, pady=10)

        # =========================
        # 1. DUŻY KAFEL STATUSU LINII
        # =========================
        self.kafelek_stan_linii = KafelekKPI(
            self.produkcja_main,
            "Stan linii",
            "ZATRZYMANA",
            szer=320,
            wys=120
        )
        self.kafelek_stan_linii.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # =========================
        # 2. KAFELKI KPI
        # =========================
        self.kpi_frame = tk.Frame(self.produkcja_main, bg="white")
        self.kpi_frame.grid(row=1, column=0, columnspan=2, sticky="w")

        self.kpi_wydajnosc = KafelekKPI(self.kpi_frame, "Aktualna wydajność", "0 szt./h")
        self.kpi_wydajnosc.grid(row=0, column=0, padx=4, pady=8)

        self.kpi_liczba = KafelekKPI(self.kpi_frame, "Liczba jednostek", "0")
        self.kpi_liczba.grid(row=0, column=1, padx=8, pady=8)

        self.kpi_czas = KafelekKPI(self.kpi_frame, "Czas pracy", "0.0 h")
        self.kpi_czas.grid(row=0, column=2, padx=8, pady=8)

        self.kpi_energia = KafelekKPI(self.kpi_frame, "Zużycie energii", "0.0 kWh")
        self.kpi_energia.grid(row=0, column=3, padx=8, pady=8)

        # =========================
        # 3. PASKI POSTĘPU
        # =========================
        self.paski_frame = tk.Frame(self.produkcja_main, bg="white")
        self.paski_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))

        self.pasek_wydajnosc = PasekParametru(
            self.paski_frame,
            "Wydajność procentowa",
            max_val=150,
            jednostka="%"
        )
        self.pasek_wydajnosc.grid(row=0, column=0, padx=10, pady=8, sticky="w")

        self.pasek_odpady = PasekParametru(
            self.paski_frame,
            "Odpady",
            max_val=100,
            jednostka="%"
        )
        self.pasek_odpady.grid(row=1, column=0, padx=10, pady=8, sticky="w")

        # =========================
        # 4. SEKCJA SZCZEGÓŁÓW
        # =========================
        szczegoly_box = tk.LabelFrame(
            self.produkcja_main,
            text="Szczegóły",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        szczegoly_box.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=15)

        self.label_czas_cyklu = tk.Label(szczegoly_box, font=("Arial", 12), bg="white")
        self.label_czas_cyklu.pack(anchor="w", pady=2)

        self.label_surowce = tk.Label(szczegoly_box, font=("Arial", 12), bg="white")
        self.label_surowce.pack(anchor="w", pady=2)

        self.label_wadliwe = tk.Label(szczegoly_box, font=("Arial", 12), bg="white")
        self.label_wadliwe.pack(anchor="w", pady=2)

        self.label_wydajnosc_energetyczna = tk.Label(szczegoly_box, font=("Arial", 12), bg="white")
        self.label_wydajnosc_energetyczna.pack(anchor="w", pady=2)

        self.odswiez_stan_produkcji()

    
    def odswiez_stan_produkcji(self):
        if self.aktualny_widok != "produkcja":
            return

        dane = pobierz_dane_produkcji()

        # =========================
        # STAN LINII
        # =========================
        if dane["stan_linii"] == "URUCHOMIONA":
            self.kafelek_stan_linii.ustaw_wartosc("URUCHOMIONA", kolor="green")
        else:
            self.kafelek_stan_linii.ustaw_wartosc("ZATRZYMANA", kolor="red")

        # =========================
        # KPI
        # =========================
        self.kpi_wydajnosc.ustaw_wartosc(f'{dane["aktualna_wydajnosc_h"]} szt./h')
        self.kpi_liczba.ustaw_wartosc(f'{dane["liczba_jednostek"]}')
        self.kpi_czas.ustaw_wartosc(f'{dane["czas_pracy_h"]} h')
        self.kpi_energia.ustaw_wartosc(f'{dane["zuzycie_energii_kwh"]} kWh')

        # =========================
        # PASKI
        # =========================
        self.pasek_wydajnosc.ustaw_wartosc(
            dane["wydajnosc_procentowa"],
            tekst=f'{dane["wydajnosc_procentowa"]} %'
        )

        self.pasek_odpady.ustaw_wartosc(
            dane["odpady_procent"],
            tekst=f'{dane["odpady_procent"]} %'
        )

        # =========================
        # SZCZEGÓŁY
        # =========================
        self.label_czas_cyklu.config(text=f'Czas cyklu: {dane["czas_cyklu_min"]} min')
        self.label_surowce.config(text=f'Zużycie surowców: {dane["zuzycie_surowcow_kg"]} kg')
        self.label_wadliwe.config(text=f'Wadliwe jednostki: {dane["wadliwe_jednostki"]}')
        self.label_wydajnosc_energetyczna.config(
            text=f'Wydajność energetyczna maszyn: {dane["wydajnosc_energetyczna"]}'
        )

    def pokaz_awarie(self):
        self.aktualny_widok = "awarie"
        self.wyczysc_content()

        tk.Label(
            self.content_frame, text="Awarie i komunikaty",
            font=("Arial", 22, "bold"), bg="white", fg="red"
        ).pack(pady=20)

        tk.Label(
            self.content_frame, text="Aktywne alarmy:",
            font=("Arial", 14, "bold"), bg="white"
        ).pack(anchor="w", padx=20, pady=(10, 5))

        self.awarie_frame = tk.Frame(self.content_frame, bg="white")
        self.awarie_frame.pack(fill="x", padx=20)

        tk.Label(
            self.content_frame, text="Historia zdarzeń:",
            font=("Arial", 14, "bold"), bg="white"
        ).pack(anchor="w", padx=20, pady=(20, 5))

        self.historia_frame = tk.Frame(self.content_frame, bg="white")
        self.historia_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.odswiez_awarie()

    def odswiez_awarie(self):
        if self.aktualny_widok != "awarie":
            return
        if not hasattr(self, "awarie_frame"):
            return

        for widget in self.awarie_frame.winfo_children():
            widget.destroy()

        for widget in self.historia_frame.winfo_children():
            widget.destroy()

        awarie = symulacja_awarii()

        for tekst in awarie:
            kolor = "green" if tekst == "Brak aktywnych awarii" else "red"
            tk.Label(
                self.awarie_frame, text=tekst, font=("Arial", 13),
                bg="white", fg=kolor
            ).pack(anchor="w", pady=2)

        if historia_zdarzen:
            for wpis in reversed(historia_zdarzen[-12:]):
                tk.Label(
                    self.historia_frame, text=wpis, font=("Arial", 11),
                    bg="white", anchor="w", justify="left"
                ).pack(anchor="w", pady=1)
        else:
            tk.Label(
                self.historia_frame, text="Brak zdarzeń.",
                font=("Arial", 11), bg="white"
            ).pack(anchor="w", pady=1)


    def pokaz_stan_komputera(self):
        self.aktualny_widok = "komputer"
        self.wyczysc_content()

        tk.Label(
            self.content_frame,
            text="Stan komputera",
            font=("Arial", 22, "bold"),
            bg="white"
        ).pack(pady=20)

        main = tk.Frame(self.content_frame, bg="white")
        main.pack(padx=20, pady=20, anchor="w")

        # ======================
        # CPU
        # ======================
        tk.Label(main, text="Użycie CPU", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")

        self.cpu_bar = ttk.Progressbar(main, length=350, maximum=100)
        self.cpu_bar.pack(pady=5)

        self.label_cpu = tk.Label(main, font=("Arial", 11), bg="white")
        self.label_cpu.pack(anchor="w", pady=(0,15))

        # ======================
        # RAM
        # ======================
        tk.Label(main, text="Użycie RAM", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")

        self.ram_bar = ttk.Progressbar(main, length=350, maximum=100)
        self.ram_bar.pack(pady=5)

        self.label_ram = tk.Label(main, font=("Arial", 11), bg="white")
        self.label_ram.pack(anchor="w", pady=(0,15))

        # ======================
        # CPU SPEED
        # ======================
        tk.Label(main, text="Prędkość CPU", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")

        self.label_cpu_speed = tk.Label(
            main,
            font=("Arial", 18, "bold"),
            fg="#0b5394",
            bg="white"
        )
        self.label_cpu_speed.pack(anchor="w", pady=5)

        self.odswiez_stan_komputera()


    def odswiez_stan_komputera(self):
        if self.aktualny_widok != "komputer":
            return

        cpu = uzycie_CPU()
        ram = wykorzystanie_RAM()
        cpu_speed = predkosc_CPU()

        self.cpu_bar["value"] = cpu
        self.ram_bar["value"] = ram

        self.label_cpu.config(text=f"{cpu:.1f} %")
        self.label_ram.config(text=f"{ram:.1f} %")
        self.label_cpu_speed.config(text=f"{cpu_speed:.0f} MHz")

    def wyswietl_sprawdzenie_obecnosci(self):
        if self.okno_potwierdzenia is not None and self.okno_potwierdzenia.winfo_exists():
            return

        self.operator_potwierdzil_obecnosc = False

        self.okno_potwierdzenia = tk.Toplevel(self.root)
        self.okno_potwierdzenia.title("Sprawdzenie obecności operatora")
        self.okno_potwierdzenia.geometry("450x200")
        self.okno_potwierdzenia.resizable(False, False)
        self.okno_potwierdzenia.grab_set()
        self.okno_potwierdzenia.focus_force()

        tk.Label(
            self.okno_potwierdzenia,
            text="Potwierdź obecność operatora",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        tk.Label(
            self.okno_potwierdzenia,
            text="Naciśnij klawisz Enter w ciągu 30 sekund.",
            font=("Arial", 12)
        ).pack(pady=10)

        tk.Label(
            self.okno_potwierdzenia,
            text="Brak potwierdzenia spowoduje alarm i wylogowanie.",
            font=("Arial", 11),
            fg="red"
        ).pack(pady=5)

        self.okno_potwierdzenia.bind("<Return>", self.potwierdz_obecnosc_klawiszem)

        self.root.after(self.czas_na_potwierdzenie_ms, self.sprawdz_brak_potwierdzenia)

    def potwierdz_obecnosc_klawiszem(self, event=None):
        self.operator_potwierdzil_obecnosc = True
        dodaj_zdarzenie("INFO: operator potwierdził obecność.")

        if self.okno_potwierdzenia is not None and self.okno_potwierdzenia.winfo_exists():
            self.okno_potwierdzenia.destroy()

        self.okno_potwierdzenia = None
        self.root.after(self.interwal_sprawdzenia_ms, self.wyswietl_sprawdzenie_obecnosci)

    def sprawdz_brak_potwierdzenia(self):
        if self.operator_potwierdzil_obecnosc:
            return

        if self.okno_potwierdzenia is not None and self.okno_potwierdzenia.winfo_exists():
            self.okno_potwierdzenia.destroy()

        self.okno_potwierdzenia = None
        self.uruchom_alarm_i_wyloguj()

    def uruchom_alarm_i_wyloguj(self):
        dodaj_zdarzenie("ALARM KRYTYCZNY: brak potwierdzenia obecności operatora.")
        messagebox.showwarning(
            "ALARM",
            "Brak potwierdzenia obecności operatora przez 30 sekund.\n"
            "Operator zostanie wylogowany z systemu."
        )

        self.root.destroy()
        pokaz_okno_logowania()


# =========================================================
# LOGOWANIE
# =========================================================

def otworz_panel_dyspozytorski():
    panel = tk.Tk()
    PanelDyspozytorski(panel)
    panel.mainloop()


def pokaz_okno_logowania():
    okno_logowania = tk.Tk()
    okno_logowania.title("Logowanie")
    okno_logowania.geometry("600x400")
    okno_logowania.config(bg="lightblue")

    def sprawdz_logowanie():
        login = entry_login.get()
        haslo = entry_haslo.get()

        if login in uzytkownicy and uzytkownicy[login] == haslo:
            messagebox.showinfo("Sukces", "Zalogowano pomyślnie!")
            okno_logowania.destroy()
            otworz_panel_dyspozytorski()
        else:
            messagebox.showerror("Błąd", "Niepoprawny login lub hasło!")
            entry_haslo.delete(0, tk.END)

    def utworz_konto():
        def zapisz_konto():
            login = entry_login_new.get().strip()
            haslo = entry_haslo_new.get().strip()
            confirm_haslo = entry_confirm_haslo.get().strip()
            admin_login = entry_admin_login.get().strip()
            admin_haslo = entry_admin_haslo.get().strip()

            if admin_login != "admin" or admin_haslo != "admin":
                messagebox.showerror("Błąd", "Niepoprawny login lub hasło administratora!")
                return

            if not login or not haslo:
                messagebox.showerror("Błąd", "Login i hasło nie mogą być puste!")
                return

            if login in uzytkownicy:
                messagebox.showerror("Błąd", "Taki login już istnieje!")
                return

            if haslo != confirm_haslo:
                messagebox.showerror("Błąd", "Hasła się nie zgadzają!")
                return

            uzytkownicy[login] = haslo
            messagebox.showinfo("Sukces", "Konto zostało pomyślnie utworzone!")
            rejestracja_window.destroy()

        rejestracja_window = tk.Toplevel(okno_logowania)
        rejestracja_window.title("Rejestracja")
        rejestracja_window.geometry("400x400")

        tk.Label(rejestracja_window, text="Nowy login:").pack(pady=5)
        entry_login_new = tk.Entry(rejestracja_window)
        entry_login_new.pack(pady=5)

        tk.Label(rejestracja_window, text="Nowe hasło:").pack(pady=5)
        entry_haslo_new = tk.Entry(rejestracja_window, show="*")
        entry_haslo_new.pack(pady=5)

        tk.Label(rejestracja_window, text="Potwierdź hasło:").pack(pady=5)
        entry_confirm_haslo = tk.Entry(rejestracja_window, show="*")
        entry_confirm_haslo.pack(pady=5)

        tk.Label(rejestracja_window, text="Login administratora:").pack(pady=5)
        entry_admin_login = tk.Entry(rejestracja_window)
        entry_admin_login.pack(pady=5)

        tk.Label(rejestracja_window, text="Hasło administratora:").pack(pady=5)
        entry_admin_haslo = tk.Entry(rejestracja_window, show="*")
        entry_admin_haslo.pack(pady=5)

        tk.Button(rejestracja_window, text="Zapisz konto", command=zapisz_konto).pack(pady=15)
        rejestracja_window.bind('<Return>', lambda event: zapisz_konto())

    tk.Label(okno_logowania, text="Login:", bg="lightblue").pack(pady=10)
    entry_login = tk.Entry(okno_logowania)
    entry_login.pack(pady=5)
    entry_login.focus()

    tk.Label(okno_logowania, text="Hasło:", bg="lightblue").pack(pady=10)
    entry_haslo = tk.Entry(okno_logowania, show="*")
    entry_haslo.pack(pady=5)

    tk.Button(okno_logowania, text="Zaloguj", command=sprawdz_logowanie).pack(pady=20)
    tk.Button(okno_logowania, text="Utwórz nowe konto", command=utworz_konto).pack(pady=10)

    okno_logowania.bind('<Return>', lambda event: sprawdz_logowanie())
    okno_logowania.mainloop()


# =========================================================
# START PROGRAMU
# =========================================================

pokaz_okno_logowania()