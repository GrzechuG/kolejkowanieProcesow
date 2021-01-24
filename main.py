## @package main
# Plik startowy main.

"""
@Author Grzegorz Gajewski (252978)
"""
from datetime import datetime
import generator as gen
from procesor import *
import copy

global debug


## Funkcja main wywołująca menu z generatora oraz wywołująca pętle CPU.
def main():
    lista_procesow, algorytm, kwant_czasu = gen.menu()

    if algorytm == "test":
        porównaj_algorytmy(kwant_czasu)
        quit()

    debug = True
    if algorytm == "Both":

        CPU1 = Procesor(copy.deepcopy(lista_procesow), "SJF")
        CPU2 = Procesor(copy.deepcopy(lista_procesow), "RR")

        lista_procesow1, kolejnosc1 = CPU1.pętla()
        lista_procesow2, kolejnosc2 = CPU2.pętla()

        generuj_raport(lista_procesow1, kolejnosc1, "SJF")
        generuj_raport(lista_procesow2, kolejnosc2, "RR")

    else:
        CPU = Procesor(lista_procesow, algorytm, kwant_czasu)
        lista_procesow, kolejnosc = CPU.pętla()
        generuj_raport(lista_procesow, kolejnosc, algorytm)


##Funkcja tworząca raport:
def generuj_raport(lista_procesow, kolejnosc, algorytm):
    print("Tworzenie raportu dla algorytmu", algorytm)
    print("Kolejność:", kolejnosc)
    print("Średni czas oczekiwania procesów wynosi:", policz_sredni_czas_oczekiwania(lista_procesow))
    print("Maksymalny czas reakcji procesów wynosi:", max_czas_reakcji(lista_procesow))
    print()


##Funkcja licząca średni czas oczekiwania dla listy procesów po symulacji
def policz_sredni_czas_oczekiwania(lista_procesow):
    średni_czas_oczekiwania = 0
    for proces in lista_procesow:
        # print("PID:", proces.PID, " Czas oczekiwania:", proces.czas_oczekiwania)
        średni_czas_oczekiwania += proces.czas_oczekiwania

    średni_czas_oczekiwania /= len(lista_procesow)
    return średni_czas_oczekiwania


## Funkcja wyliczająca maksymalny czas reakcji dla listy procesów
def max_czas_reakcji(lista_procesow):
    return max([proces.czas_reakcji for proces in lista_procesow])



## Funkcja która dokonuje porównania obu algorytmów
def porównaj_algorytmy(kwant_czasu):
    teraz = datetime.now()
    dt_string = teraz.strftime("%d-%m-%Y_%H-%M-%S")
    nazwa_pliku = "raports/raport_" + dt_string + ".csv"
    sprawozdanie = open(nazwa_pliku, "a+")
    czas_przybycia_generacja = \
        ("Staly" if gen.czas_przybycia_config == gen.czas_przybycia_konfiguracja.STALY else "Losowy")

    sprawozdanie.write(
        f"procesy,SJF(średni),RR(średni),SJF(maksymalny czas reakcji),RR(maksymalny czas reakcji), q={kwant_czasu}, seed={gen.seed}, średnia i odchylenie czasu wykonywania: ({gen.średni_czas_wykonywania} i {gen.odchylenie_standardowe_wykonywania}), "+
        f"Czas przybycia: {czas_przybycia_generacja} \n"
    )
    for i in range(3, 100):
        if int(i*100/200) % 20 == 0:
            print("Postep:", (i*100/200), "%")

        srednia_SJF_oczekiwanie = 0
        srednia_RR_oczekiwanie = 0

        max_SJF_reakcji = 0
        max_RR_rakcji = 0

        usrednianie = 10
        for j in range(0, usrednianie):
            lista_procesow = gen.generuj_procesy(
                i,
                generuj_raport=False,
                quitet=True,
                średnia_długość_wykonywania=gen.średni_czas_wykonywania,
                odchylenie_standardowe_czasu_wykonywania=gen.odchylenie_standardowe_wykonywania,
                czas_przybycia_config=gen.czas_przybycia_config
            )
            CPU1 = Procesor(copy.deepcopy(lista_procesow), "SJF")
            CPU2 = Procesor(copy.deepcopy(lista_procesow), "RR", kwant_czasu)

            lista_procesow1, kolejnosc1 = CPU1.pętla()
            lista_procesow2, kolejnosc2 = CPU2.pętla()

            sredni_czas_oczekiwania_SJF = policz_sredni_czas_oczekiwania(lista_procesow1)
            sredni_czas_oczekiwania_RR = policz_sredni_czas_oczekiwania(lista_procesow2)

            max_czas_oczekiwania_SJF = max_czas_reakcji(lista_procesow1)
            max_czas_oczekiwania_RR = max_czas_reakcji(lista_procesow2)

            srednia_SJF_oczekiwanie += sredni_czas_oczekiwania_SJF
            srednia_RR_oczekiwanie += sredni_czas_oczekiwania_RR

            max_SJF_reakcji += max_czas_oczekiwania_SJF
            max_RR_rakcji += max_czas_oczekiwania_RR

        srednia_SJF_oczekiwanie /= usrednianie
        srednia_RR_oczekiwanie /= usrednianie
        max_SJF_reakcji /= usrednianie
        max_RR_rakcji /= usrednianie

        sprawozdanie.write(
            f"{i},{srednia_SJF_oczekiwanie},{srednia_RR_oczekiwanie}," +
            f"{max_SJF_reakcji},{max_RR_rakcji}\n"
        )

        # sprawozdanie.write(f"{i}, {srednia_SJF}, {srednia_RR} \n")
    sprawozdanie.close()
    print("Wygenerowano sprawozdanie (wersja dla LibreOffice):", nazwa_pliku)

    excel = open(nazwa_pliku).read().replace(",",";").replace(".", ",")
    excel_nazwa = "raports/raport_excel_" + dt_string + ".csv"
    open(excel_nazwa, "w+").write(excel)
    print("Wygenerowano sprawozdanie (wersja dla excel):", excel_nazwa)

    google = open(nazwa_pliku).read().replace(",", "\",\"").replace(".", ",")
    goole_linie = google.split("\n")
    for i in range(len(goole_linie)):
        goole_linie[i] = "\""+goole_linie[i]+"\""
    google = "\n".join(goole_linie)
    google_nazwa = "raports/raport_google_" + dt_string + ".csv"
    open(google_nazwa, "w+").write(google)
    print("Wygenerowano sprawozdanie (wersja dla Arkusze Google):", google_nazwa)



if __name__ == "__main__":
    main()
