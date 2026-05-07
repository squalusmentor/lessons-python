age = int(input("Сколько тебе лет? "))

if age >= 18:
    print("Ты совершеннолетний.")
else:
    print("Ты ещё несовершеннолетний.")


temp = float(input("Какая температура за окном? "))

if temp < 0:
    print("Холодно, надевай куртку.")
elif temp < 15:
    print("Прохладно, возьми кофту.")
elif temp < 25:
    print("Комфортно.")
else:
    print("Жарко!")


login = input("Логин: ")
password = input("Пароль: ")

if login == "admin" and password == "1234":
    print("Добро пожаловать!")
else:
    print("Неверный логин или пароль.")


number = int(input("Введи число: "))

if number > 0:
    print("Положительное")
elif number < 0:
    print("Отрицательное")
else:
    print("Ноль")


year = int(input("Введи год: "))

if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
    print(f"{year} — високосный год.")
else:
    print(f"{year} — обычный год.")


print("\n--- Задача 1: оценка по баллам ---")
score = int(input("Введи балл (0-100): "))

if score >= 90:
    print("Отлично (5)")
elif score >= 75:
    print("Хорошо (4)")
elif score >= 60:
    print("Удовлетворительно (3)")
else:
    print("Неудовлетворительно (2)")


print("\n--- Задача 2: чётное или нечётное ---")
n = int(input("Введи целое число: "))

if n % 2 == 0:
    print(f"{n} — чётное.")
else:
    print(f"{n} — нечётное.")


print("\n--- Задача 3: максимум из трёх ---")
a = float(input("a = "))
b = float(input("b = "))
c = float(input("c = "))

if a >= b and a >= c:
    maximum = a
elif b >= a and b >= c:
    maximum = b
else:
    maximum = c

print(f"Максимум: {maximum}")
