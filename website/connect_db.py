import psycopg2
from flask import request

def connect():
    conn = psycopg2.connect(
        host="147.45.140.252",
        database="default_db",
        user="gen_user",
        password="j>X<VdW1Y/;t%/"
    )

    return conn

# пока не работает
def get_image(pid):
    image_binary = read_image(pid)
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % pid)
    return response

# ПЕРЕСОЗДАТЬ ВСЕ БД
# изменить default для profile_image на хэш картинки лк

# print(request.files['../static/img/icons/default_av.png'].read())