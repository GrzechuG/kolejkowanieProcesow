## @package procesor
# Zawiera klasę Procesor

from procesy import *
import planista


##Klasa symulująca działanie procesora
class Procesor:

    ## Funkcja inicjalizująca procesor.
    # Jako argumenty bierze listę procesów i wybrany algorytm kolejkowania jako string,
    # który może przyjmować wartości "SJF" lub "RR"
    def __init__(self, lista_procesow, algorytm_kolejkowania, kwant_czasu = 4, debug=False):
        self.czas = -1
        self.kolejka = []
        self.lista_procesow = lista_procesow
        self.zakonczone_procesy = 0
        self.algorytm_kolejkowania = algorytm_kolejkowania
        self.aktualny_proces = None
        self.kolejnosc = []
        self.kwant_czasu = kwant_czasu
        self.debug = debug

    ##Funckja dokonuje sortowania kolejki wybranym algorytmem
    def kolejkowanie(self):

        if not self.kolejka:
            return

        if self.algorytm_kolejkowania == "SJF":
            planista.SJF(self.kolejka)

        elif self.algorytm_kolejkowania == "RR":
            planista.RR(self.kolejka, self.czas, self.kwant_czasu)
        else:
            print("Algorytm: ", self.algorytm_kolejkowania, " nie jest wspierany!")

    ##Funckja dokonuje aktualizacji kolejki (dodaje nowo uruchomione procesy)
    #oraz wywołuje kolejkowanie
    def kolejka_aktualizacja(self):
        for proces in self.lista_procesow:
            if proces.czas_przybycia == self.czas:
                if self.debug:
                    print("Nowy proces: PID", proces.PID)
                self.kolejka.append(proces)

        #Rozwiązuje BUG w RR:
        if self.aktualny_proces is not None or self.algorytm_kolejkowania == "SJF":
            self.kolejkowanie()

        if self.debug:
            print("Kolejka:")
            for k in self.kolejka:
                print(k.PID, end=" ")
            print()

    ## Główna pętla procesora
    def pętla(self):

        while True:
            self.czas += 1
            if self.debug:
                print("Czas:", self.czas)

            self.kolejka_aktualizacja()

            if not self.kolejka:
                continue

            #Ustawiam aktualny proces
            if not self.aktualny_proces or self.aktualny_proces.uśpiony or self.aktualny_proces.zakończony:


                if self.aktualny_proces and self.aktualny_proces.uśpiony:
                    if self.debug:
                        print("Wywłaszczenie procesu:", self.aktualny_proces.PID)

                self.aktualny_proces = self.kolejka[0]
                if self.debug:
                    print("Aktualny proces PID:", self.aktualny_proces.PID)
                # self.aktualny_proces.czas_oczekiwania = self.czas - self.aktualny_proces.czas_przybycia
                # self.aktualny_proces.info()
                self.kolejnosc.append(self.aktualny_proces.PID)

            self.aktualny_proces.tick()

            for proces in self.kolejka:
                if proces.PID != self.aktualny_proces.PID:
                    proces.czas_oczekiwania += 1
                    if not proces.byl_wywlaszczony:
                        proces.czas_reakcji +=1


            if self.aktualny_proces.zakończony:
                if self.debug:
                    print("Proces zakończony PID:", self.aktualny_proces.PID)
                # self.aktualny_proces.info()

                self.kolejka.remove(self.aktualny_proces)
                self.zakonczone_procesy += 1
                self.aktualny_proces = None

            if self.zakonczone_procesy == len(self.lista_procesow):
                break
        if self.debug:
            print(self.kolejnosc)

        return self.lista_procesow, self.kolejnosc
