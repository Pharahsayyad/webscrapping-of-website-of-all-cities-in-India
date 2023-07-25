import requests
from bs4 import BeautifulSoup
import csv

def scrape_weather_data():
    url = 'https://www.weather-forecast.com/countries/India-1' # Replace this with the actual weather website URL
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    # Send an HTTP GET request to the website
    response = requests.get(url,headers=HEADERS)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the elements containing the weather data (modify according to the website's HTML structure)
        city_elements = soup.find_all('span', class_='b-list-table__item-name')
        temperature_elements = soup.find_all('div', class_='tempcell')
        humidity_elements = soup.find_all('span', class_='humidity')

        #print(city_elements)
        city_list = []
        temperature_list=[]
        for city_element in city_elements:
            b_tag = city_element.find('b')
            if b_tag:
                city_list.append(b_tag.text)
        #print(city_list)
        for temperature_element in temperature_elements:
            span_element=temperature_element.find('span')
            if span_element:
                temperature_list.append(span_element.text)
        #print(temperature_list)

        
        #Write the data to a CSV file
        with open('weather_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['City', 'Temperature (°C)'])
            for city, temp in zip(city_list, temperature_list):
                writer.writerow([city, temp])

            print("Weather data scraped and saved to 'weather_data.csv'")
    else:
         print("Failed to retrieve weather data. Status code:", response.status_code)

if __name__ == "__main__":
    scrape_weather_data()
