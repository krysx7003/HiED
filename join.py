import sqlite3

fish_conn = sqlite3.connect("fish.db")
fish_conn.row_factory = sqlite3.Row
shop_conn = sqlite3.connect("shop.db")
shop_conn.row_factory = sqlite3.Row
weather_conn = sqlite3.connect("weather.db")
weather_conn.row_factory = sqlite3.Row

fish_cursor = fish_conn.cursor()
shop_cursor = shop_conn.cursor()
weather_cursor = weather_conn.cursor()

# fish_data = fish_cursor.execute("SELECT * FROM ryby").fetchone()

sales_data = shop_cursor.execute(
    """
        SELECT * FROM sprzedaz 
    """
).fetchall()
# weather_data = weather_cursor.execute(
#     """
#         SELECT * FROM pomiar
#         JOIN stacje ON pomiar.station_id = stacje.id
#         JOIN wartosci ON pomiar.id = wartosci.pomiar_id
#     """
# ).fetchone()

shop_data = shop_cursor.execute(
    """
        SELECT * FROM sklep 
    """
).fetchall()

for sale in sales_data:  # Pętla 1
    id = sale["id"]
    items = shop_cursor.execute(
        f"""
            SELECT * FROM produkt 
            JOIN sprzedaz_produkt ON produkt.id = sprzedaz_produkt.produkt_id
            WHERE sprzedaz_produkt.sprzedaz_id = {id}
        """
    ).fetchall()

    amount = sale["kwota_sprzedazy"]
    quantity = 0

    for item in items:  # Pętla 2
        quantity = item["ilosc_sprzedana"]
        print(f"{item['typ']}, {item['przeznaczenie']}, {item['cena']}")

    print(f"Ilość: {quantity}, kwota: {amount}")

# Do tego dane są w shop_data
"""
    CREATE TABLE IF NOT EXISTS sklep (
        id INTEGER PRIMARY KEY,
        lokalizacja TEXT PRIMARY KEY
    );
"""

# Do tego dane są w pętli 1 zmienna sale
"""
    CREATE TABLE IF NOT EXISTS sprzedaz (
        id_sklepu INTEGER PRIMARY KEY,
        id_produktu INTEGER PRIMARY KEY,
        id_czasu INTEGER PRIMARY KEY,
        kwota INTEGER,
        ilosc INTEGER
        FOREIGN KEY (id_sklepu) REFERENCES sklep(id)
        FOREIGN KEY (id_produktu) REFERENCES produkt(id)
        FOREIGN KEY (id_czasu) REFERENCES czas(id)
    );
"""

# Do tego dane są w pętli 2 zmienna item
"""
    CREATE TABLE IF NOT EXISTS produkt (
        id INTEGER PRIMARY KEY,
        typ TEXT,
        cena INTEGER,
        przeznaczenie TEXT
    );
"""

# Do tego dane są w pętli 1 zmienna sale["data"]
"""
    CREATE TABLE IF NOT EXISTS czas(
        id INTEGER PRIMARY KEY,
        data DATE,
        rok INTEGER,
        kwartal INTEGER,
        miesiac INTEGER,
        tydzien INTEGER
    );
"""

# Ryby po prostu przekopiować
"""
    CREATE TABLE IF NOT EXISTS ryby (
        id INTEGER PRIMARY KEY,
        gatunek TEXT NOT NULL,
        typ TEXT NOT NULL,
        poczatek_okresu INTEGER,
        koniec_okresu INTEGER
    );
"""

# Do tego dane są w weather_data
"""
    CREATE TABLE IF NOT EXISTS pogoda(
        id INTEGER PRIMARY KEY,
        id_czasu INTEGER,
        lokalizacja TEXT,
        opady FLOAT,
        predkosc_wiatru FLOAT,
        cisnienie FLOAT,
        temperatura FLOAT,
        wilgotnosc FLOAT
        FOREIGN KEY (id_czasu) REFERENCES czas(id)
        FOREIGN KEY (lokalizacja) REFERENCES sklep(lokalizacja)
    );

"""

fish_conn.close()
shop_conn.close()
weather_conn.close()
