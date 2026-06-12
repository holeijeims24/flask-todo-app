users = {
    "andriy": "1234",
    "nika": "5678"
}

login = input("Логін: ")
password = input("Пароль: ")

if login in users and users[login] == password:
    print("Вхід успішний!")
else:
    print("Невірний логін або пароль")
