import time 
import psutil
import tkinter as tk
import keyboard
import random


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

uzycie_CPU()
wykorzystanie_RAM() 
predkosc_CPU()

sprawdzanie_obecnosci_operatora()



