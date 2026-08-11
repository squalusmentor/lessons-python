# Урок L5.5 — property: умные атрибуты
#
# property превращает метод в "атрибут с логикой": снаружи это обычное obj.x,
# а внутри — геттер/сеттер. В Python НЕ пишут get_x()/set_x() как в Java:
# начинают с простого атрибута, а когда понадобится валидация — превращают его
# в property. Внешний код при этом НЕ меняется.


class Temperature:
    def __init__(self, celsius: float = 0.0):
        # Присваивание пойдёт через сеттер ниже -> валидация работает уже в __init__.
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("ниже абсолютного нуля нельзя")
        self._celsius = value

    # ВЫЧИСЛЯЕМОЕ свойство только для чтения: сеттера нет, хранить нечего.
    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32


class Item:
    """Тот же приём защитит количество на складе (пригодится в практике)."""

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity          # через сеттер

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValueError("количество не может быть отрицательным")
        self._quantity = value


def demo5():
    print("-- property выглядит как обычный атрибут --")
    t = Temperature(25)
    print("  t.celsius =", t.celsius)         # вызвался геттер
    print("  t.fahrenheit =", t.fahrenheit)   # вычисляемое свойство
    t.celsius = 30                            # вызвался сеттер
    print("  после t.celsius = 30:", t.fahrenheit)

    print("-- валидация в сеттере (и в __init__ тоже) --")
    try:
        t.celsius = -300
    except ValueError as e:
        print("  поймали:", e)

    print("-- свойство только для чтения --")
    try:
        t.fahrenheit = 100
    except AttributeError:
        print("  поймали: вычисляемому свойству нельзя присвоить значение")

    print("-- та же защита в Item.quantity --")
    it = Item("Гвоздь", 100)
    it.quantity -= 30                         # читаем геттером, пишем сеттером
    print("  осталось:", it.quantity)
    try:
        it.quantity = -5
    except ValueError as e:
        print("  поймали:", e)


if __name__ == "__main__":
    demo5()
