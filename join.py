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

for sale in sales_data:
    id = sale["id"]
    items = shop_cursor.execute(
        f"""
            SELECT * FROM produkt 
            JOIN sprzedaz_produkt ON produkt.id = sprzedaz_produkt.produkt_id
            WHERE sprzedaz_produkt.sprzedaz_id = {id}
        """
    ).fetchall()
    for item in items:
        print(f"{item['typ']}, {item['przeznaczenie']}, {item['cena']}")


"""
    CREATE TABLE IF NOT EXISTS sklep (
        id INTEGER PRIMARY KEY,
        lokalizacja VARCHAR(255)
    );
"""

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

"""
    CREATE TABLE IF NOT EXISTS produkt (
        id INTEGER PRIMARY KEY,
        typ TEXT,
        cena INTEGER,
        przeznaczenie TEXT
    );
"""


fish_conn.close()
shop_conn.close()
weather_conn.close()
