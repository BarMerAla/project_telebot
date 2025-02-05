import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--headless")   # Запуск без открытия окна браузера (опционально)
driver = webdriver.Chrome(options=options)


url = "https://kino.kz/ru/movie"
headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

        
responce = requests.get(url, headers=headers)
soup = BeautifulSoup(responce.text, "lxml")

movies = soup.find_all("a", class_ = "rt-Box _1aar5ie0")
 
for movie in movies:
    movie_link = movie.get("href")
    if not movie_link:
        continue   
    
    if movie_link.startswith("http:"):   # Проверяем, начинается ли ссылка с "http" или "/"
        new_url = movie_link
    else:
        new_url = f'https://kino.kz{movie_link}'   # Убираем лишний "/ru/movie"
    # print(f"Парсим: {new_url}")
    driver.get(new_url)

    r = requests.get(new_url, headers=headers)
    if r.status_code != 200:
        print(f"Ошибка загрузки страницы: {r.status_code}")
        continue
    
    soup2 = BeautifulSoup(r.text, "lxml")
    name_movie = soup2.find("h1")   # Без указания класса
    print(f"Название фильма: {name_movie.text.strip()}")
    
    try:
        cinema_element = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nn6vvhb"))
        )
        times = driver.find_elements(By.CLASS_NAME, "nn6vvh6")[:1]
        for time in times:
            print(f"Кинотеатр: {cinema_element.text.strip()} - Время сеанса: {time.text.strip()}")
    except Exception as e:
        print("Ошибка {e}")
    # cinemas = soup2.find("span", class_ = "rt-Text rt-r-size-3 rt-r-weight-bold nn6vvhb")
    # print(name_movie.text.strip())
    # print(cinemas.text.strip())     # таким образом не выводится название кинотеатра, так что пробуем selenium
    # print(soup2.prettify())  # вывод html кода страницы
   
driver.quit()

  