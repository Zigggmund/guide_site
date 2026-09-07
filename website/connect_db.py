import psycopg2
from flask import request

def connect():
    conn = psycopg2.connect(
        host="90.156.229.71",
        database="default_db",
        user="gen_user",
        password="j>X<VdW1Y/;t%/"
    )

    return conn

def init_db():
    """Функция инициализации базы данных при старте приложения"""
    conn = connect()
    cur = conn.cursor()
    
    try:
        # Формируем путь к файлу init_db.sql относительно текущего скрипта
        current_dir = os.path.dirname(__file__)
        sql_file_path = os.path.join(current_dir, 'init_db.sql')
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            
        # Выполняем весь DDL скрипт
        cur.execute(sql_script)
        conn.commit()
        print("База данных успешно инициализирована (таблицы проверены/созданы).")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при инициализации базы данных: {e}")
    finally:
        cur.close()
        conn.close()


# ПЕРЕСОЗДАТЬ ВСЕ БД
# изменить default для profile_image на хэш картинки лк

# print(request.files['../static/img/icons/default_av.png'].read())