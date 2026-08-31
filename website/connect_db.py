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

# ПЕРЕСОЗДАТЬ ВСЕ БД
# изменить default для profile_image на хэш картинки лк

# print(request.files['../static/img/icons/default_av.png'].read())