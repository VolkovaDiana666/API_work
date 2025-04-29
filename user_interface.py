import sys

def input_float(prompt: str, min_value: float = -float('inf'), max_value: float = float('inf')) -> float:
    while True:
        try:
            value = float(input(prompt))
            if not (min_value <= value <= max_value):
                raise ValueError(f"Введите число от {min_value} до {max_value}")
            return value
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.")

def input_int(prompt: str, min_value: int = -sys.maxsize, max_value: int = sys.maxsize) -> int:
    while True:
        try:
            value = int(input(prompt))
            if not (min_value <= value <= max_value):
                raise ValueError(f"Введите целое число от {min_value} до {max_value}")
            return value
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.")

def input_choice(prompt: str, options: list[str]) -> str:
    while True:
        choice = input(prompt).strip().lower()
        if choice in options:
            return choice
        print(f"Недопустимый выбор. Возможные варианты: {', '.join(options)}")

def main_console():
    polygons = []

    while True:
        print("\nМеню:")
        print("1. Создать прямоугольник")
        print("2. Создать треугольник")
        print("3. Создать шестиугольник")
        print("4. Преобразовать полигон")
        print("5. Визуализировать полигоны")
        print("6. Очистить список")
        print("7. Выйти")

        choice = input_choice("Выберите действие (1-7): ", [str(i) for i in range(1, 8)])

        if choice == "1":
            w = input_float("Ширина прямоугольника: ", 0.1)
            h = input_float("Высота прямоугольника: ", 0.1)
            polygons.append(gen_rectangle(w, h))
            print("Прямоугольник добавлен.")

        elif choice == "2":
            side = input_float("Сторона треугольника: ", 0.1)
            polygons.append(gen_triangle(side))
            print("Треугольник добавлен.")

        elif choice == "3":
            side = input_float("Сторона шестиугольника: ", 0.1)
            polygons.append(gen_hexagon(side))
            print("Шестиугольник добавлен.")

        elif choice == "4":
            if not polygons:
                print("Список полигонов пуст.")
                continue

            index = input_int(f"Выберите полигон (0-{len(polygons)-1}): ", 0, len(polygons)-1)

            print("Доступные трансформации:")
            print("  t — перенос")
            print("  r — поворот")
            print("  s — симметрия")
            print("  h — гомотетия")

            tr = input_choice("Выберите трансформацию: ", ['t', 'r', 's', 'h'])

            if tr == 't':
                dx = input_float("Смещение по x: ")
                dy = input_float("Смещение по y: ")
                polygons[index] = tr_translate(polygons[index], dx, dy)

            elif tr == 'r':
                angle = input_float("Угол поворота (градусы): ")
                cx = input_float("X центра поворота (по умолчанию 0): ")
                cy = input_float("Y центра поворота (по умолчанию 0): ")
                polygons[index] = tr_rotate(polygons[index], angle, cx, cy)

            elif tr == 's':
                axis = input_choice("Ось симметрии (x или y): ", ['x', 'y'])
                polygons[index] = tr_symmetry(polygons[index], axis)

            elif tr == 'h':
                k = input_float("Коэффициент масштабирования: ")
                cx = input_float("X центра гомотетии (по умолчанию 0): ")
                cy = input_float("Y центра гомотетии (по умолчанию 0): ")
                polygons[index] = tr_homothety(polygons[index], k, cx, cy)

            print("Трансформация выполнена.")

        elif choice == "5":
            if not polygons:
                print("Нет полигонов для визуализации.")
            else:
                visualize_polygons(polygons)

        elif choice == "6":
            polygons.clear()
            print("Список очищен.")

        elif choice == "7":
            print("Выход из программы.")
            break

if __name__ == "__main__":
    main_console()
