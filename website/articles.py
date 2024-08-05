from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import psycopg2
from .connect_db import *

articles = Blueprint('articles', __name__)


# ДИНАМИЧЕСКОЕ СОЗДАНИЕ ФУНКЦИЙ
# открываем курсор для генерации функций
conn = connect()
cur = conn.cursor()
cur.execute('SELECT * FROM articles')
articles_list = cur.fetchall()
# закрываем для генерации функций
cur.close(), conn.close()
def generate_func():
    for article in articles_list:
        @articles.route(f'/{article[2]}', methods=['GET', 'POST'])

        # ARTICLES
        def __dynamic_func():
            conn = connect()
            cur = conn.cursor()
            article = request.path.split("/")[-1]
            cur.execute(f"SELECT * FROM articles WHERE article_url = '{article}'")
            article = cur.fetchall()[0]
            if request.method == 'POST':

                # ДОБАВИТЬ КОММЕНТАРИЙ
                if request.form['submit_button'] == 'write-comm':
                    print('*ARTICLE DATA SEND ATTEMPT*')
                    cur.execute(f'SELECT user_name FROM users WHERE user_id = {session["user_id"]}')
                    user_name = cur.fetchall()[0][0]
                    try:
                        if len(request.form["comment_text"]) > 0:
                            if len(request.form["comment_rate"]) == 0:
                                cur.execute(f'''INSERT INTO article_comments(article_id, user_id, comment_text, user_name)
                                VALUES(
                                {article[0]},
                                {session["user_id"]},
                                '{request.form["comment_text"]}',
                                '{user_name}'
                                );''')
                            else:
                                cur.execute(f'''INSERT INTO article_comments(article_id, user_id, comment_rate, comment_text, user_name) VALUES(
                                {article[0]},
                                {session["user_id"]},
                                {int(request.form["comment_rate"])},
                                '{request.form["comment_text"]}',
                                '{user_name}'
                                );''')
                            flash('Комментарий добавлен')
                            conn.commit()
                        else:
                            flash('Комментарий не добавлен: Текстовое поле пустое', 'error')
                    except (ValueError):
                        flash('Комментарий не добавлен: Оценка должна быть целым числом', 'error')
                    except psycopg2.Error as err:
                        print('!!!', err)
                        flash('Комментарий не добавлен: Диапозон оценки: от 0 до 10', 'error')
                    except (Exception):
                        flash('Комментарий не добавлен: Неизвестная ошибка', 'error')

                # УДАЛИТЬ КОММЕНТАРИЙ
                else:
                    comment_id = request.form['submit_button']
                    try:
                        cur.execute(f'DELETE FROM article_comments WHERE article_comment_id={comment_id} AND article_id={article[0]};')
                        flash('Комментарий удален')
                        conn.commit()
                    except psycopg2.Error as err:
                        flash('Удаление не произведено, неизвестная ошибка', 'error')
                    
                # откатить транзакцию при ошибке
                cur.close(), conn.close()
                conn = connect()
                cur = conn.cursor()

            cur.execute(f'SELECT * FROM article_comments WHERE article_id={article[0]} ORDER BY comment_date')
            article_comments = cur.fetchall()
            print('-----', article_comments, type(article_comments), len(article_comments), '-----', sep='\n')
            cur.close(), conn.close()
            if article[2] != 'other':
                return render_template(f'article-pages/{request.path.split("/")[-1]}.html', article_info=article, article_comments=article_comments)
            else:
                return redirect(url_for('views.error', error_text='Некорректный URL: Возможно вы хотели перейти к предложениям гидов без категории?'))
        __dynamic_func.__name__ = article[2]

        # ADS
        @articles.route(f'/{article[2]}/ads<sorting>', methods=['POST', 'GET'])
        def __dynamic_func2(sorting):
            sorting = sorting[1:-1]
            conn = connect()
            cur = conn.cursor()
            # нужно, тк после цикла article принимает последний article из бд
            article = request.path.split("/")[-2]
            cur.execute(f"SELECT * FROM articles WHERE article_url = '{article}'")
            article = cur.fetchall()[0]

            if request.method == 'POST':
                print('*AD DATA SEND ATTEMPT*')
                cur.execute(f'SELECT user_name FROM users WHERE user_id = {session["user_id"]}')
                user_name = cur.fetchall()[0][0]

                # НАПИСАТЬ ОБЪЯВЛЕНИЕ
                if request.form['submit_button'] == 'guide':
                    print('WRITING AD')
                    cur.execute(f'SELECT guide_phone_number FROM guides WHERE guide_id = {session["user_id"]}')
                    phone_number = cur.fetchall()[0][0]
                    try:
                        if len(request.form["ad_text"]) > 0:
                            cur.execute(f'''INSERT INTO ads(article_id, guide_id, ad_text, user_name, guide_phone_number) VALUES(
                            {article[0]},
                            {session["user_id"]},
                            '{request.form["ad_text"]}',
                            '{user_name}',
                            '{phone_number}'
                            );''')
                            flash('Объявление добавлено')
                            conn.commit()
                        else:
                            flash('Объявление не добавлено: Текстовое поле пустое', 'error')
                    except (ValueError): pass
                    # except (Exception):
                    #     flash('Объявление не добавлено: Неизвестная ошибка', 'error')

                # НАПИСАТЬ КОММЕНТАРИЙ
                elif 'write' in request.form['submit_button']:
                    print('WRITING AD COMMENT')
                    ad_id = request.form['submit_buttofn'].split('write')[1]
                    comm_text = request.form[f"comment_text{ad_id}"]
                    comm_rate = request.form[f"comment_rate{ad_id}"]
                    try:
                        if len(comm_text) > 0:
                            if len(comm_rate) > 0:
                                cur.execute(f'''INSERT INTO ad_comments(article_id, user_id, ad_id, ad_comment_text, ad_comment_rate, user_name)
                                VALUES(
                                {article[0]},
                                {session["user_id"]},
                                {ad_id},
                                '{comm_text}',
                                {int(comm_rate)},
                                '{user_name}'
                                );''')
                                flash('Комментарий добавлен')
                                conn.commit()
                            else:
                                flash('Комментарий не добавлен: Поле с оценкой пустое', 'error')
                        else:
                            flash('Комментарий не добавлен: Текстовое поле пустое', 'error')
                    except (ValueError):
                        flash('Комментарий не добавлен: Оценка должна быть целым числом', 'error')
                    except psycopg2.Error as err:
                        print('!!!', err)
                        flash('Комментарий не добавлен: Диапозон оценки: от 0 до 10', 'error')
                    except (Exception):
                        flash('Комментарий не добавлен: Неизвестная ошибка', 'error')
                    
                # УДАЛИТЬ ОБЪЯВЛЕНИЕ
                elif ',' not in request.form['submit_button']:
                    print('DELETING AD')
                    ad_id = request.form['submit_button']
                    try:
                        cur.execute(f'DELETE FROM ads WHERE ad_id={ad_id} AND article_id={article[0]};')
                        flash('Объявление удалено')
                        conn.commit()
                    except psycopg2.Error as err:
                        flash('Удаление не произведено, неизвестная ошибка', 'error')
                    

                # УДАЛИТЬ КОММЕНТАРИЙ 
                else:
                    print('DELETING AD COMMENT')
                    ad_id = request.form['submit_button'].split(',')[0]
                    comment_id = request.form['submit_button'].split(',')[1]
                    print(ad_id, comment_id)
                    try:
                        cur.execute(f'DELETE FROM ad_comments WHERE ad_comment_id={comment_id} AND ad_id={ad_id} AND article_id={article[0]};')
                        flash('Комментарий удален')
                        conn.commit()
                    except psycopg2.Error as err:
                        flash('Удаление не произведено, неизвестная ошибка', 'error')

            # откатить транзакцию при ошибке
            cur.close(), conn.close()
            conn = connect()
            cur = conn.cursor()

            if sorting == 'date': cur.execute(f'SELECT * FROM full_ads_info WHERE article_id = {article[0]} ORDER BY ad_date DESC')
            elif sorting == 'rate': cur.execute(f'SELECT * FROM full_ads_info WHERE article_id = {article[0]} ORDER BY average_ad_rate DESC NULLS LAST')
            elif sorting == 'comments': cur.execute(f'SELECT * FROM full_ads_info WHERE article_id = {article[0]} ORDER BY amount_of_comments DESC')
            # в случае ошибки сортируем по дате
            else: cur.execute(f'SELECT * FROM full_ads_info WHERE article_id = {article[0]} ORDER BY ad_date DESC')

            article_ads = cur.fetchall()
            print(article_ads)
            cur.execute(f'SELECT * FROM ad_comments WHERE article_id={article[0]}  ORDER BY ad_comment_date')
            ad_comments = cur.fetchall()
            cur.close(), conn.close()
            return render_template('article-pages/ads.html', article_info=article, article_ads=article_ads, ad_comments=ad_comments, sorting=sorting)
        __dynamic_func2.__name__ = article[2] + '_ads<sorting>'

generate_func()


@articles.route('/')
def home():
    # выводит шаблон home.index из templates
    return render_template('articles.html', articles=[el for el in articles_list if el[2] != 'other'])