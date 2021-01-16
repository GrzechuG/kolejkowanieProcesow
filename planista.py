## @package planista
# Zawiera czyste agorytmy kolejkowania procesów

from procesy import *

## Algorytm "Shortest Job First (niewywłaszczający)"
def SJF(kolejka):
    kolejka.sort(key=lambda x: x.pozostały_czas_wykonywania, reverse=False)

## Algorytm "Round Robin (wywłaczający)"
def RR(kolejka, czas, kwant_czasu):
    aktualny_proces = kolejka[0]
    print("Round robin:", czas, kwant_czasu)
    if aktualny_proces.czas_wykonywania() % kwant_czasu == 0 and aktualny_proces.czas_wykonywania() > 0:
        del kolejka[0]
        kolejka.append(aktualny_proces)
        aktualny_proces.uśpij()
        kolejka[0].wybudź()

        # aktualny_proces.uśpij()
        # kolejka[0].wybudź()



