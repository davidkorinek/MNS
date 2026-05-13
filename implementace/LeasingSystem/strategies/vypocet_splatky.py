from abc import ABC, abstractmethod

"""
Abstraktní základ pro různé algoritmy výpočtu měsíčních splátek.
Implementuje návrhový vzor Strategy.
"""
class StrategieVypoctu(ABC):
    """ Metoda pro výpočet výše měsíční splátky. """
    @abstractmethod
    def vypocitej(self, zakladni_cena, pocet_mesicu):
        pass

""" Běžný leasingový produkt se standardní úrokovou sazbou 5%. """
class StandardniVypocet(StrategieVypoctu):
    def vypocitej(self, zakladni_cena, pocet_mesicu):
        return (zakladni_cena * 1.05) / pocet_mesicu

""" Zvýhodněný leasingový produkt se sníženou úrokovou sazbou 3%. """
class AkcniVypocet(StrategieVypoctu):
    def vypocitej(self, zakladni_cena, pocet_mesicu):
        return (zakladni_cena * 1.03) / pocet_mesicu