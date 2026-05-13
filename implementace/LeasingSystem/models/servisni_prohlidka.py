from datetime import datetime


"""
Třída reprezentující záznam o provedené servisní prohlídce vozidla.
Umožňuje sledovat historii údržby v rámci leasingové smlouvy.
"""
class ServisniProhlidka:
    """
    Inicializuje nový záznam o servisní prohlídce.

    :param popis: Detailní popis provedených úkonů (např. 'Výměna oleje a filtrů')
    :param kilometry: Stav tachometru v době provádění servisu
    """
    def __init__(self, popis, kilometry):
        # Automaticky zaznamená aktuální čas vytvoření záznamu
        self.datum = datetime.now()
        self.popis = popis
        self.kilometry = kilometry


    """
    Vrací formátovaný řetězec pro výpis servisní historie.

    :return: String ve formátu: DD.MM.YYYY - popis (X km)
    """
    def __str__(self):
        datum_format = self.datum.strftime('%d.%m.%Y')
        return f"{datum_format} - {self.popis} ({self.kilometry} km)"