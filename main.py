import csv

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
# options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome()


ga_url = "https://goldapple.ru/parfjumerija?p=1"


class GoldenAppleParser:

    def __init__(self, url: str, count: int):
        self.url = url  # Адресс страницы для парсинга
        self.count = count  # Cчетчик количества страниц для парсинга

    def __set_up(self):
        self.driver = webdriver.Chrome()  # Инициализируем веб-драйвер
        self.driver.get(self.url)  # Запрос на страницу для парсинга

    def __create_urls(self):
        with open('urls.csv', 'w', encoding='utf-8') as file:   # Открываем файл на запись
            writer = csv.writer(file)   # Создаем файл urls.csv для хранения ссылок на товары
            writer.writerow(
                ['urls']  # Записываем заголовок колонки
            )

    def __save_urls(self, data: str):
        with open('urls.csv', 'a', encoding='utf-8') as file:    # Открываем файл на добавления
            writer = csv.writer(file)
            writer.writerow(data.split(' '))   # Записываем ссылку на товар в файл urls.csv

    def __read_urls(self):
        with open('urls.csv', 'r', encoding='utf-8') as file:   # Открываем файл на чтение
            reader = csv.DictReader(file)
            for row in reader:
                yield row['urls']   # В цикле считываем и возращаем по одной ссылке из файла

    def __data_to_csv(self, data):
        with open('data.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            for row in data:
                writer.writerow(row)

    def __paginator(self):
        """
            Выполняем пагинацию по динамически догружаемой странице,
            путем её пролистывания к элементу JS для подгрузки новых товаров и уменьшая счетчик страниц.
        """
        self.__set_up()  # Вызываем метод загрузки веб-драйвера
        self.__create_urls()    # Вызываем метод создания файла urls.csv
        while self.driver.find_elements(By.CSS_SELECTOR, "[class='RHHB8']") and self.count > 0:
            element = self.driver.find_element(By.CSS_SELECTOR,
                                               "[class='RHHB8']")  # Инициализируем элемента который отвечает за пагинацию
            action = ActionChains(self.driver)  # Инициализируем действие
            action.move_to_element(element).perform()  # Перемещаемся к элемент, подгружая новые товары
            sleep(2)  # Пауза, для подгрузки данных
            self.count -= 1  # Уменьшаем счетчик

    def get_urls(self):
        """
            Cохраням ссылки на товары в переменну page_data и в цикле записываем их в urls.csv
        """
        self.__paginator()   # Вызываем метод пагинации по странице
        page_data = self.driver.find_elements(By.CSS_SELECTOR,
                                              "[itemprop='url']")  # Получаем эелементы с ссылками на товар
        for data in page_data:
            card_url = data.get_attribute("href")  # Извлекаем ссылку из элементов
            if card_url == 'https://goldapple.ru/':     # Обрабатываем исключение
                continue
            else:
                self.__save_urls(card_url)  # Добавляем ссылку в список

    def parse_page(self):
        """
            Итерируемся по ссылкам на товар и парсим с каждой ссылки необходимые данные в шаблон,
            после заполнения шаблона передаем его на запись в виде csv файла
        """
        csv_form = [['url', 'name', 'price', 'desc', 'usage', 'rating', 'country']]     # Создаем заголовки для файла data.csv
        for card_url in self.__read_urls():  # Получаем ссылку на товар
            driver.get(card_url)   # Переходим на страницу товара
            sleep(4)    # Пауза для загрузки карточки товара
            card_data = driver.find_elements(By.CSS_SELECTOR, "[class='xvuYB']")    # Загружаем карточку товара в переменную

            for data in card_data:
                name = data.find_element(By.CSS_SELECTOR, "[class='fLd0k']").text    # Получаем имя товара
                price = data.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute('content')    # Получаем цену товара
                desc = data.find_element(By.CSS_SELECTOR, "[itemprop='description']").text    # Получаем описание товара
                csv_data = [card_url, name, price, desc]     # Передаем переменные в список, которы будем записывать в data.csv

                try:  # Проверяем наличие инструкция по применению в караточке товара, через цикл по элементам JS
                    for i in range(1, 6):
                        usage_element = data.find_element(By.XPATH, "//*[@id='__layout']/div/main/article/"
                                                                    "div[4]/div[2]/div[1]/div[1]/div[1]/"
                                                                    f"div/button[{i}]")
                        if usage_element.text != 'ПРИМЕНЕНИЕ':
                            continue
                        else:
                            driver.execute_script("arguments[0].click();", usage_element)
                            usage = data.find_element(By.XPATH,
                                                      "//*[@id='__layout']/div/main/article/div[4]/div[2]/div["
                                                      "1]/div[2]/div/div/div/div/div").text
                            csv_data.append(usage)
                        break
                except NoSuchElementException:  # Обрабатываем ошибку, если элемент отсутствует
                    usage = None
                    csv_data.append(usage)

                try:
                    rating = data.find_element(By.CSS_SELECTOR, "[class='dn1Tv']").text
                    csv_data.append(rating)
                except NoSuchElementException:  # Обрабатываем ошибку, если элемент отсутствует
                    rating = None
                    csv_data.append(rating)

                try:
                    for i in range(1, 6):  # Ищем страну производителя в караточке товара, через цикл по элементам JS
                        country_button = data.find_element(By.XPATH, "//*[@id='__layout']/div/main/article/"
                                                                     "div[4]/div[2]/div[1]/div[1]/div[1]/"
                                                                     f"div/button[{i}]")
                        if country_button.text != "ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ":
                            continue
                        else:
                            driver.execute_script("arguments[0].click();", country_button)
                            country = data.find_element(By.CSS_SELECTOR, "[class='_14lAW']").text
                            csv_data.append(country)
                        break
                except NoSuchElementException:  # Обрабатываем ошибку, если элемент отсутствует
                    country = None
                    csv_data.append(country)
                csv_form.append(csv_data)   # Передаем шаблон товара в форму для записи в csv файл
            self.__data_to_csv(csv_form)    # Записываем заполненый шаблон товара в data.csv

    def parser(self):

        print('Парсинг сайта запущен: \n'
              'Расчетное время работы программы 6 часов')
        print('Не закрывайте окно браузера!')
        print('Получаем ссылки на все товары категории парфюмерия..\n '
              'Расчетное время ожидания: 15 мин.')
        self.get_urls()
        print('Извлекаем и записываем данные с каждой ссылки..\n '
              'Расчетное время ожидания: 5 часов 35 мин.')
        self.parse_page()
        print('Парсинг завершен!')


if __name__ == "__main__":
    GoldenAppleParser(ga_url, 321).parse_page()
