from datetime import date
import sqlite3

fish_conn = sqlite3.connect("fish.db")
fish_conn.row_factory = sqlite3.Row
shop_conn = sqlite3.connect("shop.db")
shop_conn.row_factory = sqlite3.Row
weather_conn = sqlite3.connect("weather.db")
weather_conn.row_factory = sqlite3.Row
warehouse_conn = sqlite3.connect("data_warehouse.db")
warehouse_conn.row_factory = sqlite3.Row


fish_cursor = fish_conn.cursor()
shop_cursor = shop_conn.cursor()
weather_cursor = weather_conn.cursor()
warehouse_cursor = warehouse_conn.cursor()

fish_data = fish_cursor.execute("SELECT * FROM ryby").fetchall()
warehouse_cursor.executemany(
    """
        INSERT OR IGNORE INTO ryby (id, gatunek, typ, poczatek_okresu, koniec_okresu)
        VALUES (?, ?, ?, ?, ?)
    """,
    fish_data
)
warehouse_conn.commit()


shop_data = shop_cursor.execute("""SELECT * FROM sklep""").fetchall()
warehouse_cursor.executemany(
    """
        INSERT OR IGNORE INTO sklep (id, lokalizacja)
        VALUES (?, ?)
    """,
    shop_data
)
warehouse_conn.commit()


#produkt_data = shop_cursor.execute("""SELECT * FROM produkt""").fetchall()
# values = [(item['id'], item['typ'], item['cena'], item['przeznaczenie']) for item in produkt_data]

# warehouse_cursor.executemany(
#     """
#         INSERT OR IGNORE INTO produkt (id, typ, cena, przeznaczenie)
#         VALUES (?, ?, ?, ?)
#     """,
#     values
# )
# warehouse_conn.commit()


# weather_data = weather_cursor.execute(
#     """
#         SELECT * FROM pomiar
#         JOIN stacje ON pomiar.station_id = stacje.id
#         JOIN wartosci ON pomiar.id = wartosci.pomiar_id
#     """
#     ).fetchall()



# for record_index in range(0, len(weather_data), 5):
#     record = weather_data[record_index]
#     data_pomiaru = record["data_pomiaru"]
#     data_pomiaru = date.fromisoformat(data_pomiaru)
#     czas_id = ConvertTime(warehouse_cursor, data_pomiaru)

#     rainfall_record = weather_data[record_index + 0]
#     windspeed_record = weather_data[record_index + 1]
#     pressure_record = weather_data[record_index + 2]
#     temperature_record = weather_data[record_index + 3]
#     humidity_record = weather_data[record_index + 4]

#     warehouse_cursor.execute(
#         """
#             INSERT OR IGNORE INTO pogoda (id, id_czasu, lokalizacja, temperatura, wilgotnosc, cisnienie, opady, predkosc_wiatru)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#         """,
#         (
#             record["pomiar_id"],
#             czas_id,
#             record["name"],
#             temperature_record["wartosc"],
#             humidity_record["wartosc"],
#             pressure_record["wartosc"],
#             rainfall_record["wartosc"],
#             windspeed_record["wartosc"]
#         )
#     )
#     warehouse_conn.commit()

# values = [(item['id'], item['kwota_sprzedazy'], item['sklep_id'],) for item in sales_data]
# warehouse_cursor.executemany(
# """
#     INSERT OR IGNORE INTO sprzedaz (id, kwota, id_sklepu)
#     VALUES (?, ?, ?)
# """,
# values
# )

# warehouse_conn.commit()

# sprzedaz_produkt_data = shop_cursor.execute(
# """
#     SELECT * FROM sprzedaz_produkt
# """).fetchall()

# warehouse_cursor.executemany(
# """
#     INSERT OR IGNORE INTO sprzedaz_produkt (sprzedaz_id, produkt_id)
#     VALUES (?, ?)
# """,
# [(item['sprzedaz_id'], item['produkt_id']) for item in sprzedaz_produkt_data]
# )
# warehouse_conn.commit()


### DONE

def ConvertTime (cursor: sqlite3.Cursor, d: date) -> int:
    rok = d.year
    miesiac = d.month
    kwartal = (d.month - 1) // 3 + 1
    tydzien = d.isocalendar()[1]
    

    cursor.execute(
        """
            INSERT OR IGNORE INTO czas (data, rok, kwartal, miesiac, tydzien)
            VALUES (?, ?, ?, ?, ?)
        """,
        (d, rok, kwartal, miesiac, tydzien)
    )

    cursor.connection.commit()
    return cursor.lastrowid

#################################################################################


sales_data = shop_cursor.execute(
"""
    SELECT * FROM sprzedaz
    JOIN sprzedaz_produkt ON sprzedaz.id = sprzedaz_produkt.sprzedaz_id
""").fetchall()


for sale in sales_data:  # Pętla 1
    id = sale["id"]
    
    items = shop_cursor.execute(
        f"""
            SELECT * FROM produkt 
            JOIN sprzedaz_produkt ON produkt.id = sprzedaz_produkt.produkt_id
            WHERE sprzedaz_produkt.sprzedaz_id = {id}
        """
    ).fetchall()

    quantity = 0

    for item in items:  # Pętla 2
        quantity += item["ilosc_sprzedana"]
        print(f"{item['typ']}, {item['przeznaczenie']}, {item['cena']}")

    print(f"Ilość: {quantity})")

# Do tego dane są w shop_data



warehouse_conn.commit()

fish_conn.close()
shop_conn.close()
weather_conn.close()
warehouse_conn.close()