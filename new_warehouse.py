import sqlite3

conn = sqlite3.connect("data_warehouse.db")
warehouse_db = conn.cursor()

create_warehouse_db = """

    CREATE TABLE IF NOT EXISTS sklep (
        id INTEGER PRIMARY KEY,
        lokalizacja TEXT UNIQUE
    );
"""
warehouse_db.execute(create_warehouse_db)
# Do tego dane są w pętli 1 zmienna

warehouse_db.execute("DROP TABLE IF EXISTS sprzedaz;")
conn.commit()

create_warehouse_db = """
    CREATE TABLE IF NOT EXISTS sprzedaz (
        id INTEGER PRIMARY KEY,
        id_sklepu INTEGER,
        id_czasu INTEGER,
        kwota INTEGER,
        ilosc INTEGER,
        FOREIGN KEY (id_sklepu) REFERENCES sklep(id),
        FOREIGN KEY (id_czasu) REFERENCES czas(id)
    );
"""
warehouse_db.execute(create_warehouse_db)

# Do tego dane są w pętli 2 zmienna item
create_warehouse_db = """
CREATE TABLE IF NOT EXISTS produkt (
        id INTEGER PRIMARY KEY,
        typ TEXT,
        cena INTEGER,
        przeznaczenie TEXT
    );
"""
warehouse_db.execute(create_warehouse_db)

# Do tego dane są w pętli 1 zmienna sale["data"]
create_warehouse_db = """
CREATE TABLE IF NOT EXISTS czas(
        id INTEGER PRIMARY KEY,
        data DATE,      
        rok INTEGER,
        kwartal INTEGER,
        miesiac INTEGER,
        tydzien INTEGER
    );
"""
warehouse_db.execute(create_warehouse_db)
# Ryby po prostu przekopiować
create_warehouse_db = """
    CREATE TABLE IF NOT EXISTS ryby (
        id INTEGER PRIMARY KEY,
        gatunek TEXT NOT NULL UNIQUE,
        typ TEXT NOT NULL,
        poczatek_okresu INTEGER,
        koniec_okresu INTEGER
    );
"""
warehouse_db.execute(create_warehouse_db)

# Do tego dane są w weather_data
create_warehouse_db = """
    CREATE TABLE IF NOT EXISTS pogoda(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_czasu INTEGER,
        lokalizacja TEXT,
        opady FLOAT,
        predkosc_wiatru FLOAT,
        cisnienie FLOAT,
        temperatura FLOAT,
        wilgotnosc FLOAT,
        FOREIGN KEY (id_czasu) REFERENCES czas(id),
        FOREIGN KEY (lokalizacja) REFERENCES sklep(lokalizacja)
    );
"""
warehouse_db.execute(create_warehouse_db)


create_warehouse_db = """
    CREATE TABLE IF NOT EXISTS sprzedaz_produkt (
        sprzedaz_id INTEGER NOT NULL,
        produkt_id INTEGER NOT NULL,
        FOREIGN KEY (sprzedaz_id) REFERENCES sprzedaz(id),
        FOREIGN KEY (produkt_id) REFERENCES produkt(id),
        PRIMARY KEY (sprzedaz_id, produkt_id)
        );
"""
warehouse_db.execute(create_warehouse_db)


conn.commit()
conn.close()
