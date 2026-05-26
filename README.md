# Проект Online_store_django

## Описание:

Проект Online_store_django - это приложение проект интернет-магазина, созданный на основе фреймворк Django.

## Установка:

1. Выгрузите репозиторий по HTTPS по URL адресу из PyCharm:
```
https://github.com/KlimanovGrigoriy888/Online_store_django.git
```
2. Создаете виртуальное окружение:
```
python -m venv venv
```
3. Активируйте виртуальное окружение:
```
venv\Scripts\activate
```
4. Для установки окружения необходимого для проекта выполните команду:
```
pip install -r requirements.txt
```
5. Отдельная команда для установки пакета например Django:
```
pip install django
```
6. Для сохранения списка установленных дополнительных пакетов необходимо выполнить команду: 
```
pip freeze > requirements .txt
```
7. Для проверки списка установленных пакетов выполните команду: 
```
pip list
```
8. Для запуска сервера используйте команду:
```
python manage.py runserver
```
9. Для работы с миграцией базы данных с помощью ORM необходимо настроить базу данных PostgresSQL. Необходимо 
выгрузить и установить PostgreSQL c [сайта](https://www.postgresql.org/download/windows/) c помощью PGAdmin и создать базу данных.
Для создания базы данных можете использовать следующие команды с вашими данными:
```
create database <<здесь название вашей бызы данных>>;
create user <<здесь название вашего пользователя>> with password <<'здесь название вашего пароля'>>;
alter database <<здесь название вашей базы данных>> owner to <<store_user>>;
```
Далее ваши данные для настройки подключения к базе данных: DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST=localhost, DATABASE_PORT=5432 
необходимо внести в файл .env.sample и переименовать файл в .env

## Использование:

1. Скопируйте код в PyCharm смотрите раздел установка пункт 1.
2. Проект представляет собой сервер работы интернет магазина, который имеет web страницы домашняя - home.html и контакты - contacts.html в директории 'catalog/'
3. В модуле catalog/views.py созданы: контроллер GET запроса и рендеринга страницы home.html и контроллер POST запроса получения обратной связи со страницы и рендеринга страницы contact.html. 
В контроллер отображения главной страницы добавлен код, выводящий в консоль выборку последних 5 созданных продуктов, при вызове контроллера.
 и контроллер GET запроса и рендеринга страницы contact.html если не POST запрос.
4. В модуле catalog/urls.py cоздана маршрутизация пути html страниц и контроллеров обработчиков POST и GET запросов из html страниц с созданным пространством имен с названием "catalog/"
3. В модуле config/settings.py заполнены необходимые части кода для работы созданного приложения catalog, включены пути для доступа к статическим файлам "static/" 
4. В модуле config/settings.py заполнены необходимые данные для подключения с базой данных PostgreSQL в переменной DATABASES, это: DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT. Эти данные заносятся в код с помощью библиотеки os и python-dotenv и 
хранятся в файле .env.
5. В модуле config/settings.py заполнены необходимые части кода для работы созданного приложения catalog, включены пути для доступа к медиафайлам '/media/',
и config/urls добавлены настройки для сервера и пути медиа файла, что бы мог в режиме разработки обрабатывать и выводить загруженные файлы через URL.
6. В модуле приложения catalog/models.py созданы модели на основе родительских классов моделей django классы Product и  Category.
7. Выполнена миграция для создания базы с помощью команд 
```
python manage.py makemigrations

python manage.py migrate

```
8. В модуле приложения catalog/admin.py созданы настройки для отображения административных окон на странице с URL /admin для объектов классов Product, Category, Contact.
9. Создан файл фикстуры product_fixture.json в корне проекта из уже созданной базы данных для объектов класса catalog.Product и catalog.Category.
Для создания файла фикстуры с базой данных использована команда для создания фикстуры. Пример команды: 
```
python -Xutf8 manage.py dumpdata catalog.Product catalog.Category --output products_fixture.json --indent 4
```
Возможно произвести обратное действие создание объектов класса catalog.Product и catalog.Category из файла фикстуры. Пример команды:
```
python manage.py loaddata products_fixture.json --format json
```
10. В пакетах management/commands создал модули add_product и load_fixture. 
* add_product это python модуль, который создает кастомную команду, в нем написан код заполняющий базу данных новыми объектами класса Product и Category.
* load_fixture это python модуль, который создает кастомную команду, в нем написан код заполняющий базу данных из файла фикстуры products_fixture.json новыми объектами класса Product и Category с помощью метода 'call_command'.
Вызов обоих методов происходит с помощью следующих команд:
```
python manage.py add_product

python manage.py load_fixture
```

## Тестирование:
1. На данной стадии проекта тесты не реализованы 

Команда для получения данных в консоль о покрытии тестами кода. 
```
poetry run pytest --cov

```
5. Для формирования отчета в HTML формате и создания файла htmlcov, необходимо написать команду в терминале:
```
pytest --cov=src --cov-report=html

```

## Документация:

Для получения дополнительной информации обратитесь к [заданию](https://my.sky.pro/student-cabinet/stream-lesson/199148/homework-requirements).

## Лицензия:

Этот проект не лицензирован.