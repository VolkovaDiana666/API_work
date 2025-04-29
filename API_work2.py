import math
import itertools
from functools import reduce
from typing import Iterator, Tuple, List, Optional, Callable
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

Polygon = Tuple[Tuple[float, float], ...]


#1. Базовые функции генерации полигонов
def gen_rectangle(width: float = 1.0, height: float = 1.0) -> Polygon:
    """Генерирует прямоугольник с заданными шириной и высотой"""
    return ((0, 0), (0, height), (width, height), (width, 0))


def gen_triangle(side: float = 1.0) -> Polygon:
    """Генерирует равносторонний треугольник с заданной стороной"""
    height = side * math.sqrt(3) / 2
    return ((0, 0), (side, 0), (side / 2, height))


def gen_hexagon(side: float = 1.0) -> Polygon:
    """Генерирует правильный шестиугольник с заданной стороной"""
    return tuple(
        (side * math.cos(math.radians(angle)),
         side * math.sin(math.radians(angle)))
        for angle in range(0, 360, 60)
    )


#2. Функции трансформации полигонов
def tr_translate(poly: Polygon, dx: float, dy: float) -> Polygon:
    """Параллельный перенос полигона на (dx, dy)"""
    return tuple((x + dx, y + dy) for x, y in poly)


def tr_rotate(poly: Polygon, angle_deg: float, cx: float = 0, cy: float = 0) -> Polygon:
    """Поворот полигона на angle_deg градусов вокруг точки (cx, cy)"""
    angle_rad = math.radians(angle_deg)
    sin, cos = math.sin(angle_rad), math.cos(angle_rad)
    return tuple(
        (cx + (x - cx) * cos - (y - cy) * sin,
         cy + (x - cx) * sin + (y - cy) * cos)
        for x, y in poly
    )


def tr_symmetry(poly: Polygon, axis: str = 'x') -> Polygon:
    """Симметрия полигона относительно оси ('x' или 'y')"""
    if axis == 'x':
        return tuple((x, -y) for x, y in poly)
    return tuple((-x, y) for x, y in poly)


def tr_homothety(poly: Polygon, k: float, cx: float = 0, cy: float = 0) -> Polygon:
    """Гомотетия (масштабирование) полигона с коэффициентом k относительно (cx, cy)"""
    return tuple(
        (cx + (x - cx) * k,
         cy + (y - cy) * k)
        for x, y in poly
    )


#3. Функции фильтрации полигонов
def flt_convex_polygon(polygons: Iterator[Polygon]) -> Iterator[Polygon]:
    """Фильтр выпуклых многоугольников"""
    return filter(is_convex, polygons)


def flt_angle_point(polygons: Iterator[Polygon], point: Tuple[float, float]) -> Iterator[Polygon]:
    """Фильтр полигонов, имеющих хотя бы один угол в заданной точке"""
    return filter(
        lambda p: any(math.isclose(x, point[0]) and math.isclose(y, point[1])
                      for x, y in p),
        polygons
    )


def flt_square(polygons: Iterator[Polygon], max_area: float) -> Iterator[Polygon]:
    """Фильтр полигонов с площадью меньше max_area"""
    return filter(lambda p: polygon_area(p) < max_area, polygons)


def flt_short_side(polygons: Iterator[Polygon], min_length: float) -> Iterator[Polygon]:
    """Фильтр полигонов с кратчайшей стороной меньше min_length"""
    return filter(
        lambda p: any(math.hypot(x2 - x1, y2 - y1) < min_length
                      for (x1, y1), (x2, y2) in zip(p, p[1:] + p[:1])),
        polygons
    )


def flt_point_inside(polygons: Iterator[Polygon], point: Tuple[float, float]) -> Iterator[Polygon]:
    """Фильтр выпуклых полигонов, содержащих заданную точку внутри"""
    return filter(
        lambda p: is_convex(p) and point_in_polygon(p, point),
        polygons
    )


def flt_polygon_angles_inside(polygons: Iterator[Polygon], target: Polygon) -> Iterator[Polygon]:
    """Фильтр выпуклых полигонов, содержащих любой из углов целевого полигона"""
    return filter(
        lambda p: is_convex(p) and any(point_in_polygon(p, angle) for angle in target),
        polygons
    )


#4. Функции агрегации
def agr_origin_nearest(polygons: Iterator[Polygon]) -> Optional[Tuple[float, float]]:
    """Находит угол полигона, ближайший к началу координат"""
    return reduce(
        lambda closest, poly: min(
            (*poly, closest),
            key=lambda p: math.hypot(p[0], p[1])
        ),
        polygons,
        (math.inf, math.inf)
    )


def agr_max_side(polygons: Iterator[Polygon]) -> float:
    """Находит длину самой длинной стороны среди всех полигонов"""
    return reduce(
        lambda max_len, poly: max(
            max_len,
            max(math.hypot(x2 - x1, y2 - y1)
                for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]))
        ),
        polygons,
        0.0
    )


def agr_min_area(polygons: Iterator[Polygon]) -> float:
    """Находит самую маленькую площадь среди полигонов"""
    return reduce(
        lambda min_a, poly: min(min_a, polygon_area(poly)),
        polygons,
        math.inf
    )


def agr_perimeter(polygons: Iterator[Polygon]) -> float:
    """Вычисляет суммарный периметр всех полигонов"""
    return reduce(
        lambda total, poly: total + polygon_perimeter(poly),
        polygons,
        0.0
    )


def agr_area(polygons: Iterator[Polygon]) -> float:
    """Вычисляет суммарную площадь всех полигонов"""
    return reduce(
        lambda total, poly: total + polygon_area(poly),
        polygons,
        0.0
    )


#5. Визуализация
def visualize_polygons(polygons: List[Polygon], title: str = "Визуализация полигонов"):
    """Визуализирует список полигонов с помощью matplotlib"""
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    colors = itertools.cycle(['red', 'green', 'blue', 'orange', 'purple'])
    for i, poly in enumerate(polygons):
        x, y = zip(*poly)
        ax.fill(x, y, next(colors), alpha=0.5, label=f'Фигура {i + 1}')

    ax.legend()
    ax.grid(True)
    plt.title(title)
    plt.show()


#Вспомогательные функции
def is_convex(poly: Polygon) -> bool:
    """Проверяет, является ли полигон выпуклым"""
    n = len(poly)
    if n < 3:
        return False

    cross_products = []
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        x2, y2 = poly[(i + 2) % n]

        # Векторное произведение
        cross = (x1 - x0) * (y2 - y1) - (y1 - y0) * (x2 - x1)
        cross_products.append(cross)

    return all(c >= 0 for c in cross_products) or all(c <= 0 for c in cross_products)


def polygon_area(poly: Polygon) -> float:
    """Вычисляет площадь полигона по формуле шнуровки"""
    n = len(poly)
    area = 0.0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        area += (x1 * y2) - (x2 * y1)
    return abs(area) / 2


def polygon_perimeter(poly: Polygon) -> float:
    """Вычисляет периметр полигона"""
    return sum(
        math.hypot(x2 - x1, y2 - y1)
        for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1])
    )


def point_in_polygon(poly: Polygon, point: Tuple[float, float]) -> bool:
    """Проверяет, лежит ли точка внутри полигона (метод луча)"""
    x, y = point
    n = len(poly)
    inside = False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        if (min(x1, x2) <= x <= max(x1, x2)) and (min(y1, y2) <= y <= max(y1, y2)):
            if abs((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)) < 1e-12:
                return True

        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            inside = not inside
    return inside


# Пример использования
if __name__ == "__main__":
    # 1. Генерация фигур
    rectangles = [tr_translate(gen_rectangle(1, 1.5), x * 2, 0) for x in range(3)]
    triangles = [tr_rotate(gen_triangle(1.2), 30 * x) for x in range(3)]
    hexagons = [tr_homothety(gen_hexagon(0.8), 0.9 ** x) for x in range(3)]

    # 2. Фильтрация
    filtered = list(flt_convex_polygon(
        flt_square(
            itertools.chain(rectangles, triangles, hexagons),
            max_area=5.0
        )
    ))

    # 3. Анализ
    closest = agr_origin_nearest(iter(filtered))
    max_side = agr_max_side(iter(filtered))
    total_area = agr_area(iter(filtered))

    print(f"Ближайшая к началу координат вершина: {closest}")
    print(f"Самая длинная сторона: {max_side:.2f}")
    print(f"Суммарная площадь: {total_area:.2f}")

    # 4. Визуализация
    visualize_polygons(filtered[:6], "Пример работы с полигонами")


