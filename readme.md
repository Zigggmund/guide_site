# Guide Site

---

### Project Overview
BlogPoint is an information website and a collection of articles about tourism in the Krasnoyarsk Territory, featuring an integrated system for listing and managing guide services. 

The backend architecture implements business logic for three primary actor groups defined in the system requirements:
* Guide: Can create, format, and publish travel advertisements and service listings.
* User: Can browse information about the website, read articles, and view guide offers. Authenticated users can write comments under articles or service listings.
* Administrator: Holds elevated privileges to moderate the platform, including deleting inappropriate advertisements, comments, or blocking users.

This repository contains the REST API backend implemented in Python using the Flask framework.

### Tech Stack
* Framework: Flask
* Database Driver: psycopg2-binary
* ORM: Flask-SQLAlchemy (PostgreSQL)

### Deployment

#### Prerequisites
Before setting up the project locally, ensure you have Python 3.8+ and a running PostgreSQL instance installed on your machine.

#### Local Installation and Setup
1. Clone the repository and navigate to the project root folder:
   ```bash
   git clone https://github.com
   cd BlogPointFrontend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   # For Windows Command Prompt: venv\Scripts\activate
   # For Windows Git Bash: source venv/Scripts/activate
   ```

3. Install all required project dependencies from the configuration file:
   ```bash
   pip install -r requirements.txt
   ```

#### Running the Application
To run the Flask development server locally, execute the main script directly using Python:
```bash
python main.py
```
By default, the server will initialize and become accessible at http://127.0.0.1:5000/

---

### Аннотация проекта (Overview)
BlogPoint — это информационный веб-сайт и сборник статей о туризме в Красноярском Крае с возможностью размещения и продвижения услуг профессиональных гидов.

Архитектура бэкенда реализует бизнес-логику для трех ключевых ролей пользователей, определенных диаграммой прецедентов:
* Гид: Имеет возможность создавать, редактировать и публиковать объявления о своих туристических услугах.
* Пользователь: Может просматривать общую информацию о сайте, читать статьи и изучать предложения гидов. Авторизованные пользователи получают доступ к написанию комментариев к статьям и объявлениям.
* Администратор: Обладает правами модерации платформы, включая удаление некорректных объявлений, комментариев, а также управление профилями пользователей (удаление пользователей).

Данный репозиторий представляет собой серверную часть (REST API), разработанную на языке Python.

### Технологический стек
* Фреймворк: Flask
* Драйвер базы данных: psycopg2-binary
* Направленная ORM: Flask-SQLAlchemy (PostgreSQL)

### Быстрый запуск и развёртывание

#### Требования
Перед началом локальной настройки убедитесь, что у вас установлены Python версии 3.8+ и запущен локальный сервер СУБД PostgreSQL.

#### Пошаговая установка
1. Клонируйте репозиторий и перейдите в корень проекта:
   ```bash
   git clone https://github.com
   cd BlogPointFrontend
   ```

2. Создайте и активируйте виртуальное окружение Python:
   ```bash
   python -m venv venv
   source venv/bin/activate
   # Для Windows Command Prompt: venv\Scripts\activate
   # Для Windows Git Bash: source venv/Scripts/activate
   ```

3. Установите необходимые зависимости из файла требований:
   ```bash
   pip install -r requirements.txt
   ```

#### Запуск приложения
Для запуска локального сервера разработки Flask выполните главный скрипт напрямую через Python:
```bash
python main.py
```
После успешного запуска приложение станет доступно для отправки запросов по адресу: http://127.0.0.1:5000/