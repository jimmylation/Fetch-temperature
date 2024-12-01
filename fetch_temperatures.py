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
    
    sections = soup.find_all('div', class_='snotemp-container')

    # Kontrollera om vi hittar data för Lindbäcksstadion
    found = False

    for section in sections:
        heading = section.find_previous(['h3', 'h2'])
        if heading and 'Lindbäcksstadion' in heading.text:
            found = True
            snow_temp = section.find('li', class_='snotemp').text.strip()
            air_temp = section.find('li', class_='lufttemp').text.strip()

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
    
    if not found:
        print("Hittade inte data för Lindbäcksstadion.")
else:
    print(f"Kunde inte hämta data från sidan. Statuskod: {response.status_code}")
