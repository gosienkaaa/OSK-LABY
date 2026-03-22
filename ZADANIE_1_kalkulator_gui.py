import tkinter as tk
import time
import math

pierwsza_liczba=0
operacja=""
po_wyniku=False

def pokaz_czas():
    aktualny_czas = time.strftime("%H:%M:%S")
    label_czas.config(text=aktualny_czas, font=("Arial", 24))
    label_czas.after(1000, pokaz_czas)  # Aktualizuj co 1 sekundę


def oblicz(a, b, dzialanie):

    if dzialanie=="+":
        return a+b
    elif dzialanie=="-":
         return a-b
    elif dzialanie=="×":
        return a*b
    elif dzialanie=="÷":
        if b==0:
            return("niepoprawne dzialanie")
        else:
            return a/b
    elif dzialanie=="√":
        return a**0.5
    elif dzialanie=="%":
        return a/100
    elif dzialanie=="x²":
        return a**2
    elif dzialanie=="1/x":
        if a==0:
            return("niepoprawne dzialanie")
        else:
            return 1/a
    elif dzialanie=="+/-":
        return -a
    else:   return("niepoprawne działanie")


def klikniecie_operacji(op):
    global pierwsza_liczba, operacja

    pole_wyniku.config(state=tk.NORMAL)
    # Pobieramy ostatnią linię pola wyniku, żeby zamienić ją na float
    tekst = pole_wyniku.get("1.0", tk.END).strip().split("\n")[-1]
    if tekst == "":
        druga_liczba = 0
    else:
        try:
            druga_liczba = float(tekst)
        except ValueError:
            # Jeśli ostatnia linia nie jest liczbą, ustaw na 0
            druga_liczba = 0

    #druga_liczba = float(pole_wyniku.get("1.0", tk.END))

    if op in ["%", "√", "x²", "1/x", "+/-"]:
        wynik = oblicz(druga_liczba, None, op)

        pole_wyniku.delete("1.0", tk.END)
        pole_wyniku.insert(tk.END, str(wynik))

        pierwsza_liczba = wynik
        operacja = ""
        return
    
    if operacja !="":
        wynik= oblicz(pierwsza_liczba, druga_liczba, operacja)
        pierwsza_liczba=wynik

    else:
        pierwsza_liczba=druga_liczba

    operacja = op
    pole_wyniku.delete("1.0", tk.END)
    

def klikniecie_liczby(liczba): #po to aby po przycisnieciu aktulaizowaly sie liczby w polu wyniku
    global po_wyniku

    if po_wyniku:   
        pole_wyniku.config(state=tk.NORMAL)  # Odblokowujemy pole wyniku, aby można było wprowadzać nowe liczby
        pole_wyniku.delete("1.0", tk.END)
        po_wyniku = False   

    aktualna_liczba = pole_wyniku.get("1.0", tk.END).strip()

    if liczba == "." and "." in aktualna_liczba:
        return

    pole_wyniku.delete("1.0", tk.END)
    pole_wyniku.insert(tk.END, aktualna_liczba + liczba)    

def klikniecie_rowna_sie():
    global pierwsza_liczba, operacja, po_wyniku

    po_wyniku = True    

    tekst = pole_wyniku.get("1.0", tk.END).strip()
    if tekst == "":
        return

    ostatnia_linia = tekst.split("\n")[-1]

    try:
        druga_liczba = float(ostatnia_linia)
    except ValueError:
        return

    if operacja == "":
        pole_wyniku.delete("1.0", tk.END)
        pole_wyniku.insert(tk.END, str(druga_liczba))
        pierwsza_liczba = druga_liczba
        return

    if operacja in ["%", "√", "x²", "1/x", "+/-"]:
        druga_liczba = None
    else:
        druga_liczba = float(pole_wyniku.get("1.0", tk.END))
       
    wynik = oblicz(pierwsza_liczba, druga_liczba, operacja)

    rownanie = f"{pierwsza_liczba} {operacja} {druga_liczba if druga_liczba is not None else ''} = \n{wynik}"

    pole_wyniku.delete("1.0", tk.END)
    pole_wyniku.insert(tk.END, rownanie)  
    pole_wyniku.config(state=tk.DISABLED)  # Blokujemy pole wyniku po wyświetleniu wyniku
    pierwsza_liczba=wynik
    operacja=""

def klikniecie_ce():
    obecne_pole_wyniku = pole_wyniku.get("1.0", tk.END).strip()

    usunieta_liczba = obecne_pole_wyniku[:-1]
    pole_wyniku.delete("1.0", tk.END)
    pole_wyniku.insert(tk.END, usunieta_liczba) 


def klikniecie_c():
    pole_wyniku.config(state=tk.NORMAL)  # Odblokowujemy pole wyniku, aby można było wprowadzać nowe liczby
    pole_wyniku.delete("1.0", tk.END)



def klawisz(event):

    dozwolone_znaki = "0123456789."

    if event.char in dozwolone_znaki:
        klikniecie_liczby(event.char)
        return "break"  # Ignorujemy dalsze przetwarzanie klawisza
    elif event.char in ["+", "-", "*", "/"]:
        klikniecie_operacji(event.char.replace("*", "×").replace("/", "÷"))
        return "break"
    elif event.char == "=" or event.keysym == "Return":
        klikniecie_rowna_sie()
        return "break"
    elif event.char.lower() == "c":
        pole_wyniku.config(state="normal")
        pole_wyniku.delete("1.0", tk.END)
        return "break"
    elif event.keysym == "BackSpace":
        klikniecie_ce()
        return "break"
    else:
        pole_wyniku.delete("1.0", tk.END)
        return "break"  # Ignorujemy inne klawisze




def pokaz_zegar_analowowy():
    global okno_analogowe, zegar_analogowy

    if "okno_analogowe" in globals() and okno_analogowe.winfo_exists():
        return
    
    okno_analogowe = tk.Toplevel(okno)
    okno_analogowe.title("Zegar Analogowy")         
    okno_analogowe.geometry("300x300")   

    zegar_analogowy = tk.Canvas(okno_analogowe, width=300, height=300, bg="#eceaec" if slider_trybu.get() == 0 else "#746969")
    zegar_analogowy.pack()

    rysuj_zegar_analogowy()

def rysuj_zegar_analogowy():
    tryb = slider_trybu.get()

    if tryb == 0:       
        #background_color = "#eceaec"
        tarcza_color = "#f0c0f0"
        outline_color = "purple"
    else:       
        #background_color = "#746969"
        tarcza_color = "#D3BEBE"
        outline_color = "black"


    zegar_analogowy.delete("all")  
    srodek_x, srodek_y = 150, 150
    promien = 120

    zegar_analogowy.create_oval(srodek_x - promien, srodek_y - promien, srodek_x + promien, srodek_y + promien, outline=outline_color, width=2, fill=tarcza_color)
   
    for i in range(12):          
        kat = math.radians(i * 30)
        x = srodek_x + (promien - 20) * math.sin(kat)
        y = srodek_y - (promien - 20) * math.cos(kat)
        zegar_analogowy.create_text(x, y, text=str(i if i != 0 else 12), font=("Arial", 12))

    aktualny_czas = time.localtime()
    godzina = aktualny_czas.tm_hour % 12    
    minuta = aktualny_czas.tm_min
    sekunda = aktualny_czas.tm_sec

    kat_godzina = math.radians((godzina + minuta / 60) * 30)
    kat_minuta = math.radians(minuta * 6)   
    kat_sekunda = math.radians(sekunda * 6) 
    zegar_analogowy.create_line(srodek_x, srodek_y, srodek_x + 50 * math.sin(kat_godzina), srodek_y - 50 * math.cos(kat_godzina), fill=outline_color, width=4)
    zegar_analogowy.create_line(srodek_x, srodek_y, srodek_x + 70 * math.sin(kat_minuta), srodek_y - 70 * math.cos(kat_minuta), fill=outline_color, width=3)
    zegar_analogowy.create_line(srodek_x, srodek_y, srodek_x + 90 * math.sin(kat_sekunda), srodek_y - 90 * math.cos(kat_sekunda), fill="red", width=1)  
   
    zegar_analogowy.after(1000, rysuj_zegar_analogowy)
   


def zmiana_trybu():# 0 tryb jasny, 1 tryb ciemny
    tryb= slider_trybu.get() 
    
    if tryb == 0:
        background_color = "#debfe0"
        pole_wyniku_color = "#eceaec"
        text_color = "purple"
        button_color = "#f0c0f0"

    else :
        background_color = "#746969"
        pole_wyniku_color = "#D3BEBE"   
        text_color = "#333333"
        button_color = "#837777" 
    

    okno.config(bg=background_color)
    pole_wyniku.config(bg=pole_wyniku_color, fg=text_color)   
    ramka_przyciski.config(bg=pole_wyniku_color)
    label_czas.config(fg=text_color)
    slider_trybu.config(fg=text_color, troughcolor=button_color)

    for widget in ramka_przyciski.winfo_children():
        widget.config(bg=button_color, fg=text_color)

okno = tk.Tk()
okno.title("Kalkulator")
okno.geometry("410x650")

ramka_gorna= tk.Frame(okno)
ramka_gorna.pack(fill="x")

pole_wyniku = tk.Text(okno, height=3, width=30, font=("Arial", 18))
pole_wyniku.pack(pady=10)
pole_wyniku.bind("<Key>",klawisz)

label_czas = tk.Label(ramka_gorna, text="vjkjbh", font=("Arial", 12))
label_czas.pack(side="right", padx=20)
pokaz_czas()


slider_trybu = tk.Scale(ramka_gorna, from_=0, to=1, orient=tk.HORIZONTAL, label="Tryb", font=("Arial", 12), command=lambda x: zmiana_trybu(), length=50, showvalue=False)
slider_trybu.pack(padx=70, side="left")
slider_trybu.set(0)



ramka_przyciski = tk.Frame(okno)
ramka_przyciski.pack()
przyciski = [
    ("%", 1, 0), ("+/-", 1, 1), ("CE", 1, 2), ("C", 1, 3),
    ("1/x", 2, 0), ("x²", 2, 1), ("√", 2, 2), ("÷", 2, 3),
    ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("×", 3, 3),
    ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("-", 4, 3),
    ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("+", 5, 3),
    (".", 6, 0), ("0", 6, 1), ("=", 6, 2)
  
]

for (text, row, col) in przyciski:
    if text.isdigit() or text == ".":
        button = tk.Button(ramka_przyciski, text=text, width=5, height=2, font=("Arial", 18), command=lambda t=text: klikniecie_liczby(t))

    elif text in ["+", "-", "×", "÷", "√", "%", "x²", "1/x", "+/-"]:
        button = tk.Button(ramka_przyciski, text=text, width=5, height=2, font=("Arial", 18), command=lambda t=text: klikniecie_operacji(t))
        if text == "+":
            button.grid(row=row, column=col, padx=2, pady=2, rowspan=2, sticky="nsew")
    elif text == "C":
        button = tk.Button(ramka_przyciski, text=text, width=5, height=2, font=("Arial", 18), command=lambda: klikniecie_c()) 
        
    elif text == "CE":
        button = tk.Button(ramka_przyciski, text=text, width=5, height=2, font=("Arial", 18), command=lambda: klikniecie_ce())
    elif text == "=":
        button = tk.Button(ramka_przyciski, text=text, width=5, height=2, font=("Arial", 18), command=lambda: klikniecie_rowna_sie())
    else:
        button = tk.Button(ramka_przyciski, text=text, width=5, height=2, font=("Arial", 18))
    button.grid(row=row, column=col, padx=2, pady=2)


label_czas.bind("<Button-1>", lambda e: pokaz_zegar_analowowy()) #klikniecie na etykiete z czasem otwiera okno z zegarem analogowym
label_czas.bind("<Leave>", lambda e: okno_analogowe.destroy() if "okno_analogowe" in globals() else None)  # Powrót do cyfrowego po opuszczeniu etykiety

zmiana_trybu()

okno.mainloop()
