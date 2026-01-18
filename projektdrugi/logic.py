from zbiornik import Zbiornik
from rura import Rura

class ProcessLogic:
    def __init__(self):
        self.zadana_temp = 0
        self.speed = 0.8
        self.cel_produktu = 100.0
        
        self.z1 = Zbiornik(100, 70, "Surowiec")
        self.z2 = Zbiornik(400, 70, "Bufor")
        self.z3 = Zbiornik(400, 360, "Mikser")
        self.z4 = Zbiornik(750, 360, "Produkt")
        
        self.zbiorniki = [self.z1, self.z2, self.z3, self.z4]
        
        self.rury = [
            Rura([self.z1.punkt_wyjscia_dol(), (145, 250), (445, 250), self.z2.punkt_wejscia_gora()]),
            Rura([self.z2.punkt_wyjscia_dol(), self.z3.punkt_wejscia_gora()]),
            Rura([self.z3.punkt_wyjscia_dol(), (445, 560), (795, 560), self.z4.punkt_wyjscia_dol()])
        ]

    def calculate_step(self):
        s = self.speed

        #leje z Z1 do bufora dopóki w z1 coś jest
        if self.z1.poziom > 0.1:
            self.rury[0].czy_plynie = True
            self.z1.poziom -= s
            self.z2.poziom += s
        else:
            self.rury[0].czy_plynie = False
            self.z1.poziom = 0.0

        #leje z bufora do miksera dopóki suma w z3 i z4 nie osiągnie celu
        #nieważne czy z1 jeszcze leje czy już skoncylo
        obecnie_w_produkcji = self.z3.poziom + self.z4.poziom
        
        if self.z2.poziom > 0.1 and obecnie_w_produkcji < self.cel_produktu:
            self.rury[1].czy_plynie = True
            self.z2.poziom -= s
            self.z3.poziom += s
        else:
            self.rury[1].czy_plynie = False

        #pompuje do z4 aż do osiągnięcia celu
        if self.z3.poziom > 0.1 and self.z4.poziom < self.cel_produktu:
            self.rury[2].czy_plynie = True
            self.z3.poziom -= s * 0.5
            self.z4.poziom += s * 0.5
        else:
            self.rury[2].czy_plynie = False
            if self.z3.poziom <= 0.1: self.z3.poziom = 0.0

    def has_alarm(self):
        return any(z.poziom > 95 for z in self.zbiorniki[1:])