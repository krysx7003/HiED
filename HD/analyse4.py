import sqlite3

import matplotlib.pyplot as plt

warehouse_conn = sqlite3.connect("data_warehouse.db")
warehouse_conn.row_factory = sqlite3.Row
warehouse_cursor = warehouse_conn.cursor()

query_ryby = "SELECT typ, poczatek_okresu, koniec_okresu FROM ryby"
ryby_data = warehouse_cursor.execute(query_ryby).fetchall()

query1 = """
    SELECT 
        czas.tydzien,
        ryby.typ as typ_ryby,
        ryby.poczatek_okresu,
        ryby.koniec_okresu,
        CASE 
            WHEN czas.tydzien BETWEEN ryby.poczatek_okresu AND ryby.koniec_okresu THEN 'okres_ochronny'
            ELSE 'poza_okresem'
        END as status_okresu,
        SUM(sprzedaz.kwota) as suma_sprzedazy,
        COUNT(DISTINCT sprzedaz.id) as liczba_transakcji,
        produkt.typ as produkt_typ
    FROM sprzedaz
    JOIN sklep ON sprzedaz.id_sklepu = sklep.id
    JOIN czas ON sprzedaz.id_czasu = czas.id
    LEFT JOIN sprzedaz_produkt ON sprzedaz.id = sprzedaz_produkt.sprzedaz_id
    LEFT JOIN produkt ON sprzedaz_produkt.produkt_id = produkt.id
    LEFT JOIN ryby ON produkt.przeznaczenie = ryby.typ
    WHERE produkt.przeznaczenie IS NOT NULL  -- tylko sprzęt powiązany z konkretnymi rybami
    GROUP BY czas.tydzien, ryby.typ, status_okresu
    ORDER BY czas.tydzien, ryby.typ
"""

data = warehouse_cursor.execute(query1).fetchall()

analysis_data = {}
for row in data:
    typ_ryby = row["typ_ryby"]
    status = row["status_okresu"]
    tydzien = row["tydzien"]
    sprzedaz = row["suma_sprzedazy"]

    if typ_ryby not in analysis_data:
        analysis_data[typ_ryby] = {
            "okres_ochronny": {"tygodnie": [], "sprzedaz": []},
            "poza_okresem": {"tygodnie": [], "sprzedaz": []},
        }

    analysis_data[typ_ryby][status]["tygodnie"].append(tydzien)
    analysis_data[typ_ryby][status]["sprzedaz"].append(sprzedaz)


fig, axes = plt.subplots(2, figsize=(15, 10))
axes = axes.flatten()

valid_ryby = []
for typ_ryby, data in analysis_data.items():
    okres_ryby = next((r for r in ryby_data if r["typ"] == typ_ryby), None)
    if (
        okres_ryby
        and okres_ryby["poczatek_okresu"] is not None
        and okres_ryby["koniec_okresu"] is not None
    ):
        valid_ryby.append((typ_ryby, data))

for i, (typ_ryby, data) in enumerate(valid_ryby):
    if i >= len(axes):
        break

    ax = axes[i]
    okres_ryby = next((r for r in ryby_data if r["typ"] == typ_ryby), None)
    wszystkie_tygodnie = sorted(
        set(data["okres_ochronny"]["tygodnie"] + data["poza_okresem"]["tygodnie"])
    )

    wszystkie_sprzedaze = []

    for tydzien in wszystkie_tygodnie:
        if tydzien in data["okres_ochronny"]["tygodnie"]:
            idx = data["okres_ochronny"]["tygodnie"].index(tydzien)
            wszystkie_sprzedaze.append(data["okres_ochronny"]["sprzedaz"][idx])
        else:
            idx = data["poza_okresem"]["tygodnie"].index(tydzien)
            wszystkie_sprzedaze.append(data["poza_okresem"]["sprzedaz"][idx])

    ax.bar(wszystkie_tygodnie, wszystkie_sprzedaze, label="Sprzedaż")

    if okres_ryby:
        ax.axvspan(
            okres_ryby["poczatek_okresu"],
            okres_ryby["koniec_okresu"],
            alpha=0.3,
            color="red",
            label="Okres ochronny",
        )

    ax.set_title(f"Sprzedaż sprzętu dla {typ_ryby}")
    ax.set_xlabel("Tydzień")
    ax.set_ylabel("Sprzedaż (PLN)")
    ax.legend()
    ax.grid(True, alpha=0.3)

for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

plt.suptitle("Sprzedaż sprzętu wędkarskiego a okresy ochronne ryb (tygodnie)")
plt.tight_layout()
plt.savefig("analyse4.png")
plt.show()

warehouse_conn.close()
