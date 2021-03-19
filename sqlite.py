import sqlite3


class SQLight:
    def __init__(self, database_file):
        """Подключаемся к БД"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        """Получаем активных подписчиков"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def get_all_subscriptions(self):
        """Получаем всех подписчиков"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions`")

    def subscriber_exists(self, user_id):
        """Проверяем есть ли юсер в базе"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `subscriptions` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES (?,?)",
                                       (user_id, status))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки"""
        return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
        """Закрываем соединение с бд"""
        self.connection.close()


class SQLrand:
    def __init__(self, database_file):
        """Подключаемся к БД"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_users(self):
        """Получаем всех подписчиков"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users`")

    def user_exists(self, user_id):
        """Проверяем есть ли юсер в базе"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, status):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `status`) VALUES (?,?)", (user_id, status))

    def deliteusers(self):
        with self.connection:
            return self.cursor.execute("DELETE FROM `users`")

    def close(self):
        """Закрываем соединение с бд"""
        self.connection.close()
