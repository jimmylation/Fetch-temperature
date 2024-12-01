import requests
from bs4 import BeautifulSoup
import json

# URL till PiteEnergis temperaturdata
url = "https://www.piteenergi.se/snotemperatur/"
output_file = "temperature_data.json"  # Fil där datan sparas

try:
    response = requests.get(url)
    response.raise_for_status()  # Kontrollera att förfrågan lyckades

    soup = BeautifulSoup(response.text, 'html.parser')

    # Leta upp sektionen för Lindbäcksstadion
    lindbacks_section = soup.find('div', class_='stadion-container')  # Justera om nödvändigt
    if lindbacks_section:
        snow_temp = lindbacks_section.find('span', class_='snow-temp').text.strip()
        air_temp = lindbacks_section.find('span', class_='air-temp').text.strip()

        # Spara data i JSON-format
        data = {
            "location": "Lindbäcksstadion",
            "snow_temperature": snow_temp,
            "air_temperature": air_temp
        }
        with open(output_file, 'w') as file:
            json.dump(data, file)

        # Logga resultatet
        print("Temperaturer hämtade:")
        print(f"Snö: {snow_temp}, Luft: {air_temp}")
    else:
        print("Kunde inte hitta temperaturdata för Lindbäcksstadion.")
except Exception as e:
    print(f"Ett fel inträffade: {e}")
