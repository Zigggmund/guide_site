from flask import Blueprint, render_template, request, flash, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .connect_db import *

auth = Blueprint('auth', __name__)

# есть 2 основных типа запросов - get и post
# route нужно знать, какой запрос: get или post
# get, например, загружает html
# post менят состояние сайта/бд

@auth.route('/log_in', methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        if 'is_guide' in session: session.pop('is_guide') # при смене аккаунта для гида

        conn = connect()
        cur = conn.cursor()
        try:
            cur.execute(f"SELECT * FROM users WHERE user_login = '{request.form['user_login']}' AND user_password = '{request.form['user_password']}'")
            user_info = cur.fetchall()[0]

            flash('Вход совершен')
            session['user_id'] = user_info[0]
            
            cur.execute(f'SELECT * FROM guides WHERE guide_id={session["user_id"]}')
            guide_info = cur.fetchall()
            if len(guide_info) > 0: session['is_guide'] = 'true'

            if check_admin(user_info): session['is_admin'] = 'true'
            return redirect('/profile')
        except (IndexError):
            flash('Такого пользователя не существует: Перепроверьте логин и пароль', 'error')
        except (Exception):
            flash('Вход не совершен: Неизвестная ошибка', 'error')
        conn.close(), cur.close()
    return render_template('auth/log_in.html', boolean=True)

@auth.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        conn = connect()
        cur = conn.cursor()

        try:
            # если уже есть такой логин
            cur.execute(f"SELECT * FROM users WHERE user_login = '{request.form['user_login']}'")
            if len(cur.fetchall()) > 0:
                flash('Регистрация не завершена: Пользователь с таким логином уже есть', 'error')
                raise ValueError

            user_cm = 'true' if len(request.form.getlist('user_consent_messages')) == 1 else 'false'
            cur.execute(f'''insert into users
            (user_name, user_date_of_birth, user_email, 
            user_login, user_password, user_consent_messages)
            values(
                '{request.form['user_name']}',
                '{request.form['user_date_of_birth']}',
                '{request.form['user_email']}',
                '{request.form['user_login']}',
                '{request.form['user_password']}',
                {user_cm}
                );
            ''')

            if request.form['user_password'] != request.form['user_password2']:
                flash('Регистрация не завершена: Ошибка при проверке паролей(пароли не равны между собой)', 'error')
                raise ValueError
            if request.form['user_name'] != request.form['user_name'].lower():
                flash('Регистрация не завершена: Ошибка при валидации имени(превышена макс длина - 20 или имя содержит заглавные буквы)', 'error')
                raise ValueError

            flash('Регистрация прошла успешно')
            conn.commit()
            if 'is_guide' in session: session.pop('is_guide')

            cur.execute(f"SELECT * FROM users WHERE user_login = '{request.form['user_login']}' AND user_password = '{request.form['user_password']}'")
            user_info = cur.fetchall()[0]
            session['user_id'] = user_info[0]

            return redirect('/profile')
        except ValueError: pass
        except psycopg2.Error:
            if len(request.form['user_name']) > 20:
                flash('Регистрация не завершена: Ошибка при валидации имени(превышена макс длина - 20 или имя содержит заглавные буквы)', 'error')
            elif len(request.form['user_login']) < 3 or len(request.form['user_name']) > 20:
                flash('Регистрация не завершена: Ошибка при валидации логина(требуемый диапозон от 3 до 20)', 'error')
            elif len(request.form['user_password']) < 8 or len(request.form['user_name']) > 20:
                flash('Регистрация не завершена: Ошибка при валидации пароля(требуемый диапозон от 8 до 20)', 'error')
            else: 
                flash('''Регистрация не завершена: Ошибка при валидации даты 
                (слишком старая дата или неправильный формат). 
                Пример: 2002-12-01 ''', 'error')
        except (Exception):
            flash('Регистрация не завершена: Неизвестная ошибка', 'error')
        conn.close(), cur.close()
    return render_template('auth/sign_up.html', boolean=True)

@auth.route('/confirm_email', methods=['POST', 'GET'])
def confirm_email():
    # ДОДЕЛАТЬ
    return render_template('auth/confirm_email.html', boolean=True)

@auth.route('/become_a_guide', methods=['POST', 'GET'])
def become_a_guide():
    if request.method == 'POST':
        conn = connect()
        cur = conn.cursor()
        try:
            if len(request.form["guide_info"]) > 0:
                cur.execute(f'''insert into guides
                    (guide_id, guide_first_name, guide_last_name, guide_father_name, 
                    guide_info, guide_phone_number, guide_passport, 
                    guide_licence_number, guide_licence_date) 
                    values(
                    {session['user_id']},
                    '{request.form['guide_first_name']}',
                    '{request.form['guide_last_name'] }',
                    '{request.form['guide_father_name'] }',
                    '{request.form['guide_info']}',
                    '{request.form['guide_phone_number'] }',
                    '{request.form['passport-series']+' '+request.form['passport-number']}',
                    '{request.form['guide_licence_number'] }',
                    '{request.form['guide_licence_date'] }'
                    );
                ''')
            else:
                cur.execute(f'''insert into guides
                    (guide_id, guide_first_name, guide_last_name, 
                    guide_father_name, guide_phone_number, guide_passport, 
                    guide_licence_number, guide_licence_date) 
                    values(
                    {session['user_id']},
                    '{request.form['guide_first_name']}',
                    '{request.form['guide_last_name'] }',
                    '{request.form['guide_father_name'] }',
                    '{request.form['guide_phone_number'] }',
                    '{request.form['passport-series']+' '+request.form['passport-number']}',
                    '{request.form['guide_licence_number'] }',
                    '{request.form['guide_licence_date'] }'
                    );
                ''')
            session['is_guide'] = 'true'
            flash('Регистрация успешно завершена') # можно убрать
            conn.commit()

            return redirect('/guide_profile')
        # except ValueError: pass
        except psycopg2.Error as e:
            print('!!!', e)
            flash('Регистрация гида не завершена: Ошибка в заполнении формы.', 'error')
            flash('---Возможные ошибки--- ', 'error')
            flash('1. Фамилия - Длина должна быть в пределах от 2 до 20', 'error')
            flash('2. Имя - Длина должна быть в пределах от 2 до 20', 'error')
            flash('3. Отчество - Длина должна быть в пределах от 2 до 20', 'error')
            flash('4. -', 'error')
            flash('5. Номер телефона - Корректный номер телефона(пробелы не учитываются), должен начинаться с 8. Пример 8 900 000 00 00', 'error')
            flash('6. Серия паспорта - 4 цифры.', 'error')
            flash('7. Номер паспорта - 6 цифр.', 'error')
            flash('8. Номер лицензии - длиной 14(13) символов, формат в примере. Пример 12-19312-1-16', 'error')
            flash('9. Дата получения - Невозможное значение/формат даты. Пример: 2023-10-10)', 'error')
        except (Exception):
            flash('Регистрация гида не завершена: Неизвестная ошибка', 'error')
        conn.close()
        cur.close()
    else:
        if 'user_id' not in session:
            return redirect('/auth/log_in')
    return render_template('auth/become_a_guide.html', boolean=True)


def check_admin(user_info):
    if user_info[4] == 'admin_1zcjawj12394':
        return 'true'