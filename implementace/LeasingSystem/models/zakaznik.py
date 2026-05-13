"""
Třída reprezentuje klienta leasingové společnosti.
Uchovává identifikační údaje a spravuje kolekci všech smluv, které zákazník v systému uzavřel.
"""
class Zakaznik:
    """
    Inicializuje novou instanci zákazníka.

    :param jmeno: Křestní jméno klienta
    :param prijmeni: Příjmení klienta
    :param ucet: Číslo bankovního účtu pro platební styk
    """
    def __init__(self, jmeno: str, prijmeni: str, ucet: str):
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.ucet = ucet
        self.smlouvy = []


    """
    Vrací textovou reprezentaci zákazníka pro výpisy v konzoli.

    :return: Formátovaný řetězec se jménem a číslem účtu.
    """
    def __str__(self):
        return f"{self.jmeno} {self.prijmeni} (Účet: {self.ucet})"