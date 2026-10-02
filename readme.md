# Guide Site

---

### Overview
This is an information website and a collection of articles about tourism in the Krasnoyarsk Territory, featuring an integrated system for listing and promoting professional guide services. 

Four key user roles are implemented:
* Guide: Has the ability to create, edit, and publish advertisements for their tourism services.
* User: Can browse general information about the website, read articles, and view guide offers. Authorized users gain access to writing comments under articles and advertisements.
* Moderator: Holds moderation privileges for the platform, including deleting inappropriate advertisements or comments, as well as managing user profiles (deleting users).
* Administrator: Extends the moderator role and can additionally grant or revoke moderator roles.

This repository represents the server-side backend (REST API) developed in Python using the Flask framework.

### Tech Stack
* Framework: Flask
* Database Driver: psycopg2-binary
* Dedicated ORM: Flask-SQLAlchemy (PostgreSQL)

### Quick Start and Deployment

#### Prerequisites
Before starting the local setup, ensure you have Python 3.8+ installed and a running instance of the PostgreSQL DBMS server.

#### Step-by-Step Installation
1. Clone the repository and navigate to the project root folder:
   ```bash
   git clone https://github.com/Zigggmund/guide_site.git
   cd BlogPointFrontend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   # For Windows Command Prompt: venv\Scripts\activate
   # For Windows Git Bash: source venv/Scripts/activate
   ```

3. Install the required project dependencies from the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

#### Running the Application
To run the local Flask development server, execute the main script directly using Python:
```bash
python main.py
```
Upon a successful launch, the application will become available for sending requests at: http://127.0.0.1:5000/

---

### Аннотация
Это информационный веб-сайт и сборник статей о туризме в Красноярском Крае с возможностью размещения и продвижения услуг профессиональных гидов.

Реализованы три ключевые роли пользователей:
* Гид: Имеет возможность создавать, редактировать и публиковать объявления о своих туристических услугах.
* Пользователь: Может просматривать общую информацию о сайте, читать статьи и изучать предложения гидов. Авторизованные пользователи получают доступ к написанию комментариев к статьям и объявлениям.
* Модератор: Обладает правами модерации платформы, включая удаление некорректных объявлений, комментариев, а также управление профилями пользователей (удаление пользователей).
* Администратор: Расширяет роль модератора, может дополнительно выдавать/забирать роли модераторов.

Данный репозиторий представляет собой серверную часть (REST API), разработанную на языке Python.

### Стек
* Фреймворк: Flask
* Драйвер базы данных: psycopg2-binary
* Направленная ORM: Flask-SQLAlchemy (PostgreSQL)

### Быстрый запуск и развёртывание

#### Требования
Перед началом локальной настройки убедитесь, что у вас установлены Python версии 3.8+ и запущен локальный сервер СУБД PostgreSQL.

#### Пошаговая установка
1. Клонируйте репозиторий и перейдите в корень проекта:
   ```bash
   git clone https://github.com/Zigggmund/guide_site.git
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