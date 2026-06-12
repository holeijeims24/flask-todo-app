users = {
    "andriy": "1234",
    "nika": "5678"
}

login = input("Введи логін: ")

if login in users:
    print("Користувач існує")
else:
    print("Користувача не знайдено")
