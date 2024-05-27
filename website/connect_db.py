import psycopg2

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
# изменить тип user_date_of_birh на date 
# изменить default для profile_image на хэш картинки лк
# изменить тип password на bytea