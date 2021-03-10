# Yatube

Социальная сеть для блогеров. Пользователи могут выкладывать посты с картинками,
редактировать и удалять свои записи, подписываться ан любимых авторов и тематические группы.

# Getting Started

Для локального развертывания необходимо выполнить следующие шаги:
- `python manage.py makemigrations`
- `python manage.py migrate`

Далее создаем администратора и запускаем локальный сервер
- `python manage.py createsuperuser`
- `python manage.py runserver`


Для Развертывания на боевом сервере необходимо:
- #### В файле settings.py:
 - Поставить Debug = False
 - Добавить в ALLOWED_HOSTS ip и доменное имя боевого сервера
 - Изменить настройки базы данных к примеру перенести проект на PostgreSQL
- #### На сервере:
  - Перенести на сервер в корень файл .env -  в котором будут храниться настройки базы данных
  - Клонировать проект из данного репозитория на сервер, активировать виртуальное окружение и установить gunicorn
`pip install gunicorn`
  - Установить боевой веб сервер (например nginx) и настроить взаимодействие между проектом и nginx
  - Скачать необходимую библиотеку для работу Python с выбранной базой данных 
  
# Built With
* Django v:3.1.3