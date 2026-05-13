from datetime import datetime


"""
Třída zajišťuje textové uživatelské rozhraní (CLI) aplikace.
Zodpovídá za interakci s uživatelem, validaci vstupů a volání logiky systému.
"""
class ConsoleUI:

    """
    Inicializuje UI s odkazem na hlavní systémovou logiku.
    :param system: Instance třídy LeasingSystem (vzor Facade)
    """
    def __init__(self, system):
        self.system = system


    # --- POMOCNÉ VALIDAČNÍ METODY ---

    """
    Zajistí, aby uživatel zadal validní číselný údaj. 
    Předchází pádu aplikace při zadání nečíselných znaků (ValueError).
    """
    def _ziskej_cislo(self, text_vyzvy, desetinne=False):
        while True:
            vstup = input(text_vyzvy)
            try:
                if desetinne:
                    return float(vstup)
                return int(vstup)
            except ValueError:
                print(f"Chyba: Zadaná hodnota '{vstup}' není platné číslo. Zkuste to znovu.")


    """ Zajistí výběr existujícího prvku ze seznamu. Chrání aplikaci před chybou 'Index out of range'. """
    def _ziskej_index(self, seznam, text_vyzvy):
        if not seznam:
            return None
        while True:
            idx = self._ziskej_cislo(text_vyzvy)
            if 0 <= idx < len(seznam):
                return idx
            print(f"Chyba: Vyberte prosím číslo v rozsahu 0 až {len(seznam) - 1}.")


    # --- HLAVNÍ LOGIKA UI ---
    """ Spustí nekonečnou smyčku hlavní nabídky aplikace. """
    def start(self):
        while True:
            print("\n=== SYSTÉM SPRÁVY LEASINGU ===")
            print("1. Nová smlouva (vytvoří Návrh)")
            print("2. Registrace zákazníka")
            print("-" * 30)
            print("3. Zobrazit NÁVRHY smluv")
            print("4. Zobrazit AKTIVNÍ smlouvy")
            print("5. Zobrazit UKONČENÉ smlouvy")
            print("6. ZMĚNIT STAV smlouvy (aktivovat/ukončit)")
            print("-" * 30)
            print("7. Evidence platby")
            print("8. Detail smlouvy a historie plateb")
            print("-" * 30)
            print("9. Zadat servisní prohlídku")
            print("\n")
            print("0. Ukončit")

            volba = input("Vyberte akci: ")

            # Rozcestník volání jednotlivých metod UI
            if volba == "1":
                self.menu_nova_smlouva()
            elif volba == "2":
                self.menu_novy_zakaznik()
            elif volba == "3":
                self.zobrazit_smlouvy_dle_stavu("Navrh")
            elif volba == "4":
                self.zobrazit_smlouvy_dle_stavu("Aktivni")
            elif volba == "5":
                self.zobrazit_smlouvy_dle_stavu("Ukonceno")
            elif volba == "6":
                self.menu_zmena_stavu()
            elif volba == "7":
                self.menu_evidence_platby()
            elif volba == "8":
                self.menu_detail_smlouvy()
            elif volba == "9":
                self.menu_novy_servis()
            elif volba == "0":
                print("Ukončuji...")
                break
            else:
                print("!!! Neplatná volba, zkuste to znovu !!!")


    """ Vytvoří nového zákazníka na základě textových vstupů. """
    def menu_novy_zakaznik(self):
        print("\n--- Registrace zákazníka ---")
        jmeno = input("Jméno: ")
        prijmeni = input("Příjmení: ")
        ucet = input("Číslo účtu: ")
        self.system.pridej_zakaznika(jmeno, prijmeni, ucet)
        print("Zákazník byl úspěšně zaregistrován.")


    """ Průvodce vytvořením smlouvy. Kombinuje výběr objektů (Zákazník, Vozidlo) a volbu strategie. """
    def menu_nova_smlouva(self):
        print("\n--- Vytvoření nové smlouvy ---")

        # Výběr zákazníka s validací indexu
        zakaznici = self.system.ziskej_vsechny_zakazniky()
        if not zakaznici:
            print("Chyba: Nejdříve musíte registrovat zákazníka!")
            return

        for i, z in enumerate(zakaznici):
            print(f"{i}. {z.jmeno} {z.prijmeni}")
        idx_z = self._ziskej_index(zakaznici, "Vyberte index zákazníka: ")
        vybrany_zakaznik = zakaznici[idx_z]

        # Výběr pouze dostupných vozidel
        vozidla = self.system.ziskej_dostupna_vozidla()
        if not vozidla:
            print("Chyba: V nabídce aktuálně není žádné dostupné vozidlo!")
            return

        for i, v in enumerate(vozidla):
            print(f"{i}. {v.znacka} {v.model} ({v.spz})")
        idx_v = self._ziskej_index(vozidla, "Vyberte index vozidla: ")
        vybrane_vozidlo = vozidla[idx_v]

        # Volba finanční strategie (vzor Strategy)
        print("\nVyberte typ leasingu:")
        print("1. Standardní leasing (úrok 5 %)")
        print("2. Akční leasing (úrok 3 %)")
        typ_volba = input("Volba: ")

        from strategies.vypocet_splatky import StandardniVypocet, AkcniVypocet
        vybrana_strategie = AkcniVypocet() if typ_volba == "2" else StandardniVypocet()

        # Validace formátu datumu pomocí datetime.strptime
        while True:
            try:
                datum_od = input("Datum začátku (DD.MM.YYYY): ")
                datum_do = input("Datum konce (DD.MM.YYYY): ")
                # Test validity data
                datetime.strptime(datum_od, "%d.%m.%Y")
                datetime.strptime(datum_do, "%d.%m.%Y")
                break
            except ValueError:
                print("Chyba: Datum musí být ve formátu DD.MM.YYYY!")

        smlouva = self.system.vytvor_smlouvu(datum_od, datum_do, vybrany_zakaznik, vybrane_vozidlo, vybrana_strategie)
        print("\n")
        print(f"Smlouva ID {smlouva.id} úspěšně vytvořena v režimu NÁVRH!")
        print(f"Měsíční splátka: {smlouva.mesicni_splatka:.2f} Kč")


    """ Vypíše seznam smluv filtrovaný podle jejich aktuálního stavu. """
    def zobrazit_smlouvy_dle_stavu(self, stav_kod):
        titulky = {"Navrh": "NÁVRHY SMLUV", "Aktivni": "AKTUÁLNÍ LEASINGY", "Ukonceno": "ARCHIV"}
        print(f"\n--- {titulky.get(stav_kod)} ---")
        smlouvy = self.system.ziskej_smlouvy_dle_stavu(stav_kod)
        if not smlouvy:
            print("Žádné smlouvy nenalezeny.")
            return
        for s in smlouvy:
            print(f"ID: {s.id} | {s.zakaznik.prijmeni} - {s.vozidlo.znacka}")


    """ Umožňuje uživateli aktivovat nebo ukončit existující smlouvu (vzor State). """
    def menu_zmena_stavu(self):
        print("\n--- Změna stavu smlouvy ---")
        smlouvy = self.system.ziskej_vsechny_smlouvy()
        if not smlouvy: return print("Žádné smlouvy k dispozici.")

        for i, s in enumerate(smlouvy):
            print(f"{i}. {s.zakaznik.prijmeni} - {s.vozidlo.znacka} (Stav: {s.ziskej_stav_nazev()})")

        idx_s = self._ziskej_index(smlouvy, "Vyberte index smlouvy: ")
        smlouva = smlouvy[idx_s]

        print("1. Aktivovat, 2. Ukončit")
        akce = input("Volba: ")
        if akce == "1":
            smlouva.aktivovat()
        elif akce == "2":
            smlouva.ukoncit()
        else:
            print("Neplatná akce.")


    """ Zaznamená platbu k vybrané smlouvě. """
    def menu_evidence_platby(self):
        print("\n--- Evidence platby ---")
        smlouvy = self.system.ziskej_vsechny_smlouvy()
        if not smlouvy: return

        for i, s in enumerate(smlouvy):
            print(f"{i}. {s.zakaznik.prijmeni} - {s.vozidlo.znacka} ({s.ziskej_stav_nazev()})")

        idx_s = self._ziskej_index(smlouvy, "Vyberte index smlouvy: ")
        smlouva = smlouvy[idx_s]
        castka = self._ziskej_cislo("Zadejte částku platby: ", desetinne=True)

        # Volání logiky s návratovou hodnotou pro informování uživatele
        if self.system.evidovat_platbu(smlouva, castka):
            print("Platba zaevidována.")
        else:
            print("Platba zamítnuta (špatný stav smlouvy).")


    """ Zobrazí kompletní informace o smlouvě včetně finanční bilance a historie. """
    def menu_detail_smlouvy(self):
        smlouvy = self.system.ziskej_vsechny_smlouvy()
        if not smlouvy: return
        for i, s in enumerate(smlouvy):
            print(f"{i}. {s.zakaznik.prijmeni} - {s.vozidlo.znacka}")

        idx_s = self._ziskej_index(smlouvy, "Vyberte index smlouvy: ")
        s = smlouvy[idx_s]

        print(f"\nDETAIL SMLOUVY ID: {s.id} | STAV: {s.ziskej_stav_nazev()}")
        print(f"Vozidlo: {s.vozidlo.znacka} {s.vozidlo.model} | Zákazník: {s.zakaznik.prijmeni}")
        print(f"Splátka: {s.mesicni_splatka:.2f} Kč")
        print("-" * 20)
        print("PLATEBNÍ HISTORIE:")
        for p in s.seznam_plateb: print(f"  {p}")
        print("-" * 20)
        # Výpočty delegované na model Smlouva
        print(f"Zaplaceno: {s.ziskej_zaplaceno_celkem():.2f} Kč | Zbývá: {s.ziskej_zbyva_doplatit():.2f} Kč")

    """ Umožňuje přidat servisní záznam k vozidlu pod konkrétní smlouvou. """
    def menu_novy_servis(self):
        smlouvy = self.system.ziskej_vsechny_smlouvy()
        if not smlouvy: return
        for i, s in enumerate(smlouvy):
            print(f"{i}. {s.zakaznik.prijmeni} - {s.vozidlo.znacka}")

        idx_s = self._ziskej_index(smlouvy, "Vyberte index smlouvy: ")
        smlouva = smlouvy[idx_s]

        popis = input("Popis servisu: ")
        km = self._ziskej_cislo("Stav tachometru: ")

        from models.servisni_prohlidka import ServisniProhlidka
        if smlouva.pridej_servisni_prohlidku(ServisniProhlidka(popis, km)):
            print("Servis uložen.")
        else:
            print("Chyba při ukládání.")