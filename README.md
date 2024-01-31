# GoldenAppleParser

👾 Задача: создать CSV файл со всеми товарами магазина: https://goldapple.ru/parfjumerija

В этом файле должна быть следующая информация в текстовом формате:

1. ссылка на продукт
2. наименование
3. цена
4. рейтинг пользователей
5. описание продукта
6. инструкция по применению
7. страна-производитель


## Содержание
- [Библиотеки](#Библитеки)
- [Установка зависимостей](#установка зависимостей)
- [Использование](#использование)
- [To do](#to-do)

## Библиотеки
- selenium
- python 3.11
  
## Установка зависимостей

1. Клонировать репозиторий:
   
```
git clone https://github.com/K-chuklin/GoldenAppleParser.git
```
2. Создать и активировать виртуальное окружение:
   
```
python -m venv venv
(linux) source bin/activate
```
3. Установить зависимости из requirements.txt:
   
```
pip install -r requirements.txt
```

## Использование
Для запуска проекта необходимо:

1. Cкачать по ссылке в корень проекта веб-драйвер Сhrome для работы библиотеки selenium.
   Версия драйвера должна соответствовать, версии Chrom'a на вашем устройстве.
```
https://chromedriver.chromium.org/downloads
```

2. Запустить файл main.py
```
python3 main.py
```

3. Результат работы будет сформирован в файле data.csv


### Зачем вы разработали этот проект?
Было интересно поработать с selenium.

## To do
- [x] Добавить крутое README
- [ ] Реализовать парсинг в несколько вкладок
- [ ] Реализовать паралельное заполнение url и их парсинг