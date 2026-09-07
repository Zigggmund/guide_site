-- расширение для хеширования паролей
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1. таблица статей (articles)
CREATE TABLE IF NOT EXISTS articles (
    article_id serial PRIMARY KEY,
    last_update timestamp DEFAULT current_timestamp,
    article_url text NOT NULL,
    article_title text NOT NULL,
    CONSTRAINT lowercase_url CHECK (article_url = lower(article_url))
);

COMMENT ON COLUMN articles.last_update IS 'ONLY DEFAULT VALUE! To not give!';
COMMENT ON COLUMN articles.article_url IS 'store lowercase values(used for url)!';

-- 2. таблица пользователей (users)
CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY,
    user_name varchar(20) NOT NULL,
    user_date_of_birth date NOT NULL,
    user_email text NOT NULL,
    user_login varchar(20) NOT NULL UNIQUE,
    user_password varchar(100) NOT NULL,
    user_consent_messages boolean NOT NULL DEFAULT true,
    user_image bytea,
    user_date date DEFAULT current_date,
    CONSTRAINT unique_name UNIQUE (user_name),
    CONSTRAINT user_constraints CHECK (
        (date_part('year', age(current_timestamp, user_date_of_birth)) < 100) AND 
        (length(user_password) >= 8) AND 
        (length(user_login) >= 3)
    )
);

COMMENT ON COLUMN users.user_name IS 'UNIQUE name (by the way, it solved a problem with unique ADMIN name)';
COMMENT ON COLUMN users.user_date IS 'ONLY DEFAULT VALUE! To not give!';
COMMENT ON COLUMN users.user_image IS 'If default_img user_image value = NULL';
COMMENT ON COLUMN users.user_email IS 'It is checked before insertion';
COMMENT ON COLUMN users.user_password IS 'Password hash';

-- 3. таблица гидов (guides)
CREATE TABLE IF NOT EXISTS guides (
    guide_id integer NOT NULL PRIMARY KEY,
    guide_first_name varchar(20) NOT NULL,
    guide_last_name varchar(20) NOT NULL,
    guide_father_name varchar(20) NOT NULL,
    guide_info text DEFAULT '-',
    guide_phone_number text NOT NULL,
    guide_passport varchar(11) NOT NULL,
    guide_licence_date date NOT NULL,
    guide_licence_number text NOT NULL,
    guide_confirmation boolean NOT NULL DEFAULT true,
    guide_date date DEFAULT current_date,
    FOREIGN KEY (guide_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT min_length_names CHECK (
        (length(guide_first_name) >= 2) AND 
        (length(guide_last_name) >= 2) AND 
        (length(guide_father_name) >= 2)
    ),
    CONSTRAINT check_phone CHECK (
        (left(guide_phone_number, 1) = '8') AND 
        (length(replace(guide_phone_number, ' ', '')) = 11) AND 
        (guide_phone_number ~ '^[0-9\s]+$')
    ),
    CONSTRAINT check_passport CHECK (
        (length(left(guide_passport, strpos(guide_passport, ' ') - 1)) = 4) AND 
        ((length(guide_passport) - length(right(guide_passport, strpos(guide_passport, ' ')))) = 6)
    ),
    CONSTRAINT check_licence CHECK (
        (guide_licence_date < current_date) AND 
        ((length(guide_licence_number) = 14) OR (length(guide_licence_number) = 13)) AND 
        (guide_licence_number LIKE '%-%-%-%')
    )
);

COMMENT ON COLUMN guides.guide_date IS 'ONLY DEFAULT VALUE! To not give!';
COMMENT ON COLUMN guides.guide_passport IS 'SERIES&SPACE&NUMBER';
COMMENT ON COLUMN guides.guide_licence_number IS 'like 89-Э-00105- 22 or 89-Э-00105-22';
COMMENT ON COLUMN guides.guide_phone_number IS 'check ignores spaces; stored with spaces and it’s needed to replace them when we get value';

-- 4. функция и триггер для удаления пробелов
CREATE OR REPLACE FUNCTION remove_spaces() RETURNS trigger AS $$
BEGIN
    NEW.guide_phone_number = REPLACE(NEW.guide_phone_number, ' ', '');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS t_remove_spaces ON guides;
CREATE TRIGGER t_remove_spaces 
BEFORE INSERT OR UPDATE ON guides
FOR EACH ROW EXECUTE PROCEDURE remove_spaces();

-- 5. таблица комментариев к статьям (article_comments)
CREATE TABLE IF NOT EXISTS article_comments (
    article_comment_id serial PRIMARY KEY,
    article_id integer NOT NULL REFERENCES articles(article_id) ON DELETE CASCADE,
    user_id integer NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    comment_rate integer CHECK ((comment_rate IS NULL) OR ((comment_rate >= 1) AND (comment_rate <= 10))),
    comment_text text NOT NULL CHECK (length(comment_text) >= 1),
    comment_date date DEFAULT current_date,
    comment_images bytea[],
    user_image bytea,
    user_name varchar(20) NOT NULL,
    user_type integer DEFAULT 1 NOT NULL CHECK (user_type > 0 AND user_type < 10)
);

COMMENT ON COLUMN article_comments.user_name IS 'NOT CHECKED!!! only for display user name on page';
COMMENT ON COLUMN article_comments.comment_date IS 'ONLY DEFAULT VALUE! To not give!';
COMMENT ON COLUMN article_comments.comment_rate IS 'Article comments may not have a rate';
COMMENT ON COLUMN article_comments.user_type IS 'number from 1 to 9, where 1-user, 2-guide, 9-admin';

-- 6. таблица объявлений гидов (ads)
CREATE TABLE IF NOT EXISTS ads (
    ad_id serial PRIMARY KEY,
    guide_id integer NOT NULL REFERENCES guides(guide_id) ON DELETE CASCADE,
    article_id integer NOT NULL REFERENCES articles(article_id) ON DELETE CASCADE,
    ad_text text NOT NULL CHECK (length(ad_text) >= 1),
    ad_date date DEFAULT current_date,
    user_image bytea,
    user_name varchar(20) NOT NULL,
    guide_phone_number text NOT NULL CHECK (
        (left(guide_phone_number, 1) = '8') AND 
        (length(replace(guide_phone_number, ' ', '')) = 11) AND 
        (guide_phone_number ~ '^[0-9\s]+$')
    ),
    ad_images bytea[],
    category_for_other text NOT NULL DEFAULT '=БЕЗ КАТЕГОРИИ='
);

COMMENT ON COLUMN ads.ad_date IS 'ONLY DEFAULT VALUE! To not give!';
COMMENT ON COLUMN ads.ad_id IS 'There is a view counting general ad rate';

-- 7. таблица комментариев к объявлениям (ad_comments)
CREATE TABLE IF NOT EXISTS ad_comments (
    ad_comment_id serial PRIMARY KEY,
    article_id integer NOT NULL REFERENCES articles(article_id) ON DELETE CASCADE,
    user_id integer NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    ad_id integer NOT NULL REFERENCES ads(ad_id) ON DELETE CASCADE,
    ad_comment_rate integer NOT NULL CHECK ((ad_comment_rate >= 1) AND (ad_comment_rate <= 10)),
    ad_comment_text text NOT NULL CHECK (length(ad_comment_text) >= 1),
    ad_comment_date date DEFAULT current_date,
    ad_comment_images bytea[],
    user_image bytea,
    user_name varchar(20) NOT NULL,
    user_type integer DEFAULT 1 NOT NULL CHECK (user_type > 0 AND user_type < 10)
);

COMMENT ON COLUMN ad_comments.user_type IS 'number from 1 to 9, where 1-user, 2-guide, 9-admin';
COMMENT ON COLUMN ad_comments.ad_comment_date IS 'ONLY DEFAULT VALUE! To not give!';
COMMENT ON COLUMN ad_comments.ad_comment_rate IS 'Every comment must have a certain rate';

-- 8. представления
CREATE OR REPLACE VIEW average_ad_rates AS 
SELECT ads.article_id, ads.ad_id, ads.guide_id,
       (SELECT AVG(ac.ad_comment_rate) FROM ad_comments ac WHERE ac.ad_id = ads.ad_id AND ac.article_id = ads.article_id) AS average_ad_rate
FROM ads;

CREATE OR REPLACE VIEW amounts_of_comments AS 
SELECT ads.article_id, ads.ad_id, ads.guide_id,
       (SELECT count(*) FROM ad_comments ac WHERE ac.ad_id = ads.ad_id AND ac.article_id = ads.article_id) AS amount_of_comments
FROM ads;

CREATE OR REPLACE VIEW full_ads_info AS 
SELECT ads.guide_id, ads.article_id, ads.ad_id, ads.ad_text, ads.ad_date, ads.user_image, ads.user_name, ads.guide_phone_number, ads.ad_images,
       round(aar.average_ad_rate, 2) AS average_ad_rate,
       aoc.amount_of_comments
FROM ads 
JOIN average_ad_rates AS aar ON aar.article_id = ads.article_id AND aar.ad_id = ads.ad_id
JOIN amounts_of_comments AS aoc ON aoc.article_id = ads.article_id AND aoc.ad_id = ads.ad_id
ORDER BY ad_date DESC;

CREATE OR REPLACE VIEW users_lk AS 
SELECT u.user_id, u.user_name, u.user_image, u.user_date,
       (SELECT count(*) FROM article_comments ar WHERE ar.user_id = u.user_id) + 
       (SELECT count(*) FROM ad_comments ad WHERE ad.user_id = u.user_id) AS user_comments_count,
       u.user_date_of_birth, u.user_login, u.user_password
FROM users u;

CREATE OR REPLACE VIEW guides_lk AS 
SELECT u.user_id, u.user_name, u.user_image, u.user_date,
       (SELECT count(*) FROM article_comments ar WHERE ar.user_id = u.user_id) + 
       (SELECT count(*) FROM ad_comments ad WHERE ad.user_id = u.user_id) AS user_comments_count,
       u.user_date_of_birth, u.user_login, u.user_password,
       g.guide_info, g.guide_date,
       (SELECT count(*) FROM ads WHERE ads.guide_id = g.guide_id) AS guide_ads_count,
       (SELECT avg(av.average_ad_rate) FROM average_ad_rates av WHERE av.guide_id = g.guide_id) AS guide_average_rate
FROM guides g 
LEFT OUTER JOIN users u ON u.user_id = g.guide_id;

-- 9. админ
INSERT INTO users (user_name, user_date_of_birth, user_email, user_login, user_password, user_type)
SELECT 'ADMIN', '2000-01-01', 'admin@mail.ru', 'admin_1zcjawj12394', crypt('3v{qG82$G@V!&i–', gen_salt('bf')), 9
WHERE NOT EXISTS (SELECT 1 FROM users WHERE user_login = 'admin_1zcjawj12394');
