AUTOR: David Kořínek
OS. ČÍSLO: A24B0263P
TÉMA: Leasing Automobilů
ÚLOŽIŠTĚ: https://github.com/davidkorinek/MNS

==============
POPIS SYSTÉMU
==============
Systém pro správu leasingu automobilů slouží k efektivnímu sledování životního cyklu 
leasingových smluv a s nimi spojených objektů. Aplikace umožňuje komplexní evidenci 
zákazníků, vozidel a následné uzavírání smluvních vztahů. 

Klíčové vlastnosti:
- Sledování platební morálky skrze detailní evidenci příchozích plateb.
- Správa technického stavu vozového parku pomocí záznamů o servisních prohlídkách.
- Automatizované řízení stavů smluv (vzor State) a výpočtů (vzor Strategy).

================================
SEZNAM PŘÍPADŮ UŽITÍ (USE CASES)
================================
1. UC01: Vytvořit leasingovou smlouvu – Vytvoření návrhu smlouvy.
2. UC02: Registrovat nového zákazníka – Evidence osobních a kontaktních údajů.
3. UC03: Zobrazit návrhy smlouvy - Výpis detailu všech návrhů smluv.
4. UC04: Zobrazit aktivní smlouvy - Výpis detailu všech aktivních smluv.
5. UC05: Zobrazit uzavřené smlouvy - Výpis detailu všech uzavřených smluv.
6. UC06: Změna stavu smlouvy - Změna stavu smlouvy (aktivace/ukončení).
7. UC07: Evidence nové platby – Připsání splátky k aktivní smlouvě.
8. UC08: Detail smlouvy a historie plateb – Výpis kompletního detailu vybrané smlouvy.
9. UC09: Zadat servisní prohlídku - Zapsání servisní prohlídky (datum a úkony).

====================
TECHNICKÉ INFORMACE
====================
- Implementační jazyk: Python 3.14
- Architektura: Objektově orientovaný návrh (OOP)
- Použité vzory: State (životní cyklus smlouvy), Strategy (výpočet splátek)
