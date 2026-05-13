from abc import ABC, abstractmethod

"""
Abstraktní základní třída pro návrhový vzor State.
Definuje rozhraní, které musí všechny konkrétní stavy implementovat.
"""
class StavSmlouvy(ABC):
    """Vrací textovou reprezentaci stavu pro UI."""
    @abstractmethod
    def ziskej_nazev(self):
        pass


""" Reprezentuje počáteční fázi smlouvy. V této fázi je smlouva pouze rozpracovaná a neprobíhají k ní žádné platby. """
class StavNavrh(StavSmlouvy):
    def __init__(self):
        self.kod = "Navrh"

    def ziskej_nazev(self):
        return "Návrh"


    """ Pokusí se převést smlouvu do aktivního stavu. Kontroluje dostupnost vozidla a provádí jeho blokaci. """
    def aktivovat(self, smlouva):
        if not smlouva.vozidlo.dostupne:
            print(f"Chyba: Vozidlo {smlouva.vozidlo.spz} je již pronajato jinému klientovi!")
            return

        print("Schvaluji návrh a aktivuji leasing...")

        # Vozidlo přestává být nabízeno ostatním
        smlouva.vozidlo.dostupne = False

        from states.stav_smlouvy import StavAktivni
        smlouva.stav = StavAktivni()


    """ Návrh nelze ukončit, lze jej pouze aktivovat. """
    def ukoncit(self, smlouva):
        print("Chyba: Návrh nelze ukončit.")


    """ Platby nejsou v režimu návrhu povoleny. """
    def pridej_platbu(self, smlouva, platba):
        print("Chyba: Nelze evidovat platbu k neschválenému návrhu smlouvy.")
        return False

    def pridej_servisni_prohlidku(self, smlouva, prohlidka):
        """Servis se eviduje až u reálně provozovaných vozidel."""
        print("Chyba: K návrhu smlouvy nelze přidat servisní záznam.")
        return False


""" Reprezentuje běžící leasingovou smlouvu. Umožňuje evidenci plateb, servisních prohlídek a vypořádání majetku. """
class StavAktivni(StavSmlouvy):
    def __init__(self):
        self.kod = "Aktivni"

    def ziskej_nazev(self):
        return "Aktivní"

    def aktivovat(self, smlouva):
        print("Chyba: Smlouva již je aktivní.")


    """ Provádí logiku ukončení leasingu. Rozhoduje o vrácení/odkoupení vozidla na základě zbývajícího dluhu. """
    def ukoncit(self, smlouva):
        zbytek = smlouva.ziskej_zbyva_doplatit()
        print(f"\nUkončuji smlouvu ID: {smlouva.id}")

        # Scénář řádného doplacení
        if zbytek <= 0:
            smlouva.vozidlo.dostupne = False
            print("Výsledek: Leasing řádně splacen. Vozidlo přechází do vlastnictví zákazníka.")

        # Scénář předčasného ukončení nebo dluhu
        else:
            smlouva.vozidlo.dostupne = True
            print(f"Výsledek: Smlouva ukončena s dluhem {zbytek:.2f} Kč. Vozidlo se vrací do nabídky.")

        from states.stav_smlouvy import StavUkonceno
        smlouva.stav = StavUkonceno()


    """ Ukládá platbu a potvrzuje její přijetí. """
    def pridej_platbu(self, smlouva, platba):
        smlouva.seznam_plateb.append(platba)
        print(f"Platba ve výši {platba.castka} Kč byla úspěšně přidána k aktivní smlouvě.")
        return True


    """ Ukládá servisní záznam a aktualizuje stav tachometru vozidla. """
    def pridej_servisni_prohlidku(self, smlouva, prohlidka):
        smlouva.seznam_prohlidek.append(prohlidka)
        smlouva.vozidlo.kilometry = prohlidka.kilometry
        return True


""" Reprezentuje archivovanou smlouvu. Zamezuje jakýmkoliv dalším změnám nebo finančním operacím. """
class StavUkonceno(StavSmlouvy):
    def __init__(self):
        self.kod = "Ukonceno"

    def ziskej_nazev(self):
        return "Ukončeno"

    def aktivovat(self, smlouva):
        print("Chyba: Již ukončenou smlouvu nelze znovu aktivovat.")

    def ukoncit(self, smlouva):
        print("Chyba: Smlouva již je v archivu (ukončená).")

    def pridej_platbu(self, smlouva, platba):
        print("Chyba: Smlouva je již ukončena. Další platby nejsou povoleny.")
        return False

    def pridej_servisni_prohlidku(self, smlouva, prohlidka):
        print("Chyba: K ukončené smlouvě nelze přidat servisní záznam.")
        return False