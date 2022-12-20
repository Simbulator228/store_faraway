class UserLogin:
    def fromDB(self, user_id, db):  # Вытаскиваем данные из бдщки, по юзеру
        self.__user = db.get_user(user_id)
        return self

    def create(self, user):  # Так передаем информацию о пользователе
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonyumus(self):
        return False

    def get_id(self):
        return str(self.__user[0])  # Чтобы фласк_логин мог понять, что за пользователь

