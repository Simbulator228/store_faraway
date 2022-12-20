import psycopg2


class Database:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="faraway",
            user="postgres",
            password="1234",
            host="localhost",
            port=5432
        )
        self.cur = self.con.cursor()

    def is_exist_login(self, login):
        self.cur.execute(f"SELECT login FROM users WHERE login = '{login}'")
        if self.cur.fetchone():
            return True
        else:
            return False

    def add_user(self, login, password, name, surname):
        try:
            self.cur.execute(
                f"INSERT INTO users (login, password, name, surname) values('{login}', '{password}', '{name}', '{surname}')")
            self.con.commit()
            return True
        except:
            return False

    def get_user(self, user_login):
        self.cur.execute(f"SELECT * FROM users WHERE login='{user_login}'")
        res = self.cur.fetchone()
        if not res:
            print('Такого пользователя не существует')
            return False

        return res

    def get_product(self, product_id):
        self.cur.execute(f"SELECT * FROM products WHERE id='{product_id}'")
        res = self.cur.fetchone()
        if not res:
            print('Такого товара не существует')
            return False

        return res

    def add_product(self, price, name, info, rating, img):
        self.cur.execute(
            f"INSERT INTO products (price, name, info, rating, img) values({price}, '{name}', '{info}', {rating}, '{img})'")
        self.con.commit()
        return True
        # except:
        #     return False

    def get_products(self):
        self.cur.execute(f"SELECT * FROM products")
        res = self.cur.fetchall()
        if not res:
            print('База данных пустая')
            return False

        return res

    def add_wishlist(self, user, product):
        user_id = user[0]
        self.cur.execute(
            f"INSERT INTO whishlist (person_id, product_id, is_favorite) values({user_id}, {product}, True)")
        self.con.commit()

    def person_whishlist(self, user_id):
        self.cur.execute(f"SELECT product_id FROM whishlist WHERE person_id={user_id}")
        res = self.cur.fetchall()
        return res
