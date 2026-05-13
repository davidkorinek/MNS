from states.stav_smlouvy import StavNavrh
from datetime import datetime

"""
Třída reprezentuje jádro leasingového systému – konkrétní smlouvu.
Implementuje vzor State pro řízení životního cyklu (Návrh, Aktivní, Ukončeno)
a využívá vzor Strategy pro flexibilní výpočet splátek.
"""
class Smlouva:
    """
    Inicializuje novou leasingovou smlouvu.

    :param id_smlouvy: Unikátní identifikátor smlouvy
    :param datum_od: Počátek platnosti (formát DD.MM.YYYY)
    :param datum_do: Konec platnosti (formát DD.MM.YYYY)
    :param zakaznik: Instance třídy Zakaznik
    :param vozidlo: Instance třídy Vozidlo
    :param cena_vozidla: Pořizovací cena vozu pro výpočet leasingu
    :param strategie: Objekt implementující algoritmus výpočtu splátek (vzor Strategy)
    """
    def __init__(self, id_smlouvy, datum_od, datum_do, zakaznik, vozidlo, cena_vozidla, strategie):
        self.id = id_smlouvy
        self.datum_od = datum_od
        self.datum_do = datum_do
        self.zakaznik = zakaznik
        self.vozidlo = vozidlo
        self.cena_vozidla = cena_vozidla
        self.strategie = strategie
        self._stav = StavNavrh()

        # Interní inicializace seznamů pro zachování historie
        self.seznam_plateb = []
        self.seznam_prohlidek = []

        # Výpočet délky leasingu pro potřeby finanční matematiky
        d1 = datetime.strptime(datum_od, "%d.%m.%Y")
        d2 = datetime.strptime(datum_do, "%d.%m.%Y")
        pocet_dni = (d2 - d1).days
        self.pocet_mesicu = max(1, round(pocet_dni / 30.44))  # zajistí aspoň 1 měsíc

        # Nastavení počátečního stavu životního cyklu
        self._stav = StavNavrh()

        # Výpočet splátky dle zvolené finanční strategie
        self.mesicni_splatka = self.strategie.vypocitej(self.cena_vozidla, self.pocet_mesicu)


    """Vrací aktuální objekt stavu smlouvy."""
    @property
    def stav(self):
        return self._stav


    """ Umožňuje bezpečný přechod mezi stavy. Tento setter je využíván konkrétními stavy (ConcreteStates). """
    @stav.setter
    def stav(self, novy_stav):
        self._stav = novy_stav


    """ Pokusí se aktivovat smlouvu. Logika schválení a přechodu je delegována na aktuální stav. """
    def aktivovat(self):
        self._stav.aktivovat(self)


    """ Pokusí se ukončit smlouvu. Logika vypořádání je delegována na aktuální stav. """
    def ukoncit(self):
        self._stav.ukoncit(self)


    """Vrací lidsky čitelný název aktuálního stavu."""
    def ziskej_stav_nazev(self):
        return self._stav.ziskej_nazev()


    """
    Eviduje novou splátku. Kontrola, zda lze v aktuální fázi platbu přijmout, provádí stav.
        
    :return: True, pokud byla platba přijata, jinak False.
    """
    def pridej_platbu(self, platba):
        return self._stav.pridej_platbu(self, platba)


    """Vypočítá sumu všech úspěšně zaevidovaných plateb."""
    def ziskej_zaplaceno_celkem(self):
        return sum(p.castka for p in self.seznam_plateb)


    """
    Vypočítá zbývající dluh na základě celkové ceny leasingu a plateb.
    :return: Částka v Kč, která zbývá do úplného splacení.
    """
    def ziskej_zbyva_doplatit(self):
        celkova_cena = self.mesicni_splatka * self.pocet_mesicu
        zaplaceno = self.ziskej_zaplaceno_celkem()
        return max(0, celkova_cena - zaplaceno)


    """ Zaznamená servisní úkon k vozidlu v rámci této smlouvy. Povolení zápisu závisí na aktuálním stavu smlouvy. """
    def pridej_servisni_prohlidku(self, prohlidka):
        return self._stav.pridej_servisni_prohlidku(self, prohlidka)