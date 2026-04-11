from logging import root
import time 
import psutil
import tkinter as tk
import keyboard
import random
from tkinter import messagebox

def sprawdzanie_obecnosci_operatora():
    czas_początkowy = time.time()
    print("Sprawdzanie obecności operatora. Wcisnij enter")

    while czas_początkowy + 20 > time.time():
        if keyboard.is_pressed('enter'):
            print("Operator jest obecny.")
            return True

    print("Operator nie jest obecny.")
    return False

#DIAGNOSTYKA SYSTEMOWA
def uzycie_CPU():
    chwilowe_uzycie_CPU = psutil.cpu_percent(interval=1)  # Obciążenie CPU w %
    print(f"Obciążenie CPU: {chwilowe_uzycie_CPU}%")

    if chwilowe_uzycie_CPU > 80:  # Przykładowy próg krytyczny
        print("Uwaga! Obciążenie CPU przekroczyło bezpieczny poziom!")
        #uruchamianie wentylatorów   
    return chwilowe_uzycie_CPU

def wykorzystanie_RAM():
    chwilowe_uzycie_RAM = psutil.virtual_memory().percent  # Obciążenie RAM w %
    print(f"Obciążenie RAM: {chwilowe_uzycie_RAM}%")
    return chwilowe_uzycie_RAM

def predkosc_CPU():
    chwilowa_predkosc_CPU = psutil.cpu_freq().current  # Prędkość CPU w MHz
    print(f"Prędkość CPU: {chwilowa_predkosc_CPU} MHz")
    return chwilowa_predkosc_CPU    


#DANE O MASZYNACH I URZADZENIACH
class Urzadzenie:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.stan = "OFF"

    def sprawdzenie_zalaczenia_urzadzenia(self):
        pass

    def symulacja_awarii(self):
        pass


zasilanie_awaryjne = Urzadzenie("zasilanie_awaryjne")
drzwi_bezpieczenstwa = Urzadzenie("drzwi_bezpieczenstwa")
czujnik_obecnosci = Urzadzenie("czujniki_obecności")
naped_pneumatyczny = Urzadzenie("naped_pneumatyczny")

class Silnik(Urzadzenie):
    def __init__(self, nazwa):
        super().__init__(nazwa)
        self.temperatura = self.temperatura_startowa()

    def temperatura_startowa(self):
            if self.nazwa == "silnik": #silnik i obudowa silnika jako jeden obiekt
                temperatura = random.uniform(30.0, 90.0)  # Symulacja temperatury  w stopniach Celsjusza
            elif self.nazwa == "pompa_chlodnicza":
                temperatura = random.uniform(30.0, 90.0)
            return temperatura

    def monitorowanie_temperatury(self):
        return self.temperatura

    def symulacja_wzrostu_temperatury(self):
        for i in range(10):
            temperatura += random.uniform(0.5, 2.0)  # Symulacja wzrostu temperatury
            print(f"Symulacja wzrostu temperatury: {temperatura:.2f} °C")
            time.sleep(1)  # Opóźnienie między kolejnymi pomiarami

            if temperatura > 80.0:  # Przykładowy próg krytyczny
                print("Uwaga! Temperatura przekroczyła bezpieczny poziom!") 
                break
    
pompa_chlodnicza1 = Silnik("pompa_chlodnicza") #dziedziczy po silniku bo bedzie monitorowana temperatura plynu chlodniczego
pompa_chlodnicza2 = Silnik("pompa_chlodnicza")
silnik=Silnik("silnik")

class Wentylator(Urzadzenie):
    def __init__(self, nazwa):
        super().__init__(nazwa)
        self.obroty_wentylatora = self.predkosc_wentylatora()

    def predkosc_wentylatora(self):
        if self.nazwa == "wentylator_chlodzenia":
            self.obroty_wentylatora = random.uniform(1000.0, 3000.0)  # Symulacja prędkości wentylatora w RPM
            print(f"Prędkość wentylatora: {self.obroty_wentylatora:.2f} RPM")

        else:
            self.obroty_wentylatora = 0.0
            print("Nieznany typ wentylatora.")

        return self.obroty_wentylatora
    
    def wydajnosc_wentylatora(self):
        if self.nazwa == "wentylator_chlodzenia":
            wydajnosc = self.obroty_wentylatora * 0.1  # Przykładowa wydajność wentylatora
            print(f"Wydajność wentylatora: {wydajnosc:.2f} m³/h")
        
        elif self.nazwa == "filtr_powietrza":
            wydajnosc = self.obroty_wentylatora * 0.05  # Przykładowa wydajność wentylatora
            print(f"Wydajność wentylatora: {wydajnosc:.2f} m³/h")

        else:
            wydajnosc = 0.0
            print("Nieznany typ wentylatora.")

        return wydajnosc
    
wentylator1=Wentylator("wentylator_chlodzenia")
wentylator2=Wentylator("wentylator_chlodzenia")
filtr_powietrza=Wentylator("filtr_powietrza")
filtr_powietrza1=Wentylator("filtr_powietrza")

#INFORMACJE O PRODUKCJI  
#na razie przykldawoe wartosci do zmiany potem
def wydajnosc_linii_producyjnej():
    liczba_jednostek_produkcji_na_godzine= random.randint(50, 150)  # Symulacja liczby jednostek produkcji
    czas_pracy_linii=0
    wydajnosc_produkcji_procentowa = 0;
    czas_cyklu_na_minute = 60 / liczba_jednostek_produkcji_na_godzine  # Czas cyklu produkcyjnego w minutach
    ilosc_zuzytych_surowcow = liczba_jednostek_produkcji_na_godzine * 0.5  # Przykładowa ilość zużytych surowców

#monitorowanie wartosci i komunikat gdy cos zle idzie 
def monitorowanie_produkcji():
    pass


def stan_jakosci_produkcji():
    liczba_wadliwych_jednostek = random.randint(0, 10)  # Symulacja liczby wadliwych jednostek
    procentowa_liczba_odpadow = (liczba_wadliwych_jednostek / 100) * 100  # Procentowa liczba odpadów

def stan_zasilania_procesow_produkcji():
    zuzycie_energii = random.uniform(100.0, 500.0)  # Symulacja zużycia energii w kWh
    wydajnosc_energetyczna_maszyn= random.uniform(0.5, 1.0)  # Symulacja wydajności energetycznej maszyn (0-1)

#AWARIE I PRZEKROCZENIA PARAMETROW
def symulacja_awarii():

    pass



uzytkownicy = {
    "admin": "admin"
}

def otworz_panel_dyspozytorski():
    panel = tk.Tk()
    panel.title("Panel dyspozytorski")
    panel.geometry("900x600")
    panel.config(bg="white")

    label_powitalny = tk.Label(
        panel,
        text="Witaj w panelu dyspozytorskim",
        font=("Arial", 18, "bold"),
        bg="white"
    )
    label_powitalny.pack(pady=20)

    panel.mainloop()

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
        login = entry_login_new.get()
        haslo = entry_haslo_new.get()
        confirm_haslo = entry_confirm_haslo.get()
        admin_login = entry_admin_login.get()
        admin_haslo = entry_admin_haslo.get()

        if admin_login != "admin" or admin_haslo != "admin":
            messagebox.showerror("Błąd", "Niepoprawny login lub hasło administratora!")
            return

        if login in uzytkownicy:
            messagebox.showerror("Błąd", "Taki login już istnieje!")
            return

        if haslo != confirm_haslo:
            messagebox.showerror("Błąd", "Hasła się nie zgadzają!")
            return

        uzytkownicy[login] = haslo
        messagebox.showinfo("Sukces", f"Konto zostało pomyślnie utworzone!")
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



okno_logowania = tk.Tk()
okno_logowania.title("Logowanie")
okno_logowania.geometry("600x400")
okno_logowania.config(bg="lightblue")

tk.Label(okno_logowania, text="Login:", bg="lightblue").pack(pady=10)
entry_login = tk.Entry(okno_logowania)
entry_login.pack(pady=5)

tk.Label(okno_logowania, text="Hasło:", bg="lightblue").pack(pady=10)
entry_haslo = tk.Entry(okno_logowania, show="*")
entry_haslo.pack(pady=5)

tk.Button(okno_logowania, text="Zaloguj", command=sprawdz_logowanie).pack(pady=20)
tk.Button(okno_logowania, text="Utwórz nowe konto", command=utworz_konto).pack(pady=10)

okno_logowania.bind('<Return>', lambda event: sprawdz_logowanie())
okno_logowania.mainloop()


uzycie_CPU()
wykorzystanie_RAM() 
predkosc_CPU()

#sprawdzanie_obecnosci_operatora()



