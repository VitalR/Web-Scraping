import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
driver = webdriver.Chrome(executable_path="/Users/vrodikov/workspace/drivers/chromedriver", options=chrome_options)
driver.get('https://sinoptik.ua/')

city = input('Enter city name to check the weather: ')

driver.find_element_by_id('search_city').send_keys(city)
driver.find_element_by_class_name('search_city-submit').click()
url = driver.current_url
# print(url)

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
week = soup.find(id='blockDays')
# print(week)

items = week.find_all(class_='main')

dates = [item.find(class_='date').get_text() for item in items]
months = [item.find(class_='month').get_text() for item in items]
temperatures = [item.find(class_='temperature').get_text() for item in items]
descriptions = [item.find(class_='weatherIco').attrs['title'] for item in items]


weather_stuff = pd.DataFrame(
    {
        'Day': dates,
        'Month': months,
        'Temperature': temperatures,
        'Description': descriptions
    }
)

print("     ")
print("The weather in the city: " + city)
print(weather_stuff)

weather_stuff.to_csv('sinoptik_weather.csv')
weather_stuff.to_html('sinoptik_weather.html')


driver.close()