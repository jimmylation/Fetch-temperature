import requests
from bs4 import BeautifulSoup
import json
import os

url = "https://www.piteenergi.se/snotemperatur/"

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    sections = soup.find_all('div', class_='snotemp-container')

    for section in sections:
        heading = section.find_previous(['h3', 'h2'])
        if heading and 'Lindbäcksstadion' in heading.text:
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
else:
    print("Kunde inte hämta data från sidan.")
