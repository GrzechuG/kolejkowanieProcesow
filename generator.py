## @package generator
# Zajmuje się generowaniem oraz wczytywaniem danych do programu.

import random as random
import numpy as np
from procesy import *
from datetime import datetime
global seed
global średni_czas_wykonywania
global odchylenie_standardowe_wykonywania
global czas_przybycia_config
## Funkcja wypisuje interaktywne menu na konsolę oraz obiera dane wejściowe
def menu():
    global seed
    lista_procesow = []
    kwant_czasu = None
    print("__MENU__")
    print("1. Wygeneruj nowy zestaw procesów")
    print("2. Załaduj zestaw procesów z pliku csv")
    print("3. Wygeneruj na bazie zapisanego seed")
    print("4. Przeprowadź badanie na dużym zestawie danych")
    opcja = int(input("opcja> "))
    if opcja == 1:
        ilość = int(input("Ile procesów wygenerować? > "))
        try:
            lista_procesow = generuj_procesy(ilość)
        except Exception as e:
            print("Wystąpił błąd podczas generowania procesów!", e)
            quit(-1)

    elif opcja == 2:
        plik = input("Podaj ścieżkę do pliku (csv) > ")
        try:
            lista_procesow = załaduj_procesy(plik)
        except Exception as e:
            print("Wystąpił błąd podczas czytania procesów!", e)
            quit(-1)
    elif opcja == 3:
        ilość = int(input("Ile procesów wygenerować? > "))
        seed = int(input("Podaj seed: > "))

        setSeed(seed)
        try:
            lista_procesow = generuj_procesy(ilość)
        except Exception as e:
            print("Wystąpił błąd podczas generowania procesów!", e)
            quit(-1)

    elif opcja == 4:
        seed = int(input("Podaj seed dla generatora: > "))
        kwant_czasu = int(input("Podaj kwant czasu:"))
        global średni_czas_wykonywania
        global odchylenie_standardowe_wykonywania
        średni_czas_wykonywania = int(input("Podaj średni czas wykonywania dla procesu:"))
        odchylenie_standardowe_wykonywania = int(input("Podaj odchylenie standardowe czasu wykonywania dla procesu:"))
        czas_przybycia_inp = input("Czy czas przybycia ma być losowy czy stały? L/S >")
        global czas_przybycia_config
        if czas_przybycia_inp == "S":
            czas_przybycia_config = czas_przybycia_konfiguracja.STALY
        else:
            czas_przybycia_config = czas_przybycia_konfiguracja.LOSOWY

        setSeed(seed)
        return [], "test", kwant_czasu

    else:
        print("Opcja nie istnieje! Proszę wybrać właściwie!")
        return menu()


    algorytm = None
    print("__MENU__")
    print("Jakiego algorytmu kolejkowania użyć?")
    print("1. SJF (niewywłaszczający)")
    print("2. Round Robin")
    print("3. Wykonaj i porównaj oba (RR i SJF)")
    opcja = int(input("opcja> "))
    if opcja == 1:
        print("Wybrano algorytm SJF!")
        algorytm = "SJF"
    elif opcja == 2:
        print("Wybrano algorytm Round Robin!")
        kwant_czasu = int(input("Podaj kwant czasu:"))
        algorytm = "RR"

    elif opcja == 3:
        print("Wybrano tryb porównywania!")
        algorytm = "Both"
    else:
        print("Opcja nie istnieje! Proszę wybrać właściwie!")
        return menu()

    return lista_procesow, algorytm, kwant_czasu

##Ustawia seed na generatorze liczb losowych
def setSeed(sd):
    global seed
    seed = sd
    random.seed(sd)

class czas_przybycia_konfiguracja:
    LOSOWY = 0
    STALY = 1
#Funkcja generuje procesy o losowych czasach przybycia oraz wykonywania
def generuj_procesy(
        ilość,
        średnia_długość_wykonywania=10,
        odchylenie_standardowe_czasu_wykonywania=5,
        generuj_raport=True,
        quitet=False,
        czas_przybycia_config = czas_przybycia_konfiguracja.LOSOWY):

    lista_procesow = []

    if generuj_raport:
        # Utworzenie pliku o nazwie powiazanej z aktualna data i czasem:
        teraz = datetime.now()
        dt_string = teraz.strftime("%d-%m-%Y_%H-%M-%S")
        export_file = open("data/procesy_" + dt_string + ".csv", "a+")

        #Wpisanie pierwszej linii jako "tytulow" kolumn:
        export_file.write("PID, czas przybycia, czas wykonywania \n")

    #Generowanie procesow o lowych czasach przybycia i wykonywania:
    for i in range(0, ilość):
        PID = i+1
        if(czas_przybycia_config == czas_przybycia_konfiguracja.LOSOWY):
            czas_przybycia = random.randint(0, 100)
        else:
            czas_przybycia = 0

        czas_wykonywania = abs(int(
            random.normalvariate(
                średnia_długość_wykonywania,
                odchylenie_standardowe_czasu_wykonywania
                                 )))+1

        p = Proces(PID, czas_przybycia, czas_wykonywania)
        lista_procesow.append(p)

        if not quitet:
            print("P", PID, sep="")
            print(p.info())
            print()

        if generuj_raport:
            #Wpisanie do pliku danych o procesie:
            export_file.write(",".join([str(p.PID), str(p.czas_przybycia), str(p.pozostały_czas_wykonywania)]) + "\n")


    return lista_procesow


#Funkcja wczytuje procesu z pliku csv
def załaduj_procesy(plik):
    lista_procesow = []

    import_lines = open(plik, "r").readlines()

    #Usuniecie nazw kolum:
    if "PID" in import_lines[0]:
        import_lines = import_lines[1:]

    for line in import_lines:

        info = line.split(",")
        PID = int(info[0])
        czas_przybycia = int(info[1])
        czas_wykonywania = int(info[2])

        p = Proces(PID, czas_przybycia, czas_wykonywania)
        lista_procesow.append(p)
        p.info()
    return lista_procesow
