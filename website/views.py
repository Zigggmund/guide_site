# для создания компонентов приложений и поддержки общих шаблонов внутри приложения или между приложениями.
from flask import Blueprint, render_template, session, redirect, flash, request
from .connect_db import *
import psycopg2

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/<is_logout>')
def home_logout(is_logout):
    print('LOGOUT')
    # для выхода из аккаунта
    print('!!!')
    print(session)
    if is_logout:
        if 'is_guide' in session: session.pop('is_guide')
        if 'user_id' in session: session.pop('user_id')
        if 'is_admin' in session: session.pop('is_admin')
    print(session)
    return render_template('home.html')


@views.route('/error<error_title><error_text>')
def error(error_title, error_text):
    return render_template('error.html', error_title=error_title, error_text=error_text)

@views.route('/about_site')
def about_site():
    return render_template('about_site.html')

@views.route('/contacts')
def contacts():
    return render_template('contacts.html')

@views.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/auth/log_in')
    else:
        conn = connect()
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM users_lk WHERE user_id = {session["user_id"]}')
        try:
            cur.fetchall()[0]
        except Exception:
            conn.close(), cur.close()
            flash('ВАШ АККАУНТ БЫЛ УДАЛЕН', 'error')
            if 'user_id' in session: session.pop('user_id')
            if 'is_guide' in session: session.pop('is_guide')
            return redirect('/auth/log_in')

        if 'is_guide' in session:
            return redirect('/guide_profile')
        else:
            cur.execute(f'SELECT * FROM users_lk WHERE user_id = {session["user_id"]}')
            user_info = cur.fetchall()[0]
            print(user_info)
            conn.close(), cur.close()
            return render_template('profile.html', user_info=user_info)

@views.route('/profile<id>', methods=['GET', 'POST'])
def profile_with_id(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM users_lk WHERE user_id = {id}')
    try:
        cur.fetchall()[0]
    except Exception:
        conn.close(), cur.close()
        flash('Пользователь, профиль которого вы хотели посмотреть, удален', 'error')
        return redirect(request.referrer)

    # УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
    if request.method == 'POST':
        try:
            cur.execute(f'DELETE FROM users WHERE user_id={id}')
            flash('Пользователь удален')
            conn.commit()
        except psycopg2.Error:
            flash('Ошибка удаления пользователя, неизвестная ошибка', 'error')
        return redirect('/')

    cur.execute(f'SELECT * from guides WHERE guide_id = {id}')
    # если человек является гидом
    if len(cur.fetchall()) > 0:
        return redirect(f'/guide_profile{id}')
    else:
        cur.execute(f'SELECT * FROM users_lk WHERE user_id = {id}')
        user_info = cur.fetchall()[0]
        print(user_info)
        if len(user_info) == 0:
            error_title = 'Ошибка профиля'
            error_text = 'Профиля этого пользователя не существует'
            redirect(f'/error<{error_title}><{error_text}>')
        else:
            conn.close(), cur.close()
            return render_template('profile.html', user_info=user_info)

@views.route('/guide_profile')
def guide_profile():
    conn = connect()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM guides_lk WHERE user_id = {session["user_id"]}')
    guide_info = cur.fetchall()[0]
    print(guide_info)
    conn.close(), cur.close()
    return render_template('guide_profile.html', user_info=guide_info)

@views.route('/guide_profile<id>', methods=['GET', 'POST'])
def guide_profile_with_id(id):
    conn = connect()
    cur = conn.cursor()

    # УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
    if request.method == 'POST':
        try:
            cur.execute(f'DELETE FROM users WHERE user_id={id}')
            flash('Пользователь удален')
            conn.commit()
        except psycopg2.Error:
            flash('Ошибка удаления пользователя, неизвестная ошибка', 'error')
        return redirect('/')

    cur.execute(f'SELECT * FROM guides_lk WHERE user_id = {id}')
    guide_info = cur.fetchall()[0]
    print(guide_info)
    conn.close(), cur.close()
    return render_template('guide_profile.html', user_info=guide_info)