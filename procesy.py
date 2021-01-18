## @package procesy
#Plik zawiera klasę procesu. Inicjalizuje się ją podając:
#    - PID
#    - czas_przybycia procesu
#    - czas wykonania


## Klasa procesu
class Proces:

    ##Funkcja inicjalizująca Proces, należy podać:
    #    - PID
    #    - czas_przybycia procesu
    #    - czas wykonania
    def __init__(self, PID, czas_przybycia, czas_wykonywania):
        self.PID = PID
        self.czas_przybycia = czas_przybycia
        self.całkowity_czas_wykonywania = czas_wykonywania
        self.pozostały_czas_wykonywania = czas_wykonywania
        self.czas_oczekiwania = 0
        self.czas_reakcji = 0
        self.byl_wywlaszczony = False
        self.zakończony = False
        self.uśpiony = False

    ## Funkcja która przenosi proces w tryb uśpienia
    def uśpij(self):
        self.byl_wywlaszczony = True
        self.uśpiony = True

    ## Funkcja która wybudza proces
    def wybudź(self):
        self.uśpiony = False

    ## Funkcja która zwraca wyliczony czas wykonywania
    def czas_wykonywania(self):
        return self.całkowity_czas_wykonywania - self.pozostały_czas_wykonywania

    ## Funkcja wykonuje "krok" działania procesu
    def tick(self):
        if self.pozostały_czas_wykonywania > 0:
            self.pozostały_czas_wykonywania -= 1

        if self.pozostały_czas_wykonywania == 0:
            self.zakończony = True

    ## Funkcja wypisuje informacje o procesie na STDOUT
    def info(self):
        print("Info of process with PID =", self.PID, ":")
        print("czas przybycia:", self.czas_przybycia)
        print("czas wykonywania:", self.pozostały_czas_wykonywania)
        print("czas oczekiwania:", self.czas_oczekiwania)
