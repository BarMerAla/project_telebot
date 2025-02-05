import telebot
from telebot import types
import wikipediaapi
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

token = "6047511985:AAE6TyFV9eQNKk7ZeYed8_9UQntVSpMuaCI"
bot = telebot.TeleBot(token)

options = webdriver.ChromeOptions()
options.add_argument("--headless")   # Запуск без открытия окна браузера (опционально)
driver = webdriver.Chrome(options=options)

wiki = wikipediaapi.Wikipedia("Mereke", "ru")


@bot.message_handler(commands=["start"])
def start_command(message):
    keyboard = types.ReplyKeyboardMarkup()
    button_start = types.KeyboardButton("START")
    keyboard.add(button_start)
    bot.send_message(message.chat.id,"Привет! Нажми на кнопку START", reply_markup=keyboard)
    
@bot.message_handler(func=lambda message:message.text == "START")    
def handle_start_button(message):
    keyboard = types.InlineKeyboardMarkup()
    button_info = types.InlineKeyboardButton(text="Информация о боте", callback_data="but_info")
    keyboard.add(button_info)
    bot.send_message(message.chat.id,"Я новый телеграм бот!", reply_markup=keyboard)    
   
@bot.callback_query_handler(func=lambda call:True)    # здесь ответ на нажатие кнопки "Информация о боте"
def callback_query(call):
    if call.data == "but_info":
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        bot.send_message(call.message.chat.id, "Этот бот подберет вам фильм на вечер, какой вы хотите, нужно только выбрать!")  
        button_boev = types.InlineKeyboardButton(text= "Боевик", callback_data="but_boevik")
        button_com = types.InlineKeyboardButton(text= "Комедия", callback_data="but_comedy")
        button_fan = types.InlineKeyboardButton(text= "Фантастика", callback_data="but_fant")
        button_ujs = types.InlineKeyboardButton(text= "Ужасы", callback_data="but_horror")
        button_cinemas = types.InlineKeyboardButton(text = "Фильмы в кинотеатрах", callback_data="cinemas_now")
        keyboard.add(button_boev, button_com, button_fan, button_ujs, button_cinemas)
        bot.send_message(call.message.chat.id, "Выберите жанр фильма", reply_markup=keyboard)
        
    elif call.data == "but_boevik":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button_1 = types.InlineKeyboardButton(text="Джон Уик 4", callback_data="but_1")
        button_2 = types.InlineKeyboardButton(text="Законопослушный гражданин", callback_data="but_2")
        button_3 = types.InlineKeyboardButton(text="Форсаж 10", callback_data="but_3")
        button_4 = types.InlineKeyboardButton(text="Гипнотик", callback_data="but_4")
        button_back = types.InlineKeyboardButton(text="Назад к жанрам", callback_data="but_info")
        keyboard.add(button_1, button_2, button_3, button_4, button_back)
        bot.send_message(call.message.chat.id, "Какой из этих фильмов вы хотите посмотреть?", reply_markup=keyboard)
       
    elif call.data in ["but_1", "but_2", "but_3", "but_4"]:
        film_links = {
            "but_1":("Джон Уик 4", "https://hdrezka.live/4587-dzhon-uik-4.html"),
            "but_2":("Законопослушный гражданин", "https://vu.baksino.website/dramy/244-zakonoposlushnij-grazhdanin.html"),
            "but_3":("Форсаж 10", "https://kinobar.vip/29353-forsazh-10-2023.html"),
            "but_4":("Гипнотик", "https://kinobar.vip/29900-gipnotik-2023.html"),
            }
        film_name, film_url = film_links[call.data]
        page = wiki.page(film_name)
        keyboard = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton(text="Назад к фильмам", callback_data="but_boevik")
        keyboard.add(button_back)
        bot.send_message(call.message.chat.id, page.summary[0:500] + "\nСсылка на полное описание фильма" + page.fullurl)
        bot.send_message(call.message.chat.id, f"Cсылка на фильм: {film_url}", reply_markup=keyboard)
                    
    elif call.data == "but_comedy":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button_5 = types.InlineKeyboardButton(text="Маска", callback_data="but_5")
        button_6 = types.InlineKeyboardButton(text="Убойные каникулы", callback_data="but_6")
        button_7 = types.InlineKeyboardButton(text="Евротур", callback_data="but_7")
        button_8 = types.InlineKeyboardButton(text="Голый пистолет", callback_data="but_8")
        button_back = types.InlineKeyboardButton(text="Назад к жанрам", callback_data="but_info")
        keyboard.add(button_5, button_6, button_7, button_8, button_back)
        bot.send_message(call.message.chat.id, "Какой из этих фильмов вы хотите посмотреть?", reply_markup=keyboard)   
        
    elif call.data in ["but_5", "but_6", "but_7", "but_8"]:
        film_links = {
            "but_5":("Маска (фильм, 1994)", "https://hdrezka.ag/films/fantasy/3674-maska-1994.html"),
            "but_6":("Убойные каникулы", "https://kinobar.ai/355-uboynye-kanikuly-v2.html"),
            "but_7":("Евротур (фильм)", "https://kinobar.ai/969-evrotur-v1.html"),
            "but_8":("Голый пистолет", "https://rutube.ru/video/da792747f5e2bdbff2d40c7c857ca9e0/"),
            }
        film_name, film_url = film_links[call.data]
        page = wiki.page(film_name)
        keyboard = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton(text="Назад к фильмам", callback_data="but_comedy")
        keyboard.add(button_back)
        bot.send_message(call.message.chat.id, page.summary[0:500] + "\nСсылка на полное описание фильма" + page.fullurl)
        bot.send_message(call.message.chat.id, f"Cсылка на фильм: {film_url}", reply_markup=keyboard)
        
    elif call.data == "but_fant":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button_9 = types.InlineKeyboardButton(text="Начало (фильм, 2010)", callback_data="but_9")
        button_10 = types.InlineKeyboardButton(text="Интерстеллар", callback_data="but_10")
        button_11 = types.InlineKeyboardButton(text="Мстители: Война бесконечности", callback_data="but_11")
        button_12 = types.InlineKeyboardButton(text="Темный рыцарь", callback_data="but_12")
        button_back = types.InlineKeyboardButton(text="Назад к жанрам", callback_data="but_info")
        keyboard.add(button_9, button_10, button_11, button_12, button_back)
        bot.send_message(call.message.chat.id, "Какой из этих фильмов вы хотите посмотреть?", reply_markup=keyboard)   
        
    elif call.data in ["but_9", "but_10", "but_11", "but_12"]:
        film_links = {
            "but_9":("Начало (фильм, 2010)", "https://kinobar.vip/185-nachalo-v4.html"),
            "but_10":("Интерстеллар", "https://kinobar.vip/2400-interstellar-1-v4.html"),
            "but_11":("Мстители: Война бесконечности", "https://kinobar.vip/6626-mstiteli-voyna-beskonechnoosti-chast1-3-v6.html"),
            "but_12":("Темный рыцарь", "https://kinobar.vip/263-temnyy-rycar-v2.html"),
            }
        
        film_name, film_url = film_links[call.data]
        page = wiki.page(film_name)
        keyboard = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton(text="Назад к фильмам", callback_data="but_fant")
        keyboard.add(button_back)
        bot.send_message(call.message.chat.id, page.summary[0:500] + "\nСсылка на полное описание фильма" + page.fullurl)
        bot.send_message(call.message.chat.id, f"Cсылка на фильм: {film_url}", reply_markup=keyboard)
        
    elif call.data == "but_horror":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button_13 = types.InlineKeyboardButton(text="Восстание зловещих мертвецов", callback_data="but_13")
        button_14 = types.InlineKeyboardButton(text="Экзорцист Ватикана", callback_data="but_14")
        button_15 = types.InlineKeyboardButton(text="Тихое место", callback_data="but_15")
        button_16 = types.InlineKeyboardButton(text="Последнее путешествие «Деметра»", callback_data="but_16")
        button_back = types.InlineKeyboardButton(text="Назад к жанрам", callback_data="but_info")
        keyboard.add(button_13, button_14, button_15, button_16, button_back)
        bot.send_message(call.message.chat.id, "Какой из этих фильмов вы хотите посмотреть?", reply_markup=keyboard)
        
    elif call.data in ["but_13", "but_14", "but_15", "but_16"]:
        film_links = {
            "but_13":("Восстание зловещих мертвецов", "https://kinobar.vip/27687-vosstanie-zloveschih-mertvecov-2023.html"),
            "but_14":("Экзорцист Ватикана", "https://kinobar.vip/29483-ekzorcist-papy-2023.html"),
            "but_15":("Тихое место", "https://kinobar.ai/14128-tihoe-mesto-hd-v1.html"),
            "but_16":("Последнее путешествие «Деметра»", "https://kinobar.vip/30018-poslednee-puteshestvie-demetra-2023.html"),
            }
        film_name, film_url = film_links[call.data]
        page = wiki.page(film_name)
        keyboard = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton(text="Назад к фильмам", callback_data="but_horror")
        keyboard.add(button_back)
        bot.send_message(call.message.chat.id, page.summary[0:500] + "\nСсылка на полное описание фильма" + page.fullurl)
        bot.send_message(call.message.chat.id, f"Cсылка на фильм: {film_url}", reply_markup=keyboard)
        
    elif call.data == "cinemas_now":
        keyboard = types.InlineKeyboardMarkup()
        button_back = types.InlineKeyboardButton(text="Назад к жанрам", callback_data="but_info")
        keyboard.add(button_back)
        bot.send_message(call.message.chat.id, "Ближайшие сеансы ↓")
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
            driver.get(new_url)

            r = requests.get(new_url, headers=headers)
            if r.status_code != 200:
                bot.send_message(call.message.chat.id, f"Ошибка загрузки страницы: {r.status_code}")
                continue
            
            soup2 = BeautifulSoup(r.text, "lxml")
            name_movie = soup2.find("h1")   
            bot.send_message(call.message.chat.id, f"Фильм: {name_movie.text.strip()}")
            
            try:
                cinema_element = WebDriverWait(driver, 6).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "nn6vvhb"))
                )
                times = driver.find_elements(By.CLASS_NAME, "nn6vvh6")[:1]
                for time in times:
                    bot.send_message(call.message.chat.id, f"Кинотеатр: {cinema_element.text.strip()} - Время сеанса: {time.text.strip()}")
            except Exception as e:
                bot.send_message(call.message.chat.id, "Ошибка при выводе данных(")
        bot.send_message(call.message.chat.id, "Вернуться назад?", reply_markup=keyboard)
        
driver.quit()
                    
if __name__ == "__main__":
    bot.infinity_polling()    