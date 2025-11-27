import math
import sqlite3

import matplotlib.pyplot as plt

warehouse_conn = sqlite3.connect("data_warehouse.db")
warehouse_conn.row_factory = sqlite3.Row
warehouse_cursor = warehouse_conn.cursor()

query1 = """
    SELECT sprzedaz.id_sklepu, sklep.lokalizacja,
           AVG(produkt.cena) AS cena_avg,
           czas.tydzien,
           SUM(pogoda.opady) AS opady_sum,
           AVG(pogoda.predkosc_wiatru) AS predkosc_wiatru_avg,
           AVG(pogoda.cisnienie) AS cisnienie_avg,
           AVG(pogoda.temperatura) AS temperatura_avg,
           AVG(pogoda.wilgotnosc) AS wilgotnosc_avg
    FROM sprzedaz
    JOIN sklep ON sprzedaz.id_sklepu = sklep.id
    LEFT JOIN czas ON sprzedaz.id_czasu = czas.id
    LEFT JOIN pogoda ON pogoda.id_czasu = czas.id
    LEFT JOIN sprzedaz_produkt ON sprzedaz.id = sprzedaz_produkt.sprzedaz_id
    LEFT JOIN produkt ON sprzedaz_produkt.produkt_id = produkt.id
    GROUP BY czas.tydzien, sprzedaz.id_sklepu
"""

data = warehouse_cursor.execute(query1).fetchall()

shops = {}
for row in data:
    sklep_id = row["id_sklepu"]
    tydzien = row["tydzien"]
    cena = row["cena_avg"]
    opady = row["opady_sum"]

    if sklep_id not in shops:
        shops[sklep_id] = {
            "tydzien": [],
            "cena": [],
            "opady": [],
            "predkosc_wiatru_avg": [],
            "cisnienie_avg": [],
            "temperatura_avg": [],
            "wilgotnosc_avg": [],
        }

    shops[sklep_id]["tydzien"].append(tydzien)
    shops[sklep_id]["cena"].append(cena)
    shops[sklep_id]["opady"].append(opady)
    shops[sklep_id].setdefault("predkosc_wiatru_avg", []).append(row["predkosc_wiatru_avg"])
    shops[sklep_id].setdefault("cisnienie_avg", []).append(row["cisnienie_avg"])
    shops[sklep_id].setdefault("temperatura_avg", []).append(row["temperatura_avg"])
    shops[sklep_id].setdefault("wilgotnosc_avg", []).append(row["wilgotnosc_avg"])

num_shops = len(shops)
cols = 3
rows = math.ceil(num_shops / cols)

fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), sharey=False)
axes = axes.flatten()

for ax, (sklep_id, values) in zip(axes, shops.items()):
    tygodnie = values["tydzien"]
    cena = values["cena"]
    opady = values["opady"]

    # Bar chart for sales
    ax.bar(tygodnie, cena, color="cornflowerblue", label="Sprzedaż")
    ax.set_title(f"Sklep {sklep_id}")
    ax.set_xlabel("Tydzień")
    ax.set_ylabel("Cena towaru (PLN)")
    ax.grid(axis="y")

    # Secondary y-axis
    ax2 = ax.twinx()
    ax2.plot(tygodnie, opady, color="orange", marker="x", label="Opady")
    ax2.set_ylabel("Opady (mm)")

    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(handles1 + handles2, labels1 + labels2, loc="upper right")

# Hide unused subplots
for ax in axes[len(shops) :]:
    ax.set_visible(False)

plt.suptitle("Sprzedaż i opady w poszczególnych sklepach")
plt.tight_layout()
plt.savefig("analyse3_opady.png")
plt.show(block=False)

fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), sharey=False)
axes = axes.flatten()

for ax, (sklep_id, values) in zip(axes, shops.items()):
    tygodnie = values["tydzien"]
    cena = values["cena"]
    wiatr = values["predkosc_wiatru_avg"]

    # Bar chart for sales
    ax.bar(tygodnie, cena, color="cornflowerblue", label="Sprzedaż")
    ax.set_title(f"Sklep {sklep_id}")
    ax.set_xlabel("Tydzień")
    ax.set_ylabel("Cena towaru (PLN)")
    ax.grid(axis="y")

    # Secondary y-axis for rainfall
    ax2 = ax.twinx()
    ax2.plot(tygodnie, wiatr, color="orange", marker="x", label="Prędkość wiatru")
    ax2.set_ylabel("Prędkość wiatru (km/h)")

    # Combine legends from both axes
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(handles1 + handles2, labels1 + labels2, loc="upper right")

# Hide unused subplots
for ax in axes[len(shops) :]:
    ax.set_visible(False)

plt.suptitle("Sprzedaż i prędkość wiatru w poszczególnych sklepach")
plt.tight_layout()
plt.savefig("analyse3_wiatr.png")
plt.show(block=False)

fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), sharey=False)
axes = axes.flatten()

for ax, (sklep_id, values) in zip(axes, shops.items()):
    tygodnie = values["tydzien"]
    cena = values["cena"]
    cisnienie = values["cisnienie_avg"]

    # Bar chart for sales
    ax.bar(tygodnie, cena, color="cornflowerblue", label="Sprzedaż")
    ax.set_title(f"Sklep {sklep_id}")
    ax.set_xlabel("Tydzień")
    ax.set_ylabel("Cena towaru (PLN)")
    ax.grid(axis="y")

    # Secondary y-axis
    ax2 = ax.twinx()
    ax2.plot(tygodnie, cisnienie, color="orange", marker="x", label="Ciśnienie")
    ax2.set_ylabel("Ciśnienie (hPa)")

    # Combine legends from both axes
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(handles1 + handles2, labels1 + labels2, loc="upper right")

# Hide unused subplots
for ax in axes[len(shops) :]:
    ax.set_visible(False)

plt.suptitle("Sprzedaż i ciśnienie w poszczególnych sklepach")
plt.tight_layout()
plt.savefig("analyse3_cisnienie.png")
plt.show(block=False)

fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), sharey=False)
axes = axes.flatten()

for ax, (sklep_id, values) in zip(axes, shops.items()):
    tygodnie = values["tydzien"]
    cena = values["cena"]
    temperatura = values["temperatura_avg"]

    # Bar chart for sales
    ax.bar(tygodnie, cena, color="cornflowerblue", label="Sprzedaż")
    ax.set_title(f"Sklep {sklep_id}")
    ax.set_xlabel("Tydzień")
    ax.set_ylabel("Cena towaru (PLN)")
    ax.grid(axis="y")

    # Secondary y-axis
    ax2 = ax.twinx()
    ax2.plot(tygodnie, temperatura, color="orange", marker="x", label="Temperatura")
    ax2.set_ylabel("Temperatura (°C)")

    # Combine legends from both axes
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(handles1 + handles2, labels1 + labels2, loc="upper right")

# Hide unused subplots
for ax in axes[len(shops) :]:
    ax.set_visible(False)

plt.suptitle("Sprzedaż i temperatura w poszczególnych sklepach")
plt.tight_layout()
plt.savefig("analyse3_temperatura.png")
plt.show(block=False)

fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), sharey=False)
axes = axes.flatten()

for ax, (sklep_id, values) in zip(axes, shops.items()):
    tygodnie = values["tydzien"]
    cena = values["cena"]
    wilgotnosc = values["wilgotnosc_avg"]

    # Bar chart for sales
    ax.bar(tygodnie, cena, color="cornflowerblue", label="Sprzedaż")
    ax.set_title(f"Sklep {sklep_id}")
    ax.set_xlabel("Tydzień")
    ax.set_ylabel("Cena towaru (PLN)")
    ax.grid(axis="y")

    # Secondary y-axis
    ax2 = ax.twinx()
    ax2.plot(tygodnie, wilgotnosc, color="orange", marker="x", label="Wilgotność")
    ax2.set_ylabel("Wilgotność (%)")

    # Combine legends from both axes
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(handles1 + handles2, labels1 + labels2, loc="upper right")


# Hide unused subplots
for ax in axes[len(shops) :]:
    ax.set_visible(False)

plt.suptitle("Sprzedaż i wilgotność w poszczególnych sklepach")
plt.tight_layout()
plt.savefig("analyse3_wilgotnosc.png")
plt.show()

warehouse_conn.close()
