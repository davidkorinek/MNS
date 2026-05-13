from ui.console_ui import ConsoleUI
from logic.leasing_system import LeasingSystem

"""
Hlavní spouštěcí modul aplikace.
Zajišťuje propojení (Dependency Injection) mezi logickou vrstvou systému 
a prezentační vrstvou (uživatelským rozhraním).
"""
if __name__ == "__main__":

    """ 
    1. Inicializace doménové logiky (Vzor Facade)
    Vytvoří se instance systému, která v sobě drží data o zákaznících, vozidlech a smlouvách.
    """
    system = LeasingSystem()


    """
    2. Inicializace uživatelského rozhraní
    UI dostává referenci na 'system', aby s ním mohlo komunikovat.
    """
    ui = ConsoleUI(system)


    """
    3. Spuštění aplikace
    Vyvolá se nekonečná smyčka menu v konzoli.
    """
    try:
        ui.start()
    except KeyboardInterrupt:
        # Elegantní ošetření ukončení pomocí zkratky Ctrl+C
        print("\nProgram násilně ukončen uživatelem.")