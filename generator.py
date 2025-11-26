import random
from datetime import datetime, timedelta

start_date = datetime(2023, 1, 1)
with open("pomiar_insert.sql", "w") as file:
    for i in range(1, 6):
        for j in range(365):
            current_date = (start_date + timedelta(days=j)).strftime("%Y-%m-%d")
            file.write(
                f"INSERT INTO pomiar (station_id, data_pomiaru, godzina_pomiaru) VALUES ({i}, '{current_date}', 12);\n"
            )

typy_pomiaru = ["opady", "predkosc_wiatru", "cisnienie", "temperatura", "wilgotnosc"]
jednostki = ["mm", "km/h", "hPa", "°C", "%"]


with open("wart_insert.sql", "w") as file:
    for i in range(1, 1826):
        for j in range(5):
            measurement_type = typy_pomiaru[j]

            value = 0
            if measurement_type == "opady":
                if random.random() < 0.7:
                    value = 0.0
                else:
                    value = round(random.uniform(0.1, 25.0), 1)

            elif measurement_type == "predkosc_wiatru":
                value = round(random.uniform(0, 35.0), 1)
                if random.random() < 0.05:
                    value = round(random.uniform(35.0, 80.0), 1)

            elif measurement_type == "cisnienie":
                value = round(random.uniform(980.0, 1040.0), 1)

            elif measurement_type == "temperatura":
                value = round(random.uniform(-15.0, 35.0), 1)

            elif measurement_type == "wilgotnosc":
                value = round(random.uniform(30.0, 95.0), 1)

            file.write(
                f"INSERT INTO wartosci ( pomiar_id, typ_pomiaru, wartosc, jednostka) VALUES ( {i}, '{typy_pomiaru[j]}', {value}, '{jednostki[j]}');\n"
            )
