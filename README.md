# The lol Project
## Special for Boklach and THE GREAT MDK 10.1 ![Static Badge](https://img.shields.io/badge/one_%3C3-8A2BE2?style=plastic&logo=linux&label=Linux)

Проект на реактивной тяге и Flask фреймворке, позволяющий просматривать информацию о количестве городов и население десяти самых больших городов в стране.
Сайт работает с использованием реляционной СУБД PostgreSQL. В качестве БД выбран сэмпл с официального сайта используемой СУБД и приложено в корневой папке репозитория.

Для того чтобы развернуть сайт в своем окружении, вам потребуется проследовать инструкции:
1. Убедитесь что у вас установлен python не ниже версии 3.1 и pip.
2. Вам понадобится PostgreSQL. Вы можете поднять ее сами или использовать облачное решение. Не забудьте импортировать схему world.sql
3. Скачайте репозиторий и войдите в него при помощи терминала.
4. Создайте виртуальное окружение и войдите в него при помощи команды: `python3 -m venv . & source bin/activate`
5. Скачайте зависимости: `pip install -r requirements.txt`.
6. Измените данные для подключения к БД на собственные в файле main.py.
7. Запустите проект командой: `python3 main.py`
8. У вас запущен мой проект :)

## Интерфейс
Сайт представляет собой простейшее веб-приложение из трех страниц:
  - главная (index.html)
  - страница с данными (country_info.html)
  - страница с сообщением об ошибке (country_not_fount.html)

Каждая страница включает в себя базовый шаблон `base.html`, который позволяет не повторяться в фундаментальной структуре сайта и упрощает разработку.

## Код
Файл имеет две функции.
Одна из них `index()`, которая позволяет принимать запросы, где в качестве аргумента приходит трехзначный код страны методом POST. 
Эта функция, получив запрос методом POST, она сразу вызывает функцию методом GET `get_country_info(country_code)`, что в свою очередь получает данные из БД и генерирует уже страницы по запросу.
`get_country_info(country_code)` преобразует к правильному виду полученный код и делает запрос в БД. Получив ответ, генерируется страница по шаблону `country_info.html`. Иначе генерируется по шаблону `country_not_found.html`.
Также реализован прикол, который незадокументирован)

## Скриншоты
<img width="1322" alt="image" src="https://github.com/Daxik2x/lol/assets/63903274/f66c287e-37a2-4c7a-9bb6-23617af8ae2d">
<img width="1320" alt="image" src="https://github.com/Daxik2x/lol/assets/63903274/72ace627-20d1-42e1-aa31-5d7067bae964">
<img width="1320" alt="image" src="https://github.com/Daxik2x/lol/assets/63903274/2edf07b2-1f1c-48ee-80dd-91a4f5e52458">

