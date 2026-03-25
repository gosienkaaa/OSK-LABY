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
def monitorowanie_temperatury(urzadzenie):

    if urzadzenie == "obudowa_silnika":
        temperatura = random.uniform(30.0, 90.0)  # Symulacja temperatury  w stopniach Celsjusza
    elif urzadzenie == "plyn_chlodniczy":
        temperatura = random.uniform(30.0, 90.0)  
    print(f"Temperatura {urzadzenie}: {temperatura:.2f} °C")

    return temperatura

def sprawdzenie_zalaczenia_urzadzenia(urzadzenie):
    pass

def symulacja_wzrostu_temperatury(temperatura):
    for i in range(10):
        temperatura += random.uniform(0.5, 2.0)  # Symulacja wzrostu temperatury
        print(f"Symulacja wzrostu temperatury: {temperatura:.2f} °C")
        time.sleep(1)  # Opóźnienie między kolejnymi pomiarami

        if temperatura > 80.0:  # Przykładowy próg krytyczny
            print("Uwaga! Temperatura przekroczyła bezpieczny poziom!") 
            break


    

uzycie_CPU()
wykorzystanie_RAM() 
predkosc_CPU()

sprawdzanie_obecnosci_operatora()



