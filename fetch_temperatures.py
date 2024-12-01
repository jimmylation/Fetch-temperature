import requests
from bs4 import BeautifulSoup
import json

# URL till sidan
url = "https://www.piteenergi.se/snotemperatur/"

# Hämta innehåll från sidan
response = requests.get(url)

# Om förfrågan lyckas, fortsätt bearbeta
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Hitta alla div-taggar som kan innehålla temperaturinformation
    sections = soup.find_all('div', class_='snotemp-container')  # Justera för att passa korrekt element
    
    # Gå igenom alla sektioner och hitta Lindbäcksstadion
    for section in sections:
        heading = section.find_previous(['h3', 'h2'])  # Titta på rubriken före sektionen
        if heading and 'Lindbäcksstadion' in heading.text:
            # Hämta temperaturer
            snow_temp = section.find('li', class_='snotemp').text.strip()
            air_temp = section.find('li', class_='lufttemp').text.strip()

            # Skapa en dictionary för att spara temperaturdata
            temperature_data = {
                'Lindbäcksstadion': {
                    'Snow Temperature': snow_temp,
                    'Air Temperature': air_temp
                }
            }

            # Skriv ut för att säkerställa att vi hittar temperaturerna
            print(f"Snow Temperature: {snow_temp}")
            print(f"Air Temperature: {air_temp}")

            # Skriv ut att vi skriver till filen
            print("Skriver temperaturdata till temperature_data.json")

            # Spara data som JSON-fil
            with open('temperature_data.json', 'w') as json_file:
                json.dump(temperature_data, json_file, indent=4)

            print("Temperaturdata för Lindbäcksstadion sparad.")
            break
else:
    print("Kunde inte hämta data från sidan.")
