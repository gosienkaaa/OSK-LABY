import time
import psutil
import tkinter as tk
import random
from tkinter import messagebox


# =========================
# DIAGNOSTYKA SYSTEMOWA
# =========================

def uzycie_CPU():
    return psutil.cpu_percent(interval=None)

def wykorzystanie_RAM():
    return psutil.virtual_memory().percent

def predkosc_CPU():
    cpu_freq = psutil.cpu_freq()
    if cpu_freq is not None:
        return cpu_freq.current
    return 0.0


# =========================
# DANE O MASZYNACH I URZĄDZENIACH
# =========================

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

    def temperatura_startowa(self):
        if self.nazwa == "silnik":
            return random.uniform(45.0, 60.0)
        elif self.nazwa == "pompa_chlodnicza":
            return random.uniform(22.0, 35.0)
        return random.uniform(25.0, 40.0)

    def monitorowanie_temperatury(self):
        return self.temperatura

    def aktualizuj_temperature(self, linia_dziala):
        if self.stan != "ON":
            self.temperatura -= random.uniform(0.1, 0.3)
        else:
            if linia_dziala:
                self.temperatura += random.uniform(0.1, 0.6)
            else:
                self.temperatura -= random.uniform(0.05, 0.2)

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
            return random.uniform(1600.0, 2400.0)
        elif self.nazwa == "filtr_powietrza":
            return random.uniform(700.0, 1200.0)
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
                self.obroty_wentylatora += random.uniform(-50, 80)
            else:
                self.obroty_wentylatora += random.uniform(-40, 40)
            self.obroty_wentylatora = max(1400.0, min(self.obroty_wentylatora, 3000.0))

        elif self.nazwa == "filtr_powietrza":
            if linia_dziala:
                self.obroty_wentylatora += random.uniform(-20, 30)
            else:
                self.obroty_wentylatora += random.uniform(-10, 10)
            self.obroty_wentylatora = max(600.0, min(self.obroty_wentylatora, 1500.0))


# Urządzenia
zasilanie_awaryjne = Urzadzenie("zasilanie awaryjne", "ON")
drzwi_bezpieczenstwa = Urzadzenie("drzwi bezpieczeństwa", "zamknięte")
czujnik_obecnosci = Urzadzenie("czujnik obecności operatora", "aktywne")
naped_pneumatyczny = Urzadzenie("napęd pneumatyczny", "ON")

pompa_chlodnicza1 = Silnik("pompa_chlodnicza", "ON")
pompa_chlodnicza2 = Silnik("pompa_chlodnicza", "ON")
silnik = Silnik("silnik", "ON")

wentylator1 = Wentylator("wentylator_chlodzenia", "ON")
wentylator2 = Wentylator("wentylator_chlodzenia", "ON")
filtr_powietrza1 = Wentylator("filtr_powietrza", "ON")
filtr_powietrza2 = Wentylator("filtr_powietrza", "ON")


# =========================
# PRODUKCJA - STAN CIĄGŁY
# =========================

linia_uruchomiona = False
czas_startu_linii = None
ostatnia_aktualizacja_produkcji = None

bazowa_wydajnosc_na_godzine = 120.0

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
    stan_produkcji["liczba_jednostek"] = 0.0
    stan_produkcji["czas_pracy_h"] = 0.0
    stan_produkcji["wydajnosc_procentowa"] = 0.0
    stan_produkcji["czas_cyklu_min"] = 0.0
    stan_produkcji["zuzycie_surowcow_kg"] = 0.0
    stan_produkcji["wadliwe_jednostki"] = 0
    stan_produkcji["odpady_procent"] = 0.0
    stan_produkcji["zuzycie_energii_kwh"] = 0.0
    stan_produkcji["wydajnosc_energetyczna"] = 0.0
    stan_produkcji["aktualna_wydajnosc_h"] = 0.0


def czy_mozna_uruchomic_linie():
    if drzwi_bezpieczenstwa.stan != "zamknięte":
        return False, "Nie można uruchomić linii: drzwi bezpieczeństwa są otwarte."

    if zasilanie_awaryjne.stan != "ON":
        return False, "Nie można uruchomić linii: zasilanie awaryjne jest wyłączone."

    return True, "Warunki startu spełnione."


def aktualizuj_urzadzenia():
    silnik.aktualizuj_temperature(linia_uruchomiona)
    pompa_chlodnicza1.aktualizuj_temperature(linia_uruchomiona)
    pompa_chlodnicza2.aktualizuj_temperature(linia_uruchomiona)

    wentylator1.aktualizuj_obroty(linia_uruchomiona)
    wentylator2.aktualizuj_obroty(linia_uruchomiona)
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
    aktualna_wydajnosc = bazowa_wydajnosc_na_godzine + odchylenie

    if silnik.temperatura > 80:
        aktualna_wydajnosc -= 15

    if pompa_chlodnicza1.temperatura > 60 or pompa_chlodnicza2.temperatura > 60:
        aktualna_wydajnosc -= 10

    if wentylator1.obroty_wentylatora < 1500 or wentylator2.obroty_wentylatora < 1500:
        aktualna_wydajnosc -= 8

    aktualna_wydajnosc = max(60.0, aktualna_wydajnosc)

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

    moc_chwilowa_kw = random.uniform(18.0, 24.0)
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


def symulacja_awarii():
    lista_awarii = []

    if linia_uruchomiona:
        if silnik.temperatura > 80:
            lista_awarii.append("Przekroczona temperatura silnika")

        if pompa_chlodnicza1.temperatura > 60:
            lista_awarii.append("Wysoka temperatura pompy chłodniczej 1")

        if pompa_chlodnicza2.temperatura > 60:
            lista_awarii.append("Wysoka temperatura pompy chłodniczej 2")

        if wentylator1.obroty_wentylatora < 1500:
            lista_awarii.append("Zbyt niskie obroty wentylatora 1")

        if wentylator2.obroty_wentylatora < 1500:
            lista_awarii.append("Zbyt niskie obroty wentylatora 2")

        if uzycie_CPU() > 85:
            lista_awarii.append("Wysokie obciążenie CPU komputera")

    if not lista_awarii:
        lista_awarii.append("Brak aktywnych awarii")

    return lista_awarii


# =========================
# KONTA
# =========================

uzytkownicy = {
    "admin": "admin"
}


# =========================
# PANEL DYSPOZYTORSKI
# =========================

class PanelDyspozytorski:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel dyspozytorski")
        self.root.geometry("1200x700")
        self.root.configure(bg="lightgray")

        self.aktualny_widok = None

        self.okno_potwierdzenia = None
        self.operator_potwierdzil_obecnosc = False
        self.interwal_sprawdzenia_ms = 60000
        self.czas_na_potwierdzenie_ms = 30000

        self.main_frame = tk.Frame(self.root, bg="lightgray")
        self.main_frame.pack(fill="both", expand=True)

        self.menu_frame = tk.Frame(self.main_frame, bg="#d9d9d9", width=270, bd=2, relief="solid")
        self.menu_frame.pack(side="left", fill="y")
        self.menu_frame.pack_propagate(False)

        self.content_frame = tk.Frame(self.main_frame, bg="white", bd=2, relief="solid")
        self.content_frame.pack(side="right", fill="both", expand=True)

        tk.Button(
            self.menu_frame, text="Stan urządzeń", font=("Arial", 14), height=2,
            command=self.pokaz_stan_urzadzen
        ).pack(fill="x", pady=2)

        tk.Button(
            self.menu_frame, text="Stan produkcji", font=("Arial", 14), height=2,
            command=self.pokaz_stan_produkcji
        ).pack(fill="x", pady=2)

        tk.Button(
            self.menu_frame, text="Awarie", font=("Arial", 14), height=2,
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

    def wyczysc_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def petla_glowna_aktualizacji(self):
        aktualizuj_urzadzenia()
        aktualizuj_stan_produkcji()

        if self.aktualny_widok == "urzadzenia":
            self.odswiez_stan_urzadzen()
        elif self.aktualny_widok == "produkcja":
            self.odswiez_stan_produkcji()
        elif self.aktualny_widok == "awarie":
            self.odswiez_awarie()
        elif self.aktualny_widok == "komputer":
            self.odswiez_stan_komputera()

        self.root.after(1000, self.petla_glowna_aktualizacji)

    def przelacz_linie(self):
        global linia_uruchomiona, czas_startu_linii, ostatnia_aktualizacja_produkcji

        if not linia_uruchomiona:
            mozna_uruchomic, komunikat = czy_mozna_uruchomic_linie()

            if not mozna_uruchomic:
                messagebox.showwarning("Brak możliwości uruchomienia", komunikat)
                return

            linia_uruchomiona = True
            czas_startu_linii = time.time()
            ostatnia_aktualizacja_produkcji = time.time()
            resetuj_stan_produkcji()

            self.btn_linia.config(text="Zatrzymaj linię produkcyjną", bg="#f3d48b")
            self.status_linii_label.config(text="Status linii: URUCHOMIONA", fg="green")
            messagebox.showinfo("Linia produkcyjna", "Linia produkcyjna została uruchomiona.")
        else:
            linia_uruchomiona = False
            czas_startu_linii = None
            ostatnia_aktualizacja_produkcji = None

            self.btn_linia.config(text="Uruchom linię produkcyjną", bg="#b6e3b6")
            self.status_linii_label.config(text="Status linii: ZATRZYMANA", fg="red")
            messagebox.showinfo("Linia produkcyjna", "Linia produkcyjna została zatrzymana.")

    def wyloguj(self):
        odpowiedz = messagebox.askyesno("Wylogowanie", "Czy na pewno chcesz się wylogować?")
        if odpowiedz:
            self.root.destroy()
            pokaz_okno_logowania()

    def pokaz_stan_urzadzen(self):
        self.aktualny_widok = "urzadzenia"
        self.wyczysc_content()

        tk.Label(
            self.content_frame, text="Stan urządzeń",
            font=("Arial", 22, "bold"), bg="white"
        ).pack(pady=20)

        self.urzadzenia_labels = []
        for _ in range(11):
            lbl = tk.Label(self.content_frame, font=("Arial", 13), bg="white")
            lbl.pack(anchor="w", padx=20, pady=4)
            self.urzadzenia_labels.append(lbl)

        self.odswiez_stan_urzadzen()

    def odswiez_stan_urzadzen(self):
        if self.aktualny_widok != "urzadzenia":
            return
        if not hasattr(self, "urzadzenia_labels"):
            return

        dane = [
            f"Silnik - stan: {silnik.stan}, temperatura: {silnik.monitorowanie_temperatury():.2f} °C",
            f"Pompa chłodnicza 1 - stan: {pompa_chlodnicza1.stan}, temperatura: {pompa_chlodnicza1.monitorowanie_temperatury():.2f} °C",
            f"Pompa chłodnicza 2 - stan: {pompa_chlodnicza2.stan}, temperatura: {pompa_chlodnicza2.monitorowanie_temperatury():.2f} °C",
            f"Wentylator 1 - stan: {wentylator1.stan}, obroty: {wentylator1.obroty_wentylatora:.2f} RPM",
            f"Wentylator 2 - stan: {wentylator2.stan}, obroty: {wentylator2.obroty_wentylatora:.2f} RPM",
            f"Filtr powietrza 1 - wydajność: {filtr_powietrza1.wydajnosc_wentylatora():.2f} m³/h",
            f"Filtr powietrza 2 - wydajność: {filtr_powietrza2.wydajnosc_wentylatora():.2f} m³/h",
            f"Zasilanie awaryjne - stan: {zasilanie_awaryjne.stan}",
            f"Drzwi bezpieczeństwa - stan: {drzwi_bezpieczenstwa.stan}",
            f"Czujnik obecności operatora - stan: {czujnik_obecnosci.stan}",
            f"Napęd pneumatyczny - stan: {naped_pneumatyczny.stan}",
        ]

        for lbl, tekst in zip(self.urzadzenia_labels, dane):
            lbl.config(text=tekst)

    def pokaz_stan_produkcji(self):
        self.aktualny_widok = "produkcja"
        self.wyczysc_content()

        tk.Label(
            self.content_frame, text="Stan produkcji",
            font=("Arial", 22, "bold"), bg="white"
        ).pack(pady=20)

        self.produkcja_labels = {}
        pola = [
            "Stan linii",
            "Aktualna wydajność chwilowa",
            "Liczba jednostek",
            "Czas pracy linii",
            "Wydajność procentowa",
            "Czas cyklu",
            "Zużycie surowców",
            "Wadliwe jednostki",
            "Odpady",
            "Zużycie energii",
            "Wydajność energetyczna maszyn"
        ]

        for nazwa in pola:
            lbl = tk.Label(self.content_frame, font=("Arial", 13), bg="white")
            lbl.pack(anchor="w", padx=20, pady=4)
            self.produkcja_labels[nazwa] = lbl

        self.odswiez_stan_produkcji()

    def odswiez_stan_produkcji(self):
        if self.aktualny_widok != "produkcja":
            return
        if not hasattr(self, "produkcja_labels"):
            return

        dane = pobierz_dane_produkcji()

        self.produkcja_labels["Stan linii"].config(text=f"Stan linii: {dane['stan_linii']}")
        self.produkcja_labels["Aktualna wydajność chwilowa"].config(
            text=f"Aktualna wydajność chwilowa: {dane['aktualna_wydajnosc_h']} szt./h"
        )
        self.produkcja_labels["Liczba jednostek"].config(
            text=f"Liczba jednostek: {dane['liczba_jednostek']}"
        )
        self.produkcja_labels["Czas pracy linii"].config(
            text=f"Czas pracy linii: {dane['czas_pracy_h']} h"
        )
        self.produkcja_labels["Wydajność procentowa"].config(
            text=f"Wydajność procentowa: {dane['wydajnosc_procentowa']} %"
        )
        self.produkcja_labels["Czas cyklu"].config(
            text=f"Czas cyklu: {dane['czas_cyklu_min']} min"
        )
        self.produkcja_labels["Zużycie surowców"].config(
            text=f"Zużycie surowców: {dane['zuzycie_surowcow_kg']} kg"
        )
        self.produkcja_labels["Wadliwe jednostki"].config(
            text=f"Wadliwe jednostki: {dane['wadliwe_jednostki']}"
        )
        self.produkcja_labels["Odpady"].config(
            text=f"Odpady: {dane['odpady_procent']} %"
        )
        self.produkcja_labels["Zużycie energii"].config(
            text=f"Zużycie energii: {dane['zuzycie_energii_kwh']} kWh"
        )
        self.produkcja_labels["Wydajność energetyczna maszyn"].config(
            text=f"Wydajność energetyczna maszyn: {dane['wydajnosc_energetyczna']}"
        )

    def pokaz_awarie(self):
        self.aktualny_widok = "awarie"
        self.wyczysc_content()

        tk.Label(
            self.content_frame, text="Awarie",
            font=("Arial", 22, "bold"), bg="white", fg="red"
        ).pack(pady=20)

        self.awarie_frame = tk.Frame(self.content_frame, bg="white")
        self.awarie_frame.pack(fill="both", expand=True)

        self.odswiez_awarie()

    def odswiez_awarie(self):
        if self.aktualny_widok != "awarie":
            return
        if not hasattr(self, "awarie_frame"):
            return

        for widget in self.awarie_frame.winfo_children():
            widget.destroy()

        awarie = symulacja_awarii()

        for tekst in awarie:
            kolor = "green" if tekst == "Brak aktywnych awarii" else "red"
            tk.Label(
                self.awarie_frame, text=tekst, font=("Arial", 13),
                bg="white", fg=kolor
            ).pack(anchor="w", padx=20, pady=4)

    def pokaz_stan_komputera(self):
        self.aktualny_widok = "komputer"
        self.wyczysc_content()

        tk.Label(
            self.content_frame, text="Stan komputera",
            font=("Arial", 22, "bold"), bg="white"
        ).pack(pady=20)

        self.label_cpu = tk.Label(self.content_frame, font=("Arial", 13), bg="white")
        self.label_cpu.pack(anchor="w", padx=20, pady=4)

        self.label_ram = tk.Label(self.content_frame, font=("Arial", 13), bg="white")
        self.label_ram.pack(anchor="w", padx=20, pady=4)

        self.label_cpu_speed = tk.Label(self.content_frame, font=("Arial", 13), bg="white")
        self.label_cpu_speed.pack(anchor="w", padx=20, pady=4)

        self.odswiez_stan_komputera()

    def odswiez_stan_komputera(self):
        if self.aktualny_widok != "komputer":
            return
        if not hasattr(self, "label_cpu") or not self.label_cpu.winfo_exists():
            return

        cpu = uzycie_CPU()
        ram = wykorzystanie_RAM()
        cpu_speed = predkosc_CPU()

        self.label_cpu.config(text=f"Użycie CPU: {cpu:.2f} %")
        self.label_ram.config(text=f"Użycie RAM: {ram:.2f} %")
        self.label_cpu_speed.config(text=f"Prędkość CPU: {cpu_speed:.2f} MHz")

    # =========================
    # SPRAWDZANIE OBECNOŚCI OPERATORA
    # =========================

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
        messagebox.showwarning(
            "ALARM",
            "Brak potwierdzenia obecności operatora przez 30 sekund.\n"
            "Operator zostanie wylogowany z systemu."
        )

        self.root.destroy()
        pokaz_okno_logowania()


# =========================
# LOGOWANIE
# =========================

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


# =========================
# START PROGRAMU
# =========================

pokaz_okno_logowania()