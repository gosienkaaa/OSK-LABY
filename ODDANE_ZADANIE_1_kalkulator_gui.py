import tkinter as tk
import time
import math

# przechowuje pierwszą liczbę do działania
pierwsza_liczba = 0

# przechowuje wybraną operację
operacja = ""

#  informuje czy przed chwilą został wyświetlony wynik
po_wyniku = False


def pokaz_czas():
    # pobiera aktualny czas systemowy w formacie godzina:minuta:sekunda
    aktualny_czas = time.strftime("%H:%M:%S")

    # ustawia tekst etykiety z aktualnym czasem
    label_czas.config(text=aktualny_czas, font=("Arial", 24))

    # odświeża czas co 1s
    label_czas.after(1000, pokaz_czas)


def oblicz(a, b, dzialanie):
    # wykonuje działanie matematyczne w zależności od operatora

    if dzialanie == "+":
        return a + b
    elif dzialanie == "-":
        return a - b
    elif dzialanie == "×":
        return a * b
    elif dzialanie == "÷":
        if b == 0:
            return "niepoprawne dzialanie"
        else:
            return a / b
    elif dzialanie == "√":
        return a ** 0.5
    elif dzialanie == "%":
        return a / 100
    elif dzialanie == "x²":
        return a ** 2
    elif dzialanie == "1/x":
        if a == 0:
            return "niepoprawne dzialanie"
        else:
            return 1 / a
    elif dzialanie == "+/-":
        return -a
    else:
        return "niepoprawne działanie"


def klikniecie_operacji(op):
    global pierwsza_liczba, operacja

    # odblokowuje pole wyniku, aby można było edytować jego zawartość
    pole_wyniku.config(state=tk.NORMAL)

    # pobiera ostatnią linię z pola wyniku
    tekst = pole_wyniku.get("1.0", tk.END).strip().split("\n")[-1]

    # jeśli pole jest puste, ustawia domyślnie 0
    if tekst == "":
        druga_liczba = 0
    else:
        try:
            # próbuje zamienić tekst na liczbę typu float
            druga_liczba = float(tekst)
        except ValueError:
            # jeśli nie uda się zamienić tekstu na liczbę, ustawia 0
            druga_liczba = 0

    # obsługuje operacje jednoargumentowe
    if op in ["%", "√", "x²", "1/x", "+/-"]:
        wynik = oblicz(druga_liczba, None, op)

        # wyświetla wynik operacji jednoargumentowej
        pole_wyniku.delete("1.0", tk.END)
        pole_wyniku.insert(tk.END, str(wynik))

        # zapisuje wynik jako pierwszą liczbę do ewentualnych kolejnych działań
        pierwsza_liczba = wynik
        operacja = ""
        return

    # jeśli wcześniej była już wybrana operacja, najpierw wykonuje poprzednie działanie
    if operacja != "":
        wynik = oblicz(pierwsza_liczba, druga_liczba, operacja)
        pierwsza_liczba = wynik
    else:
        # jeśli nie było wcześniejszej operacji, zapisuje aktualną liczbę jako pierwszą
        pierwsza_liczba = druga_liczba

    # zapisuje nowo wybraną operację
    operacja = op

    # czyści pole wyniku, aby można było wpisać drugą liczbę
    pole_wyniku.delete("1.0", tk.END)


def klikniecie_liczby(liczba):
    global po_wyniku

    # jeśli wcześniej został wyświetlony wynik, to po wpisaniu nowej liczby pole zostaje wyczyszczone
    if po_wyniku:
        pole_wyniku.config(state=tk.NORMAL)
        pole_wyniku.delete("1.0", tk.END)
        po_wyniku = False

    # pobiera aktualny tekst z pola wyniku
    aktualna_liczba = pole_wyniku.get("1.0", tk.END).strip()

    # blokuje możliwość wpisania więcej niż jednej kropki w liczbie
    if liczba == "." and "." in aktualna_liczba:
        return

    # wpisuje nową cyfrę lub kropkę na końcu aktualnej liczby
    pole_wyniku.delete("1.0", tk.END)
    pole_wyniku.insert(tk.END, aktualna_liczba + liczba)


def klikniecie_rowna_sie():
    global pierwsza_liczba, operacja, po_wyniku

    # ustawia flagę informującą, że został wyświetlony wynik
    po_wyniku = True

    # pobiera cały tekst z pola wyniku
    tekst = pole_wyniku.get("1.0", tk.END).strip()
    if tekst == "":
        return

    # pobiera ostatnią linię z pola wyniku
    ostatnia_linia = tekst.split("\n")[-1]

    try:
        # próbuje zamienić ostatnią linię na liczbę
        druga_liczba = float(ostatnia_linia)
    except ValueError:
        return

    # jeśli nie wybrano żadnej operacji, zostawia samą liczbę jako wynik
    if operacja == "":
        pole_wyniku.delete("1.0", tk.END)
        pole_wyniku.insert(tk.END, str(druga_liczba))
        pierwsza_liczba = druga_liczba
        return

    # dla operacji jednoargumentowych druga liczba nie jest potrzebna
    if operacja in ["%", "√", "x²", "1/x", "+/-"]:
        druga_liczba = None
    else:
        # pobiera liczbę wpisaną w polu wyniku
        druga_liczba = float(pole_wyniku.get("1.0", tk.END))

    # oblicza wynik działania
    wynik = oblicz(pierwsza_liczba, druga_liczba, operacja)
    wynik=round(wynik, 5) if isinstance(wynik, float) else wynik

    # tworzy zapis działania wraz z wynikiem
    rownanie = f"{pierwsza_liczba} {operacja} {druga_liczba if druga_liczba is not None else ''} = \n{wynik}"

    # wyświetla działanie i wynik
    pole_wyniku.delete("1.0", tk.END)
    pole_wyniku.insert(tk.END, rownanie)

    # blokuje pole po wyświetleniu wyniku
    pole_wyniku.config(state=tk.DISABLED)

    # zapisuje wynik jako pierwszą liczbę do kolejnych działań
    pierwsza_liczba = wynik
    operacja = ""


def klikniecie_ce():
    # pobiera aktualny tekst z pola wyniku
    obecne_pole_wyniku = pole_wyniku.get("1.0", tk.END).strip()

    # usuwa ostatni znak
    usunieta_liczba = obecne_pole_wyniku[:-1]

    # wyświetla tekst po usunięciu ostatniego znaku
    pole_wyniku.delete("1.0", tk.END)
    pole_wyniku.insert(tk.END, usunieta_liczba)


def klikniecie_c():
    # odblokowuje pole wyniku
    pole_wyniku.config(state=tk.NORMAL)

    # czyści całe pole wyniku
    pole_wyniku.delete("1.0", tk.END)


def klawisz(event):
    # znaki dozwolone do bezpośredniego wpisania z klawiatury
    dozwolone_znaki = "0123456789."

    # obsługa cyfr i kropki
    if event.char in dozwolone_znaki:
        klikniecie_liczby(event.char)
        return "break"

    # obsługa operatorów z klawiatury
    elif event.char in ["+", "-", "*", "/"]:
        klikniecie_operacji(event.char.replace("*", "×").replace("/", "÷"))
        return "break"

    # obsługa klawisza równa się i enter
    elif event.char == "=" or event.keysym == "Return":
        klikniecie_rowna_sie()
        return "break"

    # obsługa klawisza c do czyszczenia pola
    elif event.char.lower() == "c":
        pole_wyniku.config(state="normal")
        pole_wyniku.delete("1.0", tk.END)
        return "break"

    # obsługa backspace do usuwania ostatniego znaku
    elif event.keysym == "BackSpace":
        klikniecie_ce()
        return "break"

    else:
        # dla innych klawiszy czyści pole i blokuje dalsze działanie
        pole_wyniku.delete("1.0", tk.END)
        return "break"


def pokaz_zegar_analowowy():
    global okno_analogowe, zegar_analogowy

    # jeśli okno zegara już istnieje, nie tworzy nowego
    if "okno_analogowe" in globals() and okno_analogowe.winfo_exists():
        return

    # tworzy nowe okno zegara analogowego
    okno_analogowe = tk.Toplevel(okno)
    okno_analogowe.title("Zegar Analogowy")
    okno_analogowe.geometry("300x300")

    # tworzy obszar rysowania zegara
    zegar_analogowy = tk.Canvas(
        okno_analogowe,
        width=300,
        height=300,
        bg="#eceaec" if slider_trybu.get() == 0 else "#746969"
    )
    zegar_analogowy.pack()

    # uruchamia rysowanie zegara
    rysuj_zegar_analogowy()


def rysuj_zegar_analogowy():
    # pobiera aktualnie ustawiony tryb kolorystyczny
    tryb = slider_trybu.get()

    # ustala kolory zegara zależnie od trybu
    if tryb == 0:
        tarcza_color = "#f0c0f0"
        outline_color = "purple"
    else:
        tarcza_color = "#D3BEBE"
        outline_color = "black"

    # czyści poprzednio narysowany zegar
    zegar_analogowy.delete("all")

    # ustala środek i promień tarczy
    srodek_x, srodek_y = 150, 150
    promien = 120

    # rysuje tarczę zegara
    zegar_analogowy.create_oval(
        srodek_x - promien,
        srodek_y - promien,
        srodek_x + promien,
        srodek_y + promien,
        outline=outline_color,
        width=2,
        fill=tarcza_color
    )

    # rysuje cyfry od 1 do 12 na tarczy
    for i in range(12):
        kat = math.radians(i * 30)
        x = srodek_x + (promien - 20) * math.sin(kat)
        y = srodek_y - (promien - 20) * math.cos(kat)
        zegar_analogowy.create_text(x, y, text=str(i if i != 0 else 12), font=("Arial", 12))

    # pobiera aktualny czas systemowy
    aktualny_czas = time.localtime()
    godzina = aktualny_czas.tm_hour % 12
    minuta = aktualny_czas.tm_min
    sekunda = aktualny_czas.tm_sec

    # oblicza kąty wskazówek
    kat_godzina = math.radians((godzina + minuta / 60) * 30)
    kat_minuta = math.radians(minuta * 6)
    kat_sekunda = math.radians(sekunda * 6)

    # rysuje wskazówkę godzinową
    zegar_analogowy.create_line(
        srodek_x, srodek_y,
        srodek_x + 50 * math.sin(kat_godzina),
        srodek_y - 50 * math.cos(kat_godzina),
        fill=outline_color,
        width=4
    )

    # rysuje wskazówkę minutową
    zegar_analogowy.create_line(
        srodek_x, srodek_y,
        srodek_x + 70 * math.sin(kat_minuta),
        srodek_y - 70 * math.cos(kat_minuta),
        fill=outline_color,
        width=3
    )

    # rysuje wskazówkę sekundową
    zegar_analogowy.create_line(
        srodek_x, srodek_y,
        srodek_x + 90 * math.sin(kat_sekunda),
        srodek_y - 90 * math.cos(kat_sekunda),
        fill="red",
        width=1
    )

    # odświeża zegar co 1 sekundę
    zegar_analogowy.after(1000, rysuj_zegar_analogowy)


def zmiana_trybu():
    # pobiera aktualny tryb z suwaka
    tryb = slider_trybu.get()

    # ustawia kolory dla trybu jasnego
    if tryb == 0:
        background_color = "#debfe0"
        pole_wyniku_color = "#eceaec"
        text_color = "purple"
        button_color = "#f0c0f0"

    # ustawia kolory dla trybu ciemnego
    else:
        background_color = "#746969"
        pole_wyniku_color = "#D3BEBE"
        text_color = "#333333"
        button_color = "#837777"

    # zmienia tło głównego okna
    okno.config(bg=background_color)

    # zmienia kolory pola wyniku
    pole_wyniku.config(bg=pole_wyniku_color, fg=text_color)

    # zmienia kolory ramki przycisków
    ramka_przyciski.config(bg=pole_wyniku_color)

    # zmienia kolor tekstu zegara cyfrowego
    label_czas.config(fg=text_color)

    # zmienia wygląd suwaka trybu
    slider_trybu.config(fg=text_color, troughcolor=button_color)

    # zmienia kolory wszystkich przycisków kalkulatora
    for widget in ramka_przyciski.winfo_children():
        widget.config(bg=button_color, fg=text_color)


# tworzy główne okno aplikacji
okno = tk.Tk()
okno.title("Kalkulator")
okno.geometry("410x650")

# tworzy górną ramkę na zegar i suwak trybu
ramka_gorna = tk.Frame(okno)
ramka_gorna.pack(fill="x")

# tworzy pole tekstowe do wyświetlania działań i wyników
pole_wyniku = tk.Text(okno, height=3, width=30, font=("Arial", 18))
pole_wyniku.pack(pady=10)

# podpina obsługę klawiatury do pola wyniku
pole_wyniku.bind("<Key>", klawisz)

# tworzy etykietę zegara cyfrowego
label_czas = tk.Label(ramka_gorna, text="vjkjbh", font=("Arial", 12))
label_czas.pack(side="right", padx=20)

# uruchamia wyświetlanie aktualnego czasu
pokaz_czas()

# tworzy suwak do zmiany trybu jasny/ciemny
slider_trybu = tk.Scale(
    ramka_gorna,
    from_=0,
    to=1,
    orient=tk.HORIZONTAL,
    label="Tryb",
    font=("Arial", 12),
    command=lambda x: zmiana_trybu(),
    length=50,
    showvalue=False
)
slider_trybu.pack(padx=70, side="left")
slider_trybu.set(0)

# tworzy ramkę na przyciski kalkulatora
ramka_przyciski = tk.Frame(okno)
ramka_przyciski.pack()

# lista przycisków wraz z ich pozycjami w siatce
przyciski = [
    ("%", 1, 0), ("+/-", 1, 1), ("CE", 1, 2), ("C", 1, 3),
    ("1/x", 2, 0), ("x²", 2, 1), ("√", 2, 2), ("÷", 2, 3),
    ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("×", 3, 3),
    ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("-", 4, 3),
    ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("+", 5, 3),
    (".", 6, 0), ("0", 6, 1), ("=", 6, 2)
]

# tworzy przyciski na podstawie listy
for (text, row, col) in przyciski:
    if text.isdigit() or text == ".":
        # tworzy przyciski cyfr i kropki
        button = tk.Button(
            ramka_przyciski,
            text=text,
            width=5,
            height=2,
            font=("Arial", 18),
            command=lambda t=text: klikniecie_liczby(t)
        )

    elif text in ["+", "-", "×", "÷", "√", "%", "x²", "1/x", "+/-"]:
        # tworzy przyciski operacji
        button = tk.Button(
            ramka_przyciski,
            text=text,
            width=5,
            height=2,
            font=("Arial", 18),
            command=lambda t=text: klikniecie_operacji(t)
        )

        # przycisk plus zajmuje dwa wiersze
        if text == "+":
            button.grid(row=row, column=col, padx=2, pady=2, rowspan=2, sticky="nsew")

    elif text == "C":
        # tworzy przycisk czyszczenia całego pola
        button = tk.Button(
            ramka_przyciski,
            text=text,
            width=5,
            height=2,
            font=("Arial", 18),
            command=lambda: klikniecie_c()
        )

    elif text == "CE":
        # tworzy przycisk usuwania ostatniego znaku
        button = tk.Button(
            ramka_przyciski,
            text=text,
            width=5,
            height=2,
            font=("Arial", 18),
            command=lambda: klikniecie_ce()
        )

    elif text == "=":
        # tworzy przycisk obliczania wyniku
        button = tk.Button(
            ramka_przyciski,
            text=text,
            width=5,
            height=2,
            font=("Arial", 18),
            command=lambda: klikniecie_rowna_sie()
        )
    else:
        # tworzy domyślny przycisk, jeśli nie pasuje do żadnej kategorii
        button = tk.Button(ramka_przyciski, text=text, width=5, height=2, font=("Arial", 18))

    # umieszcza przycisk w odpowiednim miejscu siatki
    button.grid(row=row, column=col, padx=2, pady=2)

# kliknięcie etykiety czasu otwiera zegar analogowy
label_czas.bind("<Button-1>", lambda e: pokaz_zegar_analowowy())

# opuszczenie etykiety zamyka okno zegara analogowego
label_czas.bind(
    "<Leave>",
    lambda e: okno_analogowe.destroy() if "okno_analogowe" in globals() else None
)

# ustawia początkowy tryb kolorystyczny
zmiana_trybu()

# uruchamia główną pętlę programu
okno.mainloop()