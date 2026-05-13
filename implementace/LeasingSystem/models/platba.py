from datetime import date


"""
Třída reprezentující finanční transakci (splátku) v rámci leasingové smlouvy.
Uchovává informace o zaplacené částce a datu přijetí platby.
"""
class Platba:
    """
    Inicializuje novou instanci platby.

    :param castka: Hodnota zaplacené částky v Kč.
    :param datum: Datum provedení platby. Pokud není zadáno, použije se aktuální den.
    """
    def __init__(self, castka: float, datum: date = None):
        self.castka = castka
        # Pokud datum není specifikováno, automaticky se nastaví dnešní datumc
        self.datum = datum if datum else date.today()


    """
    Vrací textovou reprezentaci platby pro snadný výpis v uživatelském rozhraní.
    Formátuje datum do čitelné podoby.

    :return: String s informacemi o částce a datu.
    """
    def __str__(self):
        # Formátování data na DD.MM.YYYY
        datum_format = self.datum.strftime("%d.%m.%Y")
        return f"Platba: {self.castka:,.2f} Kč ze dne {datum_format}"