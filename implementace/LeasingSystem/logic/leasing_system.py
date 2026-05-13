from models.vozidlo import Vozidlo
from models.smlouva import Smlouva
from models.zakaznik import Zakaznik
from strategies.vypocet_splatky import StandardniVypocet


"""
Třída reprezentující hlavní logiku leasingového systému.
Slouží jako fasáda (Facade) pro správu zákazníků, vozidel a smluv.
"""
class LeasingSystem:
    """ Iniciální hodnoty pro snažší testování """
    def __init__(self):
        self.zakaznici = [
            Zakaznik("Karel", "Jonák", "12345678/0300"),
            Zakaznik("Michal", "Soukup", "98765432/3030"),
            Zakaznik("Jana", "Němcová", "10203040/0300")
        ]

        self.vozidla = [
            Vozidlo("4P5 1234", "Škoda", "Octavia", 609900),
            Vozidlo("2B8 5678", "Volkswagen", "Golf", 677900),
            Vozidlo("1A2 9999", "Audi", "A5", 1282900)
        ]

        self.smlouvy = []

    """
    Vytvoří a zaregistruje nového zákazníka do systému.

    :param jmeno: Křestní jméno zákazníka
    :param prijmeni: Příjmení zákazníka
    :param ucet: Číslo bankovního účtu pro splátky
    :return: Instance nově vytvořeného zákazníka
    """
    def pridej_zakaznika(self, jmeno, prijmeni, ucet):
        novy = Zakaznik(jmeno, prijmeni, ucet)
        self.zakaznici.append(novy)
        return novy


    """
    Vytvoří novou leasingovou smlouvu v počátečním stavu 'Návrh'.
    Automaticky generuje ID smlouvy a přiřazuje výpočetní strategii.

    :param datum_od: Datum začátku leasingu (string DD.MM.YYYY)
    :param datum_do: Datum konce leasingu (string DD.MM.YYYY)
    :param zakaznik: Objekt třídy Zakaznik
    :param vozidlo: Objekt třídy Vozidlo
    :param strategie: Výše úroku
    :return: Instance vytvořené smlouvy
    """
    def vytvor_smlouvu(self, datum_od, datum_do, zakaznik, vozidlo, strategie):
        """
        Vytvoří novou smlouvu s konkrétní strategií výpočtu úroku.
        """
        cena_auta = vozidlo.cena_auta
        nove_id = len(self.smlouvy) + 1

        nova_smlouva = Smlouva(nove_id, datum_od, datum_do, zakaznik, vozidlo, cena_auta, strategie)
        self.smlouvy.append(nova_smlouva)
        return nova_smlouva


    """Vrací seznam všech registrovaných zákazníků."""
    def ziskej_vsechny_zakazniky(self):
        return self.zakaznici


    """Vrací seznam všech dostupných vozidel v systému."""
    def ziskej_vsechna_vozidla(self):
        return self.vozidla

    """Vrátí seznam vozidel, která nejsou aktuálně pronajatá."""
    def ziskej_dostupna_vozidla(self):
        return [v for v in self.vozidla if v.dostupne]

    """Vrací seznam smluv, které jsou aktuálně ve stavu 'Aktivní'."""
    def ziskej_aktivni_smlouvy(self):
        return self.ziskej_smlouvy_dle_stavu("Aktivni")


    """Vrací kompletní seznam všech smluv bez ohledu na stav."""
    def ziskej_vsechny_smlouvy(self):
        return self.smlouvy


    """
    Zaznamená novou příchozí platbu k dané smlouvě.
    Proces připsání je řízen vnitřním stavem smlouvy (vzor State).

    :param smlouva: Objekt smlouvy, ke které platba patří
    :param castka: Zaplacená částka v Kč
    :return: True, pokud byla platba přijata, jinak False
    """
    def evidovat_platbu(self, smlouva, castka):
        from models.platba import Platba
        nova_platba = Platba(castka)
        return smlouva.pridej_platbu(nova_platba)


    """
    Vyfiltruje smlouvy podle zadaného kódu stavu.

    :param stav_kod: Identifikátor stavu (např. 'Navrh', 'Aktivni', 'Ukonceno')
    :return: Seznam vyfiltrovaných smluv
    """
    def ziskej_smlouvy_dle_stavu(self, stav_kod):
        return [s for s in self.smlouvy if s.stav.kod == stav_kod]