"""
Třída reprezentující předmět leasingu – vozidlo.
Uchovává technické specifikace, pořizovací cenu a aktuální stav dostupnosti.
"""
class Vozidlo:
    """
    Inicializuje novou instanci vozidla.

    :param spz: Státní poznávací značka (unikátní identifikátor vozu)
    :param znacka: Výrobce vozidla (např. Škoda, Audi)
    :param model: Konkrétní modelová řada
    :param cena_auta: Pořizovací cena, ze které se vypočítává výše leasingu
    """
    def __init__(self, spz, znacka, model, cena_auta):
        self.spz = spz
        self.znacka = znacka
        self.model = model
        self.cena_auta = cena_auta

        # Atribut 'dostupne' slouží k řízení logiky nabídek.
        # True = vozidlo lze přiřadit k nové smlouvě.
        # False = vozidlo je aktuálně v aktivním leasingu nebo již bylo odkoupeno.
        self.dostupne = True


    """
    Vrací uživatelsky přívětivý popis vozidla včetně jeho aktuální dostupnosti.
    Využívá se při výpisu vozového parku v konzoli.
    """
    def __str__(self):
        stav = "Dostupné" if self.dostupne else "Pronajato / Prodáno"
        return f"{self.znacka} {self.model} ({self.spz}) - {stav}"