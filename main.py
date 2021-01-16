## @package main
#Plik startowy main.

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

    print("Czasy oczekiwania:")

    średni_czas_oczekiwania = 0
    for proces in lista_procesow:

        print("PID:", proces.PID, " Czas oczekiwania:", proces.czas_oczekiwania)

        średni_czas_oczekiwania += proces.czas_oczekiwania

    średni_czas_oczekiwania /= len(lista_procesow)

    print()
    print("Kolejność:", kolejnosc)
    print("Średni czas oczekiwania procesów wynosi:", średni_czas_oczekiwania)
    print()
    return średni_czas_oczekiwania

def policz_sredni_czas_oczekiwania(lista_procesow):
    średni_czas_oczekiwania = 0
    for proces in lista_procesow:
        #print("PID:", proces.PID, " Czas oczekiwania:", proces.czas_oczekiwania)
        średni_czas_oczekiwania += proces.czas_oczekiwania

    średni_czas_oczekiwania /= len(lista_procesow)
    return średni_czas_oczekiwania

## Funkcja która dokonuje porównania obu algorytmów
def porównaj_algorytmy(kwant_czasu):

    teraz = datetime.now()
    dt_string = teraz.strftime("%d-%m-%Y_%H:%M:%S")
    nazwa_pliku = "raports/raport_" + dt_string + ".csv"
    sprawozdanie = open(nazwa_pliku, "a+")
    sprawozdanie.write(f"procesy, SJF, RR, q={kwant_czasu} \n")
    for i in range(3,100):

        srednia_SJF = 0
        srednia_RR = 0
        for j in range(0,20):
            lista_procesow = gen.generuj_procesy(i, generuj_raport=False)
            CPU1 = Procesor(copy.deepcopy(lista_procesow), "SJF")
            CPU2 = Procesor(copy.deepcopy(lista_procesow), "RR", kwant_czasu)

            lista_procesow1, kolejnosc1 = CPU1.pętla()
            lista_procesow2, kolejnosc2 = CPU2.pętla()

            sredni_czas_oczekiwania_SJF = policz_sredni_czas_oczekiwania(lista_procesow1)
            sredni_czas_oczekiwania_RR = policz_sredni_czas_oczekiwania(lista_procesow2)
            srednia_SJF += sredni_czas_oczekiwania_SJF
            srednia_RR += sredni_czas_oczekiwania_RR

        srednia_SJF /= 20
        srednia_RR /= 20

        sprawozdanie.write(f"{i}, {srednia_SJF}, {srednia_RR} \n")
    print("Wygenerowano sprawozdanie:", nazwa_pliku)



if __name__ == "__main__":
    main()




