import requests
from bs4 import BeautifulSoup
import json
import os

url = "https://www.piteenergi.se/snotemperatur/"

response = requests.get(url)

# Kontrollera om förfrågan lyckades
if response.status_code == 200:
    print("Hämtade data från sidan.")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Hitta sektionen som innehåller temperaturer för Lindbäcksstadion
    # Jag letar efter den specifika sektionen där temperaturerna är listade (i li-taggar)
    temp_section = soup.find('div', class_='m-snow-card__content')

    if temp_section:
        # Hitta snötemperatur och lufttemperatur
        snow_temp = temp_section.find('li', class_='snotemp').text.strip() if temp_section.find('li', class_='snotemp') else "Ingen snötemp tillgänglig"
        air_temp = temp_section.find('li', class_='lufttemp').text.strip() if temp_section.find('li', class_='lufttemp') else "Ingen lufttemp tillgänglig"

        temperature_data = {
            'Lindbäcksstadion': {
                'Snow Temperature': snow_temp,
                'Air Temperature': air_temp
            }
        }

        print(f"Snow Temperature: {snow_temp}")
        print(f"Air Temperature: {air_temp}")
        print("Skriver temperaturdata till temperature_data.json")

        # Kontrollera om filen redan finns
        print("Kontrollerar om temperature_data.json finns innan skrivning:", os.path.exists('temperature_data.json'))

        try:
            # Skriv till fil
            with open('temperature_data.json', 'w') as json_file:
                json.dump(temperature_data, json_file, indent=4)

            print("temperature_data.json skapad.")
        except Exception as e:
            print(f"Fel vid skrivning till fil: {e}")
    else:
        print("Hittade ingen temperatursektion för Lindbäcksstadion.")
else:
    print(f"Kunde inte hämta data från sidan. Statuskod: {response.status_code}")
