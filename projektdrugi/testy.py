import pytest
from zbiornik import Zbiornik
from rura import Rura

@pytest.fixture
def system_testowy():
    """Przygotowuje zestaw zbiorników do testów (odpowiednik bazy_testowej)"""
    z1 = Zbiornik(0, 0, "Z1")
    z2 = Zbiornik(100, 0, "Z2")
    return [z1, z2]

def test_napelniania_zbiornika(system_testowy):
    """Test prosty: czy poziom się zmienia"""
    z1 = system_testowy[0]
    z1.poziom = 50.0
    assert z1.poziom == 50.0

def test_alarmu_logika(system_testowy):
    """Test sprawdzający warunek alarmu (powyżej 95)"""
    z2 = system_testowy[1]
    z2.poziom = 96.0
    #sprawdzanie czy logika alarmu działa
    czy_alarm = z2.poziom > 95
    assert czy_alarm is True

@pytest.mark.parametrize("poziom_start, ile_dolac, oczekiwany", [
    (10, 20, 30),  # 10 + 20 = 30
    (90, 20, 110), # 90 + 20 = 110
    (0, 5, 5)      # 0 + 5 = 5
])
def test_matematyki_zbiornikow(poziom_start, ile_dolac, oczekiwany, system_testowy):
    """Test wielu przypadków dodawania cieczy (jak test_wielu_przypadkow)"""
    z1 = system_testowy[0]
    z1.poziom = poziom_start
    z1.poziom += ile_dolac
    assert z1.poziom == oczekiwany