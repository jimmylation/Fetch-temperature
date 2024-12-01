import requests
from bs4 import BeautifulSoup

url = "https://www.piteenergi.se/snotemperatur/"

response = requests.get(url)

# Kontrollera om förfrågan lyckades
if response.status_code == 200:
    print("Hämtade data från sidan.")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Skriv ut första 5000 tecken av HTML-sidan för felsökning
    print(soup.prettify()[:5000])

else:
    print(f"Kunde inte hämta data från sidan. Statuskod: {response.status_code}")
