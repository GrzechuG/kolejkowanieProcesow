## @package procesor
# Zawiera klasę Procesor

from procesy import *
import planista


##Klasa symulująca działanie procesora
class Procesor:

    ## Funkcja inicjalizująca procesor.
    # Jako argumenty bierze listę procesów i wybrany algorytm kolejkowania jako string,
    # który może przyjmować wartości "SJF" lub "RR"
    def __init__(self, lista_procesow, algorytm_kolejkowania):
        self.czas = -1
        self.kolejka = []
        self.lista_procesow = lista_procesow
        self.zakonczone_procesy = 0
        self.algorytm_kolejkowania = algorytm_kolejkowania
        self.aktualny_proces = None
        self.kolejnosc = []

    ##Funckja dokonuje sortowania kolejki wybranym algorytmem
    def kolejkowanie(self):

        if not self.kolejka:
            return

        if self.algorytm_kolejkowania == "SJF":
            planista.SJF(self.kolejka)

        elif self.algorytm_kolejkowania == "RR":
            planista.RR(self.kolejka, self.czas, 4)
        else:
            print("Algorytm: ", self.algorytm_kolejkowania, " nie jest wspierany!")

    ##Funckja dokonuje aktualizacji kolejki (dodaje nowo uruchomione procesy)
    def kolejka_aktualizacja(self):
        for proces in self.lista_procesow:
            if proces.czas_przybycia == self.czas:
                print("Nowy proces: PID", proces.PID)
                self.kolejka.append(proces)

        self.kolejkowanie()

        # print("Kolejka:")
        # for k in self.kolejka:
        #     print(k.PID)

    ## Główna pętla procesora
    def pętla(self):

        while True:
            self.czas += 1
            #print("Czas:", self.czas)

            self.kolejka_aktualizacja()

            if not self.kolejka:
                continue

            if not self.aktualny_proces or self.aktualny_proces.uśpiony:

                if self.aktualny_proces and self.aktualny_proces.uśpiony:
                    print("Wywłaszczenie procesu:", self.aktualny_proces.PID)

                self.aktualny_proces = self.kolejka[0]
                print("Aktualny proces:")
                # self.aktualny_proces.czas_oczekiwania = self.czas - self.aktualny_proces.czas_przybycia
                # self.aktualny_proces.info()
                self.kolejnosc.append(self.aktualny_proces.PID)

            self.aktualny_proces.tick()

            for proces in self.kolejka:
                if proces.PID != self.aktualny_proces.PID:
                    proces.czas_oczekiwania += 1

            if self.aktualny_proces.zakończony:
                print("Proces zakończony: ")
                # self.aktualny_proces.info()

                self.kolejka.remove(self.aktualny_proces)
                self.zakonczone_procesy += 1
                self.aktualny_proces = None

            if self.zakonczone_procesy == len(self.lista_procesow):
                break

        print(self.kolejnosc)

        return self.lista_procesow, self.kolejnosc
