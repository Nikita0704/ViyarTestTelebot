import requests
from datetime import datetime
import telebot
from telebot import types
from auth_data import token
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import psycopg2
from psycopg2 import Error
import csv
import time

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Сроки производства')
        item2 = types.KeyboardButton('Статус Вияр Базара')
        item3 = types.KeyboardButton('Скорость загрузки страниц')
        item4 = types.KeyboardButton('Проверка авторизации')
        item5 = types.KeyboardButton('Список неотправленных смс')
        item6 = types.KeyboardButton('Статистика заказов')

        markup.add(item1, item2, item3, item4, item5, item6)

        bot.send_message(message.chat.id, 'Привет, {0.first_name}'.format(message.from_user), reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def send_text(message):
        if message.chat.type == 'private':
            if message.text == 'Сроки производства':
                try:
                    Fasady = {
                        0: {'Name': 'Шпонированный',
                            'Days': requests.get(
                                'https://viyarbazar.com/api/get_terms_date.php?id_terms_fasade=28014/').json()},
                        1: {'Name': 'HPL',
                            'Days': requests.get(
                                'https://viyarbazar.com/api/get_terms_date.php?id_terms_fasade=28015/').json()},
                        2: {'Name': 'Крашенный МДФ',
                            'Days': requests.get(
                                'https://viyarbazar.com/api/get_terms_date.php?id_terms_fasade=28008/').json()},
                        3: {'Name': 'Пленочный МДФ',
                            'Days': requests.get(
                                'https://viyarbazar.com/api/get_terms_date.php?id_terms_fasade=28009/').json()},
                        4: {'Name': 'Рамочный ДСП',
                            'Days': requests.get(
                                'https://viyarbazar.com/api/get_terms_date.php?id_terms_fasade=28011/').json()},
                        5: {'Name': 'Акриловый',
                            'Days': requests.get(
                                'https://viyarbazar.com/api/get_terms_date.php?id_terms_fasade=28013/').json()},
                        6: {'Name': 'Рамочный Алюминиевый',
                            'Days': requests.get(
                                'https://viyarbazar.com/api/get_terms_date.php?id_terms_fasade=28012/').json()},
                        7: {'Name': 'Порезка и ДСП',
                            'Days': requests.get(
                                'https://viyarbazar.com/api/get_terms_date.php?id_terms_fasade=63662/').json()},
                    }

                    for k, v in Fasady.items():
                        fasad_name = Fasady[k]['Days']
                        if fasad_name > 1:
                            bot.send_message\
                                (message.chat.id,
                                 f'{Fasady[k]["Name"]} фасад производиться {Fasady[k]["Days"]} дней')
                except Exception as ex:
                    print(ex)
                    bot.send_message(
                        message.chat.id,
                        'Что-то пошло не так'
                    )
            elif message.text == 'Скорость загрузки страниц':
                try:
                    Pages = {
                        0: {'Name': 'Главная страница',
                            'Url': requests.get('https://viyarbazar.com/').elapsed.total_seconds()},
                        1: {'Name': 'Галерея',
                            'Url': requests.get('https://viyarbazar.com/gallery/').elapsed.total_seconds()},
                        2: {'Name': 'Журнал',
                            'Url': requests.get('https://viyarbazar.com/blog/').elapsed.total_seconds()},
                        3: {'Name': 'Видео',
                            'Url': requests.get('https://viyarbazar.com/video/').elapsed.total_seconds()},
                        4: {'Name': 'Специалисты',
                            'Url': requests.get('https://viyarbazar.com/makers/').elapsed.total_seconds()},
                        5: {'Name': 'Личный кабинет мебельщика',
                            'Url': requests.get(
                                'https://viyarbazar.com/personal/maker/profile/?mid=19392').elapsed.total_seconds()},
                        6: {'Name': 'Про нас',
                            'Url': requests.get('https://viyarbazar.com/about/').elapsed.total_seconds()},
                        7: {'Name': 'Правовая информация',
                            'Url': requests.get('https://viyarbazar.com/policy/').elapsed.total_seconds()},
                        8: {'Name': 'Вопросы и ответы',
                            'Url': requests.get('https://viyarbazar.com/faq/').elapsed.total_seconds()},
                    }

                    new_res = ''
                    for k, v in Pages.items():
                        new_res += f'\n{Pages[k]["Name"]} - скорость ответа {Pages[k]["Url"]} секунд'

                    bot.send_message(message.chat.id, new_res)

                except Exception as ex:
                    print(ex)
                    bot.send_message(
                        message.chat.id,
                        'Что-то пошло не так'
                    )

            elif message.text == 'Статус Вияр Базара':
                try:
                    r = requests.get('https://viyarbazar.com/', verify=False)
                    if r.status_code == 200:
                        bot.send_message(message.chat.id, 'Сайт работает нормально')
                except Exception as ex:
                    print(ex)
                    bot.send_message(
                        message.chat.id,
                        'Что-то пошло не так'
                    )

            elif message.text == 'Проверка авторизации':
                try:
                    driver = webdriver.Chrome(ChromeDriverManager().install())
                    driver.maximize_window()
                    driver.implicitly_wait(10)

                    driver.get("https://viyarbazar.com/auth_check/")
                    login_field = driver.find_element_by_id("username")
                    login_field.send_keys("n.alexeyevich7@gmail.com")
                    password_field = driver.find_element_by_id("password")
                    password_field.send_keys("Sufonees54")
                    button_login = driver.find_element_by_xpath(
                        "/html/body/div[2]/div[2]/div/div/div[2]/div/form/div[4]/button")
                    button_login.click()
                    user_mail = driver.find_element_by_class_name('userLogin')
                    assert user_mail.text == 'n.alexeyevich7@gmail.com'
                    if user_mail.text == 'n.alexeyevich7@gmail.com':
                        bot.send_message(message.chat.id, 'Авторизация успешна')
                    else:
                        bot.send_message(message.chat.id, 'Авторизация не прошла')
                except Exception as ex:
                    print(ex)
                    bot.send_message(
                        message.chat.id,
                        'Что-то пошло не так'
                    )

            elif message.text == 'Список неотправленных смс':
                try:
                    # Подключение к существующей базе данных
                    connection = psycopg2.connect(user="postgres",
                                                  # пароль, который указали при установке PostgreSQL
                                                  password="Rf4p7UH4m5",
                                                  host="notify-corezoid-pg.cpax6ewejpz1.eu-central-1.rds.amazonaws.com",
                                                  port="5432",
                                                  database="postgres"
                                                  )

                    cursor = connection.cursor()
                    postgreSQL_select_Query = 'SELECT * FROM "Viyar_Notify".messages WHERE time_stamp >=' + str(
                        current_date) + ' ORDER BY "time_stamp" desc LIMIT 2000'

                    cursor.execute(postgreSQL_select_Query)
                    sms = cursor.fetchall

                    SMS_IN_QUEUE = []
                    SMS_ERROR = []
                    SMS_NULL = []
                    SMS_UNDELIVERED_STATE = []

                    for row in cursor:
                        if 'DELIVERED' and 'BLACKLISTED' and 'BLACKLISTED' in row:
                            pass
                        if 'IN_QUEUE' in row:
                            SMS_IN_QUEUE.append(row)
                        if 'SMS_UNDELIVERED_STATE' in row:
                            SMS_UNDELIVERED_STATE.append(row)
                        if 'error' in row:
                            SMS_ERROR.append(row)

                    for sms in SMS_UNDELIVERED_STATE:
                        with open('SMS_UNDELIVERED_STATE.csv', 'a', encoding='utf-8') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow(sms)

                    for sms in SMS_ERROR:
                        with open('SMS_ERROR.csv', 'a', encoding='utf-8') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow(sms)
                except (Exception, Error) as error:
                    print("Ошибка при работе с PostgreSQL", error)
                finally:
                    if connection:
                        cursor.close()
                        connection.close()
                        print("Соединение с PostgreSQL закрыто")

                document = open('SMS_UNDELIVERED_STATE.csv')
                bot.send_document(message.chat.id, document)

            elif message.text == 'Статистика заказов':
                try:
                    info = requests.get('https://viyarbazar.com/for_developers/chigrin/get_all_orders_api.php').json()

                    OFFERS_WITH_STATUS_0 = []
                    OFFERS_WITH_STATUS_1 = []
                    OFFERS_WITH_STATUS_2 = []

                    for i in info:
                        if '0' in i['STATUS']:
                            OFFERS_WITH_STATUS_0.append(i['ID'])

                    for i in info:
                        if '1' in i['STATUS']:
                            OFFERS_WITH_STATUS_1.append(i['ID'])

                    for i in info:
                        if '2' in i['STATUS']:
                            OFFERS_WITH_STATUS_2.append(i['ID'])

                    bot.send_message(message.chat.id, f'Заказов в ожидании: {len(OFFERS_WITH_STATUS_0)}\n' +
                                     f'Заказов в работе: {len(OFFERS_WITH_STATUS_1)}\n' +
                                     f'Завершенных заказов: {len(OFFERS_WITH_STATUS_2)}')
                except Exception as ex:
                    print(ex)
                    bot.send_message(
                        message.chat.id,
                        'Что-то пошло не так'
                    )

    # bot.polling()


if __name__ == '__main__':
    telegram_bot(token)
