# Урок 2 — Переменные: числа и строки

# --- Целые числа (int) ---
a = 10
b = 3

print("Сложение:     ", a + b)   # 13
print("Вычитание:    ", a - b)   # 7
print("Умножение:    ", a * b)   # 30
print("Деление:      ", a / b)   # 3.333...
print("Целое деление:", a // b)  # 3
print("Остаток:      ", a % b)   # 1
print("Степень:      ", a ** b)  # 1000

# --- Дробные числа (float) ---
height = 1.75  # pylint: disable=invalid-name
weight = 60.5

print("Рост:", height)
print("Вес:", weight)
print("ИМТ:", round(weight / (height ** 2), 2))

# --- Строки (str) ---
name = "Антон"
surname = ""

# Склейка строк (конкатенация)
full_name = name + " " + surname
print("Полное имя:", full_name)

# f-строки — удобный способ вставить переменную в текст
age = 20
print(f"Привет, {name}! Тебе {age} лет.")

# Длина строки
print("Букв в имени:", len(name))

# Методы строк
print(name.upper())
print(name.lower())
print("  пробелы  ".strip())  # убирает пробелы по краям
