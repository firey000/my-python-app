import mysql.connector
from config import DATABASE_CONFIG

conn = mysql.connector.connect(**DATABASE_CONFIG)
cursor = conn.cursor()

with open('schema.sql', 'r') as f:
    for line in f.readlines():
        if line.strip():  # Пропускаем пустые строки
            cursor.execute(line)

# Добавляем пользователей и заказы
users = [
    {'username': 'User1', 'email': 'user1@example.com'},
    {'username': 'User2', 'email': 'user2@example.com'}
]
orders = [
    {'order_id': 1, 'user_id': 1, 'amount': 100},
    {'order_id': 2, 'user_id': 2, 'amount': 200}
]

for user in users:
    cursor.execute("INSERT INTO users(username, email) VALUES (%s, %s)", (user['username'], user['email']))

for order in orders:
    cursor.execute("INSERT INTO orders(order_id, user_id, amount) VALUES (%s, %s, %s)",
                   (order['order_id'], order['user_id'], order['amount']))

conn.commit()
cursor.close()
conn.close()
